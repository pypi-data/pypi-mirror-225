from dataclasses import dataclass
from typing import Type

from tdm.abstract.datamodel import Identifiable
from tdm.abstract.datamodel.domain import AbstractValueDomainType
from tdm.abstract.datamodel.value import AbstractConceptValue


@dataclass(frozen=True)
class AbstractConceptType(Identifiable, AbstractValueDomainType[AbstractConceptValue]):
    value_type: Type[AbstractConceptValue] = AbstractConceptValue


@dataclass(frozen=True)
class ConceptType(AbstractConceptType):
    pass


@dataclass(frozen=True)
class DocumentType(AbstractConceptType):
    pass


#  following classes could be removed after v0 support stop

@dataclass(frozen=True)
class AccountType(AbstractConceptType):
    pass


@dataclass(frozen=True)
class PlatformType(AbstractConceptType):
    pass
