from abc import ABC, abstractmethod

from django.urls.resolvers import RoutePattern

from autoapi.api.schema_presenter.interface import ISchemaPresenter
from autoapi.schema.data import Type, ServiceSchema
from autoapi.settings import AutoAPISettings


class IExplorerGenerator(ABC):
    app_structure_serializer: ISchemaPresenter
    settings: AutoAPISettings

    @abstractmethod
    def endpoints(self, schemas: list[ServiceSchema], models: dict[str, Type]) -> list[RoutePattern]:
        """
        Генерирует массив RoutePattern'ов для HTTP API explorer'a
        Обычно там 2 ендпоинта: под схему (e.g. openapi.json)
        и под софт для просмотра (e.g. swagger).
        """

