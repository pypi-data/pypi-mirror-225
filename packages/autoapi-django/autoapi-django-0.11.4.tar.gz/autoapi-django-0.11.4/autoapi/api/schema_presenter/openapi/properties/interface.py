from abc import ABC, abstractmethod

from autoapi.schema.data import Type, Annotation


class IComponentBuilder(ABC):

    @abstractmethod
    def check(self, annotation: Annotation) -> bool:
        ...

    @abstractmethod
    def parse(self, annotation: Annotation) -> dict:
        ...
