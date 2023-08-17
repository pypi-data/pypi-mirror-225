from dataclasses import dataclass

from tdm.abstract.datamodel import AbstractLinkFact, Identifiable
from tdm.abstract.json_schema import generate_model
from tdm.datamodel.domain import RelationPropertyType, RelationType, SlotType
from .concept import ConceptFact
from .value import CompositeValueFact, ValueFact


@generate_model(label='relation')
@dataclass(frozen=True, eq=False)
class RelationFact(Identifiable, AbstractLinkFact[ConceptFact, ConceptFact, RelationType]):
    pass


@generate_model(label='r_property')
@dataclass(frozen=True, eq=False)
class RelationPropertyFact(Identifiable, AbstractLinkFact[RelationFact, ValueFact, RelationPropertyType]):
    pass


@generate_model(label='slot')
@dataclass(frozen=True, eq=False)
class SlotFact(Identifiable, AbstractLinkFact[CompositeValueFact, ValueFact, SlotType]):
    pass
