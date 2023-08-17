from dataclasses import dataclass
from typing import Optional

from typing_extensions import Self


@dataclass(frozen=True)
class EnsureConfidenced(object):
    def __post_init__(self):
        if not isinstance(self, Confidenced):
            raise TypeError(f"{type(self)} should inherit {AbstractValue}. Actual mro is {type(self).mro()}")


@dataclass(frozen=True)
class Confidenced(object):
    confidence: Optional[float] = None

    def __post_init__(self):
        if self.confidence is not None and not 0 < self.confidence <= 1:
            raise ValueError(f"value confidence should be in interval (0; 1], {self.confidence} is given")
        for type_ in type(self).mro():
            if issubclass(type_, Confidenced):
                continue
            if hasattr(type_, '__post_init__'):
                type_.__post_init__(self)


@dataclass(frozen=True)
class AbstractConceptValue(Confidenced):
    pass


@dataclass(frozen=True)
class AbstractValue(Confidenced):
    @classmethod
    def from_dict(cls, value: dict) -> Self:
        return cls(**value)
