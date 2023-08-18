from autoapi.schema.data import ServiceSchema, MethodSchema
from django.urls import path
from django.urls.resolvers import RoutePattern
from django.views import View

from autoapi.api.routes.django.base import BaseExecuteMethodDjangoView
from autoapi.api.routes.interface import IEndpointsGenerator


class HTTPEndpointsGenerator(IEndpointsGenerator):
    def generate_api(self, services: list[ServiceSchema]) -> list[RoutePattern]:
        result = []
        for service_schema in services:
            for method_schema in service_schema.methods:
                view: type = self._generate_endpoint(service_schema.cls, method_schema)
                view: View
                url = self.url_builder.build(service_schema, method_schema)
                route_name = self._build_route_name(service_schema, method_schema)
                route = path(url, view.as_view(), name=route_name)
                result.append(route)
        return result

    def _generate_endpoint(self, service_: type, schema_: MethodSchema) -> type:
        class ExecuteMethodDjangoView(BaseExecuteMethodDjangoView):
            service = service_
            schema = schema_
            auth = self.auth_provider
            deserializer = self.content_deserializer
            use_aio = self.settings.use_aio

        return ExecuteMethodDjangoView

    def _build_route_name(self, service_schema: ServiceSchema, method_schema: MethodSchema) -> str:
        return f'autoapi__{service_schema.name}__{method_schema.name}'
