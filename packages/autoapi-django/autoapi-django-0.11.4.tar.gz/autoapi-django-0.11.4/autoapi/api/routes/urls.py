from abc import ABC

from autoapi.schema.data import ServiceSchema, MethodSchema


class IURLBuilder(ABC):
    def build(self, service_schema: ServiceSchema, method_schema: MethodSchema) -> str:
        """
        Собирает url метода
        """


class DefaultURLBuilder(IURLBuilder):
    def build(self, service_schema: ServiceSchema, method_schema: MethodSchema) -> str:
        return f'{service_schema.name}/{method_schema.name}/'
