from dataclasses import dataclass, replace
from typing import Callable, Tuple, TypeVar, Union

from typing_extensions import Self

from tdm.abstract.datamodel import AbstractDomain, AbstractLinkFact, AbstractValue, FactStatus, Identifiable
from tdm.abstract.datamodel.fact import AbstractValueFact
from tdm.abstract.datamodel.value import AbstractConceptValue, EnsureConfidenced
from tdm.abstract.json_schema import generate_model
from tdm.datamodel.domain import PropertyType
from tdm.datamodel.domain.types import AbstractConceptType
from tdm.datamodel.facts.value import ValueFact


@dataclass(frozen=True)
class _KBConceptValue(EnsureConfidenced):
    concept: str


@dataclass(frozen=True)
class KBConceptValue(AbstractConceptValue, _KBConceptValue):
    @classmethod
    def build(cls, value: Union[str, 'KBConceptValue']) -> 'KBConceptValue':
        if isinstance(value, KBConceptValue):
            return value
        if isinstance(value, str):
            return cls(concept=value)
        raise ValueError


_PT = TypeVar('_PT', bound=PropertyType)
_VT = TypeVar('_VT', bound=AbstractValue)


@dataclass(frozen=True)
class ConceptPropertyValue(object):
    type_id: Union[str, PropertyType]
    value: AbstractValue

    @classmethod
    def from_property_fact(cls, fact: 'PropertyFact') -> Self:
        value = fact.target.value
        if isinstance(value, tuple):
            if len(value) > 1:
                raise ValueError
            value = value[0]
        return cls(type_id=fact.type_id, value=value)


@dataclass(frozen=True)
class _MissedConceptValue(EnsureConfidenced):
    filters: Tuple[ConceptPropertyValue, ...]

    def __post_init__(self):
        if not self.filters:
            raise ValueError


@dataclass(frozen=True)
class MissedConceptValue(AbstractConceptValue, _MissedConceptValue):
    pass


ConceptValue = Union[KBConceptValue, MissedConceptValue]


@generate_model(label='concept')
@dataclass(frozen=True)
class ConceptFact(Identifiable, AbstractValueFact[AbstractConceptType, ConceptValue]):

    def __post_init__(self):
        Identifiable.__post_init__(self)
        if isinstance(self.value, tuple):
            if len([v for v in self.value if isinstance(v, MissedConceptValue)]) > 1:
                raise ValueError(f"Concept fact {self} can't contain more than 1 missed value")
        if isinstance(self.value, MissedConceptValue):
            if self.status is FactStatus.APPROVED:
                raise ValueError(f"Approved fact {self} can't be with missed value.")

    def replace_with_domain(self, domain: AbstractDomain) -> 'ConceptFact':
        if isinstance(self.type_id, str):
            domain_type = domain.get_type(self.type_id)
            if not isinstance(domain_type, AbstractConceptType):
                raise ValueError
            return replace(self, type_id=domain_type)
        return self

    def _as_tuple(self) -> tuple:
        return self.id, (self.type_id if isinstance(self.type_id, str) else self.type_id.id), self.value

    def __eq__(self, other):
        if not isinstance(other, ConceptFact):
            return NotImplemented
        return self._as_tuple() == other._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())

    @staticmethod
    def empty_value_filter() -> Callable[['ConceptFact'], bool]:
        return lambda f: isinstance(f.value, tuple) and not f.value

    @staticmethod
    def tuple_value_filter() -> Callable[['ConceptFact'], bool]:
        return lambda f: isinstance(f.value, tuple)

    @staticmethod
    def single_value_filter() -> Callable[['ConceptFact'], bool]:
        return lambda f: isinstance(f.value, ConceptValue)


@generate_model(label='property')
@dataclass(frozen=True, eq=False)
class PropertyFact(Identifiable, AbstractLinkFact[ConceptFact, ValueFact, PropertyType]):
    pass
