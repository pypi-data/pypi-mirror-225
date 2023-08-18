from django.urls import path
from django.urls.resolvers import RoutePattern

from autoapi.api.http_explorer.interface import IExplorerGenerator
from autoapi.api.http_explorer.openapi_views import OpenAPIJsonView, SwaggerView
from autoapi.schema.data import Type, ServiceSchema


class Swagger(IExplorerGenerator):

    def endpoints(self, schemas: list[ServiceSchema], models: dict[str, Type]) -> list[RoutePattern]:
        schema_json = self.app_structure_serializer.present(schemas, models)
        explorer_url = self.settings.explorer_url
        if explorer_url[0] == '/':
            explorer_url = explorer_url[1:]
        return [
            path(explorer_url, SwaggerView.as_view(), name='Swagger'),
            path('openapi.json', self.generate_schema_view(schema_json).as_view(), name='OpenAPI'),
        ]

    def generate_schema_view(self, json: str) -> type:
        class CurrentSchemaView(OpenAPIJsonView):
            schema_json = json

        return CurrentSchemaView
