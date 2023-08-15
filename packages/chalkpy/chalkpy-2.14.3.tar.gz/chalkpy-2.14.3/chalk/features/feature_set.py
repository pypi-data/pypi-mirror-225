from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Dict, Iterator, List, Optional, Tuple, Type, cast

from typing_extensions import TypeGuard

from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
from chalk.features.live_updates import register_live_updates_if_in_notebook
from chalk.utils.collections import ensure_tuple, get_unique_item

__all__ = ["Features", "FeaturesMeta", "FeatureSetBase", "is_features_cls"]


class FeaturesMeta(type):
    """Metaclass for classes decorated with ``@features``.

    This metaclass allows for:

    1.  Classes annotated with @features to pass the
        ``isinstance(x, Features)`` and ``issubclass(X, Features)`` checks.
    2.  ``Features[Feature1, Feature2]`` annotations to return subclasses of Features, so they can be used as proper type annotations.
    """

    def __subclasscheck__(self, subcls: type) -> bool:
        if not isinstance(subcls, type):
            raise TypeError(f"{subcls} is not a type")
        if hasattr(subcls, "__is_features__"):
            return getattr(subcls, "__is_features__")
        return False

    def __instancecheck__(self, instance: object) -> bool:
        return self.__subclasscheck__(type(instance))

    def __getitem__(cls, item: Any) -> Any:
        # This lets us subscript by the features
        # Annotating the return type as Type[Any] as instances of @features classes are
        # not recognized as being subclasses of Features by the type checker (even though at runtime they would be)
        from chalk.features.dataframe import DataFrame

        is_exploded = False

        # Typing the `__getitem__` as any, since the @features members are typed as the underlying data structure
        # But, they should always be features or a tuple of features
        if isinstance(item, type) and issubclass(item, Features):
            is_exploded = True
            item = [
                f
                for f in item.features
                if not f.is_autogenerated and not f.is_has_one and not f.is_has_many and not f.is_windowed
            ]
        item = ensure_tuple(item)
        item = tuple(unwrap_feature(x) if isinstance(x, FeatureWrapper) else x for x in item)
        for x in item:
            if isinstance(x, str):
                raise TypeError(
                    f'String features like {cls.__name__}["{x}"] are unsupported. Instead, replace with "{cls.__name__}[{x}]"'
                )
            if isinstance(x, Feature) or (isinstance(x, type) and issubclass(x, DataFrame)):
                continue

            raise TypeError(f"Invalid feature {x} of type {type(x).__name__}")
        cls = cast(Type[Features], cls)

        new_features = tuple([*cls.features, *item])
        if len(new_features) == 0:
            raise ValueError("Cannot create empty Features[] class")

        class SubFeatures(cls):
            __is_exploded__ = is_exploded
            features = new_features

        return SubFeatures

    def __repr__(cls) -> str:
        cls = cast(Type[Features], cls)
        return f"Features[{', '.join(str(f) for f in cls.features)}]"

    def __call__(cls, *args: object, **kwargs: object):
        raise RuntimeError("Instances features cls should never be directly created. Instead, use Features[User.id]")

    def __sub__(self, other):
        if isinstance(other, FeaturesMeta):
            other_features = set(other.features)
            return FeaturesImpl[tuple(f for f in self.features if f not in other_features)]
        if isinstance(other, FeatureWrapper):
            return FeaturesImpl[tuple(f for f in self.features if f != other._chalk_feature)]
        raise TypeError(f"Invalid type {type(other)} for subtraction with Features[...]")

    @property
    def namespace(cls):
        cls = cast(Type[Features], cls)
        namespaces = [x.namespace for x in cls.features]
        return get_unique_item(namespaces, name=f"{cls.__name__} feature namespaces")


class FeaturesImpl(metaclass=FeaturesMeta):
    """Features base class.

    This class is never instantiated or directly inherited. However, classes
    annotated with @features can be thought of as inheriting from this class.
    It can be used with ``isinstance`` and ``issubclass`` checks, as well as for
    typing.
    """

    # Internally, the Features class is instantiated when results come through, and
    # results are bound to instances of this class via attributes
    __chalk_etl_offline_to_online__: ClassVar[bool]
    __chalk_max_staleness__: ClassVar[timedelta]
    __chalk_namespace__: ClassVar[str]
    __chalk_primary__: ClassVar[Optional[Feature]]  # The primary key feature
    __chalk_owner__: ClassVar[Optional[str]]
    __chalk_tags__: ClassVar[List[str]]
    __chalk_ts__: ClassVar[Optional[Feature]]  # The timestamp feature
    __chalk_feature_fqns_raw__: ClassVar[List[str]]
    features: ClassVar[Tuple[Feature, ...]] = ()  # TODO: This is actually set to a list at creation.
    __is_exploded__: ClassVar[bool] = False
    __is_features__: ClassVar[bool] = True

    # When constructing results, this class is instantiated

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Iterating over features yields tuples of (fqn, value) for all scalarish feature values."""
        raise NotImplementedError

    def __len__(self) -> int:
        """The number of features that are set."""
        raise NotImplementedError

    def items(self) -> Iterator[Tuple[str, Any]]:
        """Iterating over features yields tuples of (fqn, value) for all feature values."""
        raise NotImplementedError


# Hack to get VSCode/Pylance/Pyright to type Features as Type[FeatureImpl]
# but IntelliJ to type it as Type[Any]
# Vscode can parse through literal dicts; IntelliJ can't
if TYPE_CHECKING:

    class FeaturesProtocol(FeaturesImpl):
        def __class_getitem__(cls, item: Any) -> "FeaturesProtocol":
            ...

    _dummy_dict = {"0": FeaturesProtocol}
else:
    _dummy_dict = {"0": FeaturesImpl}

Features = _dummy_dict["0"]


class FeatureSetBase:
    """Registry containing all @features classes."""

    registry: ClassVar[Dict[str, Type[Features]]] = {}  # mapping of fqn to Features cls
    hook: ClassVar[Optional[Callable[[Features], None]]] = None

    def __init__(self) -> None:
        raise RuntimeError("FeatureSetBase should never be instantiated")


register_live_updates_if_in_notebook(FeatureSetBase)


def is_features_cls(maybe_features: Any) -> TypeGuard[Type[FeaturesProtocol]]:
    """BEWARE: this returns true for FeatureClass but also Features[...]"""

    return isinstance(maybe_features, type) and issubclass(maybe_features, Features)


def is_feature_set_class(maybe_features: Any) -> TypeGuard[Type[FeaturesImpl]]:
    return is_features_cls(maybe_features) and getattr(maybe_features, "__chalk_feature_set__", False)
