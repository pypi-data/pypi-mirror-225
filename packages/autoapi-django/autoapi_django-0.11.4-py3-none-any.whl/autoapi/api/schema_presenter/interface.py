from abc import ABC

from autoapi.api.schema_presenter.openapi.properties.interface import IComponentBuilder
from autoapi.api.routes.urls import IURLBuilder
from autoapi.schema.data import Type, ServiceSchema
from autoapi.settings import AutoAPISettings


class ISchemaPresenter(ABC):
    url_builder: IURLBuilder
    settings: AutoAPISettings
    components_properties_parsers: list[IComponentBuilder]

    def present(self, schemas: list[ServiceSchema], models: dict[str, Type]) -> str:
        """
        Сериализует структуру приложения
        """
