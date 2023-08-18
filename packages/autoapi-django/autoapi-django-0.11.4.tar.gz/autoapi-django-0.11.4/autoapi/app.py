from dataclasses import dataclass

from django.urls.resolvers import RoutePattern
from django.utils.module_loading import import_string

from autoapi.dependencies import AutoAPIContainer
from autoapi.schema.data import Type, ServiceSchema
from autoapi.settings import AutoAPISettings


@dataclass
class AutoAPI:
    services: list[str]

    settings: AutoAPISettings | dict = None
    container: AutoAPIContainer | dict = None

    schemas: dict[str, ServiceSchema] = None
    models: dict[str, Type] = None

    def __post_init__(self):
        if self.settings is None:
            self.settings = AutoAPISettings()
        elif isinstance(self.settings, dict):
            self.settings = AutoAPISettings(**self.settings)
        elif not isinstance(self.settings, AutoAPISettings):
            raise ValueError('Property "settings" must be an instance of AutoAPISettings, '
                             'or dict of constructor kwargs for them')

        if self.container is None:
            self.container = AutoAPIContainer()
        elif isinstance(self.container, dict):
            self.container = AutoAPIContainer(**self.container)
        elif not isinstance(self.container, AutoAPIContainer):
            raise ValueError('Property "container" must be an instance of AutoAPIContainer, '
                             'or dict of constructor kwargs for them')

        self.container.resolve(self.settings)
        self._init_schemas()

    def get_django_routes(self) -> list[RoutePattern]:
        services_schemas = list(self.schemas.values())
        methods_routes = self.container.endpoints_generator.generate_api(services_schemas)
        explorer_routes = self.container.explorer_views_generator.endpoints(services_schemas, self.models)
        return [*methods_routes, *explorer_routes]

    def _init_schemas(self):
        schemas = {}
        models = {}
        for service_name in self.services:
            service_cls = import_string(service_name)
            schema, models_ = self.container.service_builder.build(service_cls)
            schemas[service_name] = schema
            models.update(models_)
        self.schemas = schemas
        self.models = models
