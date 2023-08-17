from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import Callable, Iterable, Type, TypeVar, Union

from tdm.abstract.datamodel.domain import AbstractDomain
from tdm.abstract.datamodel.identifiable import EnsureIdentifiable


@total_ordering
class FactStatus(str, Enum):
    def __new__(cls, name: str, priority: int):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj.priority = priority
        return obj

    APPROVED = ("approved", 0)
    DECLINED = ("declined", 1)
    AUTO = ("auto", 2)
    HIDDEN = ("hidden", 3)
    NEW = ("new", 4)

    def __lt__(self, other: 'FactStatus'):
        if not isinstance(other, FactStatus):
            return NotImplemented
        return self.priority < other.priority


_Fact = TypeVar('_Fact', bound='AbstractFact')


@dataclass(frozen=True)
class AbstractFact(EnsureIdentifiable, metaclass=ABCMeta):
    status: FactStatus

    @abstractmethod
    def replace_with_domain(self: _Fact, domain: AbstractDomain) -> _Fact:
        pass

    @staticmethod
    def id_filter(obj: Union['AbstractFact', str]) -> Callable[['AbstractFact'], bool]:
        id_ = obj.id if isinstance(obj, AbstractFact) else obj

        def _filter(fact: AbstractFact) -> bool:
            return fact.id == id_

        return _filter

    @staticmethod
    def status_filter(status: Union[FactStatus, Iterable[FactStatus]]) -> Callable[['AbstractFact'], bool]:
        if isinstance(status, FactStatus):
            def _filter(fact: AbstractFact) -> bool:
                return fact.status is status
        else:
            statuses = frozenset(status)

            def _filter(fact: AbstractFact) -> bool:
                return fact.status in statuses

        return _filter

    @staticmethod
    def type_filter(type_: Type['AbstractFact']) -> Callable[['AbstractFact'], bool]:
        def _filter(fact: AbstractFact) -> bool:
            return isinstance(fact, type_)

        return _filter
