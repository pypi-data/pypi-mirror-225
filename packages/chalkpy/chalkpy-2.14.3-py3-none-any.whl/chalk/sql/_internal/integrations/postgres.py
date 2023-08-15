from __future__ import annotations

import contextlib
import csv
import io
import logging
import os
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union

import pyarrow as pa
import pyarrow.csv

from chalk.features import FeatureConverter
from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import (
    BaseSQLSource,
    SQLSourceKind,
    TableIngestMixIn,
    UnsupportedEfficientExecutionError,
    validate_dtypes_for_efficient_execution,
)
from chalk.sql.finalized_query import FinalizedChalkQuery, Finalizer
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine import URL, Connection

try:
    import sqlalchemy as sa
except ImportError:
    sa = None

if sa is None:
    _supported_sqlalchemy_types_for_pa_csv_querying = ()
else:
    _supported_sqlalchemy_types_for_pa_csv_querying = (
        sa.BigInteger,
        sa.Boolean,
        sa.Float,
        sa.Integer,
        sa.String,
        sa.Text,
        sa.DateTime,
        sa.Date,
        sa.SmallInteger,
        sa.BIGINT,
        sa.BOOLEAN,
        sa.CHAR,
        sa.DATETIME,
        sa.FLOAT,
        sa.INTEGER,
        sa.SMALLINT,
        sa.TEXT,
        sa.TIMESTAMP,
        sa.VARCHAR,
    )

_logger = get_logger(__name__)


class PostgreSQLSourceImpl(BaseSQLSource, TableIngestMixIn, SQLSourceWithTableIngestProtocol):
    kind = SQLSourceKind.postgres

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        async_engine_args: Optional[Dict[str, Any]] = None,
    ):
        try:
            import psycopg  # Used for the async driver
            import psycopg2  # Used for the sync driver
            import sqlalchemy.dialects
        except ImportError:
            raise missing_dependency_exception("chalkpy[postgresql]")
        del psycopg2  # unused
        del psycopg  # unused
        if "postgresql.psycopg" not in sqlalchemy.dialects.registry.impls:
            sqlalchemy.dialects.registry.register(
                "postgresql.psycopg", "chalk.sql._internal.integrations.psycopg3.psycopg_dialect", "dialect"
            )
        if "postgresql.psycopg_async" not in sqlalchemy.dialects.registry.impls:
            sqlalchemy.dialects.registry.register(
                "postgresql.psycopg_async", "chalk.sql._internal.integrations.psycopg3.psycopg_dialect", "dialect_async"
            )
        self.name = name
        self.host = host or load_integration_variable(integration_name=name, name="PGHOST")
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(integration_name=name, name="PGPORT", parser=int)
        )
        self.db = db or load_integration_variable(integration_name=name, name="PGDATABASE")
        self.user = user or load_integration_variable(integration_name=name, name="PGUSER")
        self.password = password or load_integration_variable(integration_name=name, name="PGPASSWORD")
        self.ingested_tables: Dict[str, Any] = {}
        if engine_args is None:
            engine_args = {}
        if async_engine_args is None:
            async_engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        async_engine_args.setdefault("pool_size", 20)
        async_engine_args.setdefault("max_overflow", 60)
        async_engine_args.setdefault(
            "connect_args",
            {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )
        engine_args.setdefault(
            "connect_args",
            {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )
        # We set the default isolation level to autocommit since the SQL sources are read-only, and thus
        # transactions are not needed
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool
        engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        async_engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args=async_engine_args)

    def get_sqlglot_dialect(self) -> str | None:
        return "postgres"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def async_local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql+psycopg_async",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def _get_parsed_table_via_polars(
        self,
        finalized_query: FinalizedChalkQuery,
        connection: Optional[Connection],
        columns_to_converters: Callable[[List[str]], Dict[str, FeatureConverter]],
    ) -> pyarrow.Table:
        import polars as pl

        buffer = self._get_result_csv_buffer(finalized_query, connection=connection, escape_char='"')

        first_line = buffer.readline()
        column_names = list(csv.reader([first_line.decode("utf8")], doublequote=True, quoting=csv.QUOTE_MINIMAL))[0]
        buffer.seek(0)
        converters = columns_to_converters(column_names)

        parse_dtypes = {}
        boolean_columns = []
        for col_name, converter in converters.items():
            dtype = converter.polars_dtype
            if dtype == pl.Boolean:
                # Parsing "t" and "f" as booleans fails.
                # We will parse the column as a string, and then
                # convert it to a boolean later.
                parse_dtypes[col_name] = pl.Utf8
                boolean_columns.append(col_name)
            elif dtype == pl.List:
                # We will parse the list as a string, and then
                # convert it to a list later. Polars does not
                # support parsing lists directly from CSV.
                parse_dtypes[col_name] = pl.Utf8
            elif dtype == pl.Datetime:
                # This might seem odd, but the equality operator
                # for `pl.Datetime` is overridden, and this means
                # `dtype` can be an instance of `pl.Datetime`
                # with a timezone or time unit set, and we want
                # to parse without those because Ramp, for example,
                # returns datetimes that are tricky to parse
                # with the timezone or time unit set.
                #
                # We will cast to the target timezone and time unit
                # when casting to the final pyarrow dtype.
                parse_dtypes[col_name] = pl.Datetime
            else:
                parse_dtypes[col_name] = dtype

        """
        CSV -> Polars -> Pyarrow table
        """
        boolean_mappings = [
            pl.col(bool_col).map_dict({"f": False, "t": True}, return_dtype=pl.Boolean) for bool_col in boolean_columns
        ]
        # Previously we were using `pyarrow.csv.read_csv` but performance
        # degraded over time up till the next FastAPI reboot.
        pl_table = pl.read_csv(buffer, dtypes=parse_dtypes)
        if boolean_mappings:
            pl_table = pl_table.with_columns(*boolean_mappings)

        parsed_table = pl_table.to_arrow()
        if len(converters) != len(parsed_table.column_names):
            _logger.warn(
                f"mismatch in number of columns between query and converters: {len(converters)=}, {len(parsed_table.column_names)=}"
            )

        """
        Pyarrow table -> Pyarrow table with correct dtype
        """
        # Cast to target pyarrow dtypes. Some of the columns may have been parsed with
        # the correct polars dtype and then cast to the correct pyarrow dtype, but
        # some other columns such as lists and booleans have intentionally not been cast.
        restricted_schema = pa.schema([pa.field(k, v.pyarrow_dtype) for (k, v) in converters.items()])
        # Reorder columns to match order of the schema.
        return parsed_table.select([c for c in converters.keys()]).cast(restricted_schema)

    def _get_result_csv_buffer(
        self, finalized_query: FinalizedChalkQuery, connection: Optional[Connection], escape_char: str
    ) -> io.BytesIO:
        import psycopg2.sql

        stmt, positional_params, named_params = self.compile_query(finalized_query, paramstyle="named")
        assert len(positional_params) == 0, "should not have any positional params"

        # Forcing quote so the unquoted empty string will represent null values
        stmt = f"COPY ({stmt}) TO STDOUT (FORMAT CSV, HEADER true, FORCE_QUOTE *, ESCAPE '{escape_char}')"
        # Convert the param style to python3-style {}, which is what psycopg2.sql.SQL.format expects
        for named_param in named_params:
            stmt = stmt.replace(f":{named_param}", ("{" f"{named_param}" "}"))
        formatted_stmt = psycopg2.sql.SQL(stmt).format(
            **{k: psycopg2.sql.Literal(v) for (k, v) in named_params.items()}
        )
        with self.get_engine().connect() if connection is None else contextlib.nullcontext(connection) as cnx:
            dbapi = cnx.connection
            with dbapi.cursor() as cursor:
                buffer = io.BytesIO()
                cursor.copy_expert(formatted_stmt, buffer)
        buffer.seek(0)

        return buffer

    def execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_converters: Callable[[List[str]], Dict[str, FeatureConverter]],
        connection: Optional[Connection],
        polars_read_csv: bool = False,
    ) -> pa.Table:
        from sqlalchemy.sql import Select

        if env_var_bool("CHALK_FORCE_SQLALCHEMY_QUERY_EXECUTION_WITHOUT_EXCEPTION"):
            raise UnsupportedEfficientExecutionError(
                (
                    f"The SQL statement will be executed into SQLAlchemy objects, as the environment "
                    "variable 'CHALK_FORCE_SQLALCHEMY_QUERY_EXECUTION' is set. Unset this variable to execute "
                    "the query directly into a PyArrow table."
                ),
                log_level=logging.DEBUG,
            )

        if finalized_query.finalizer in (Finalizer.FIRST, Finalizer.ONE, Finalizer.ONE_OR_NONE):
            raise UnsupportedEfficientExecutionError(
                (
                    f"Falling back to SQLAlchemy execution for finalizer '{finalized_query.finalizer.value}', "
                    "as it is faster for small results."
                ),
                log_level=logging.DEBUG,
            )

        if isinstance(finalized_query.query, Select):
            validate_dtypes_for_efficient_execution(
                finalized_query.query, _supported_sqlalchemy_types_for_pa_csv_querying
            )

        if polars_read_csv:
            try:
                return self._get_parsed_table_via_polars(finalized_query, connection, columns_to_converters)
            except Exception as e:
                _logger.error("Failed to parse CSV with Polars, falling back to PyArrow CSV reader", exc_info=e)

        buffer = self._get_result_csv_buffer(finalized_query, connection=connection, escape_char="\\")

        # Peek the column names
        first_line = buffer.readline()
        column_names = list(
            csv.reader([first_line.decode("utf8")], escapechar="\\", doublequote=False, quoting=csv.QUOTE_ALL)
        )[0]
        buffer.seek(0)
        converters = columns_to_converters(column_names)

        if env_var_bool("CSV_READ_THEN_CAST"):
            # This seems to tolerant unzoned datetimes better
            parsed_table = pyarrow.csv.read_csv(
                buffer,
                parse_options=pyarrow.csv.ParseOptions(
                    newlines_in_values=True,
                    escape_char="\\",
                    double_quote=False,
                ),
                convert_options=pyarrow.csv.ConvertOptions(
                    true_values=["t"],
                    false_values=["f"],
                    strings_can_be_null=True,
                    quoted_strings_can_be_null=False,
                ),
            )

            if len(converters) != len(parsed_table.column_names):
                _logger.warn(
                    f"mismatch in number of columns between query and converters: {len(converters)=}, {len(parsed_table.column_names)=}"
                )

            restricted_schema = pa.schema([pa.field(k, v.pyarrow_dtype) for (k, v) in converters.items()])
            try:
                return parsed_table.cast(restricted_schema)
            except:
                _logger.warn(f"Falling back from cast in postgres")
                return parsed_table.select([c for c in converters.keys()]).cast(restricted_schema)

        else:
            schema = pa.schema([pa.field(k, v.pyarrow_dtype) for (k, v) in converters.items()])
            return pyarrow.csv.read_csv(
                buffer,
                parse_options=pyarrow.csv.ParseOptions(
                    newlines_in_values=True,
                    escape_char="\\",
                    double_quote=False,
                ),
                convert_options=pyarrow.csv.ConvertOptions(
                    true_values=["t"],
                    false_values=["f"],
                    strings_can_be_null=True,
                    quoted_strings_can_be_null=False,
                    column_types=schema,
                ),
            )
