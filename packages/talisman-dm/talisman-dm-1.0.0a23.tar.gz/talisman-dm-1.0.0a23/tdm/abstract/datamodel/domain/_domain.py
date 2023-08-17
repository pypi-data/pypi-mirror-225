from abc import ABCMeta, abstractmethod
from typing import Callable, Dict, Iterable, Iterator, Type, TypeVar, Union

from tdm.abstract.datamodel.identifiable import Identifiable
from ._type import AbstractDomainType

_DomainType = TypeVar('_DomainType', bound=AbstractDomainType)


class AbstractDomain(metaclass=ABCMeta):
    __slots__ = ()

    @property
    @abstractmethod
    def id2type(self) -> Dict[str, AbstractDomainType]:
        pass

    @property
    @abstractmethod
    def types(self) -> Dict[Type[AbstractDomainType], Iterable[AbstractDomainType]]:
        pass

    @abstractmethod
    def get_type(self, id_: str) -> AbstractDomainType:
        pass

    @abstractmethod
    def get_types(
            self, type_: Type[_DomainType] = AbstractDomainType, *,
            filter_: Union[Callable[[_DomainType], bool], Iterable[Callable[[_DomainType], bool]]] = tuple()
    ) -> Iterator[_DomainType]:
        pass

    @abstractmethod
    def related_types(
            self, obj: Union[Identifiable, str], type_: Type[_DomainType] = AbstractDomainType, *,
            filter_: Union[Callable[[_DomainType], bool], Iterable[Callable[[_DomainType], bool]]] = tuple()
    ) -> Iterator[_DomainType]:
        pass
