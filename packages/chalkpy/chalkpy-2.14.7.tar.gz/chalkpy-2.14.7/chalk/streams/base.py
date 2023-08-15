from __future__ import annotations

from typing import Any


class StreamSource:
    """Base class for all stream sources generated from `@stream`."""

    registry: "list[StreamSource]" = []

    def _config_to_json(self) -> Any:
        ...

    @property
    def streaming_type(self) -> str:
        """e.g. 'kafka' or 'kinesis'"""
        raise NotImplementedError()

    @property
    def dlq_name(self) -> str | None:
        """stream name for kinesis, topic for kafka"""
        raise NotImplementedError()
