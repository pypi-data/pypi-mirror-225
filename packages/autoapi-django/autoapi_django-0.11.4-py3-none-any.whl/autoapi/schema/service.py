import inspect
from types import FunctionType

from autoapi.schema.interfaces import IServiceBuilder
from autoapi.schema.data import Type, ServiceSchema
from autoapi.schema.utils import resolve_service_name, get_docstring_description_lines


class ServiceBuilder(IServiceBuilder):

    def build(self, service_cls: type) -> tuple[ServiceSchema, dict[str, Type]]:
        members = inspect.getmembers(service_cls)
        methods = []
        models = {}
        description = ''
        if service_cls.__doc__:
            description, params, return_description, raises = get_docstring_description_lines(service_cls.__doc__)
        for member_name, member in members:
            if isinstance(member, FunctionType):
                if member.__name__.startswith('_'):
                    continue
                func = getattr(service_cls(), member.__name__)
                method, models_ = self.method_builder.build(member_name, func)
                methods.append(method)
                models.update(models_)
        service_schema = ServiceSchema(
            name=resolve_service_name(service_cls.__name__),
            cls=service_cls,
            methods=methods,
            description=description,
        )
        return service_schema, models

