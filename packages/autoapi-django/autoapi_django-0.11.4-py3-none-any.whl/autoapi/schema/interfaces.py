from abc import ABC, abstractmethod

from autoapi.schema.data import Type, Annotation, MethodSchema, ServiceSchema
from autoapi.settings import AutoAPISettings


class IMethodBuilder(ABC):
    annotation_builder: 'IAnnotationBuilder'
    type_builder: 'ITypeBuilder'
    settings: AutoAPISettings

    @abstractmethod
    def build(self, method_name: str, method: callable) -> tuple[MethodSchema, dict[str, Type]]:
        """
        Собирает схему метода
        """


class IServiceBuilder(ABC):
    method_builder: IMethodBuilder

    @abstractmethod
    def build(self, service_cls: type) -> tuple[ServiceSchema, dict[str, Type]]:
        """
        Собирает схему класса-сервиса
        """


class ITypeParser(ABC):
    annotation_builder: 'IAnnotationBuilder'

    @abstractmethod
    def check(self, t: type) -> bool:
        """
        Подходящий ли тип для парсинга?
        """

    @abstractmethod
    def parse(self, t: type) -> tuple[Type, dict[str, Type]]:
        """
        Собирает обьект Type с поданного типа и всех подтипов
        """

    def _full_path(self, t: type) -> str:
        module = t.__module__
        full_path = t.__name__
        if module is not None and module != '__builtin__':
            full_path = module + '.' + full_path
        return full_path


class ITypeBuilder(ABC):
    type_parsers: list[ITypeParser]

    @abstractmethod
    def build(self, t: type) -> tuple[Type, dict[str, Type]]:
        """
        Преобразует любой тип (класс) в обьект Type.
        :param t: тип данных
        :return: данные о типе и подтипах
        """


class IAnnotationBuilder(ABC):
    type_builder: ITypeBuilder

    @abstractmethod
    def build(self, t: type) -> tuple[Annotation, dict[str, Type]]:
        """
        Собирает аннотацию типа
        :param t: тип данных
        :return: данные об аннотации типа и всех типах внутри нее
        """
