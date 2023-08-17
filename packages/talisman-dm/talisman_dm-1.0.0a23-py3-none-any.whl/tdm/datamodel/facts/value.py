from abc import ABCMeta
from dataclasses import dataclass, replace
from typing import Callable, Set, Union

from tdm.abstract.datamodel import AbstractDomain, AbstractFact, Identifiable
from tdm.abstract.datamodel.fact import AbstractValueFact
from tdm.abstract.datamodel.value import AbstractValue
from tdm.abstract.json_schema import generate_model
from tdm.datamodel.domain import AtomValueType, CompositeValueType


@generate_model(label='atom')
@dataclass(frozen=True)
class AtomValueFact(Identifiable, AbstractValueFact[AtomValueType, AbstractValue]):

    def replace_with_domain(self, domain: AbstractDomain) -> 'AtomValueFact':
        if isinstance(self.type_id, str):
            domain_type = domain.get_type(self.type_id)
            if not isinstance(domain_type, AtomValueType):
                raise ValueError
            return replace(self, type_id=domain_type)
        return self

    def _as_tuple(self) -> tuple:
        return self.id, (self.type_id if isinstance(self.type_id, str) else self.type_id.id), self.value

    def __eq__(self, other):
        if not isinstance(other, AtomValueFact):
            return NotImplemented
        return self._as_tuple() == other._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())

    @staticmethod
    def empty_value_filter() -> Callable[['AtomValueFact'], bool]:
        return lambda f: isinstance(f.value, tuple) and not f.value

    @staticmethod
    def tuple_value_filter() -> Callable[['AtomValueFact'], bool]:
        return lambda f: isinstance(f.value, tuple)

    @staticmethod
    def single_value_filter() -> Callable[['AtomValueFact'], bool]:
        return lambda f: isinstance(f.value, AbstractValue)


@dataclass(frozen=True)
class _CompositeValueFact(AbstractFact, metaclass=ABCMeta):
    type_id: Union[str, CompositeValueType]

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'type_id'}


@generate_model(label='composite')
@dataclass(frozen=True)
class CompositeValueFact(Identifiable, _CompositeValueFact):

    def replace_with_domain(self, domain: AbstractDomain) -> 'CompositeValueFact':
        if isinstance(self.type_id, str):
            domain_type = domain.get_type(self.type_id)
            if not isinstance(domain_type, CompositeValueType):
                raise ValueError
            return replace(self, type_id=domain_type)
        return self

    def _as_tuple(self) -> tuple:
        return self.id, (self.type_id if isinstance(self.type_id, str) else self.type_id.id)

    def __eq__(self, other):
        if not isinstance(other, CompositeValueFact):
            return NotImplemented
        return self._as_tuple() == other._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())


ValueFact = Union[AtomValueFact, CompositeValueFact]
