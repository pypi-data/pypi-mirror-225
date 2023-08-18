from abc import ABC, abstractmethod

from autoapi.schema.data import Annotation


class ISerializer(ABC):
    content_parsers: list['ITypeSerializer']

    @abstractmethod
    def deserialize(self, content: str | list | dict, annotation: Annotation) -> any:
        """
        Превращает словари из content в модели из annotation, включая все вложенные
        """

    @abstractmethod
    def serialize(self, content: any, annotation: Annotation) -> any:
        """
        Сериализовывает значение
        """


class ITypeSerializer(ABC):
    content_deserializer: 'ISerializer'

    @abstractmethod
    def check(self, annotation: Annotation):
        """
        Проверяет по аннотации, можно ли десериализовать значение
        с помощью этого класса
        """

    @abstractmethod
    def serialize(self, content: any, annotation: Annotation) -> any:
        """
        Сериализовывает значение
        """

    @abstractmethod
    def deserialize(self, content: any, annotation: Annotation) -> any:
        """
        Десериализовывает значение
        """