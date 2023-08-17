from dataclasses import dataclass

from tdm.abstract.datamodel import AbstractValue, Identifiable
from tdm.abstract.datamodel.domain import AbstractValueDomainType


@dataclass(frozen=True)
class AtomValueType(Identifiable, AbstractValueDomainType[AbstractValue]):
    pass
