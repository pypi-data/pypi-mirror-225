import inspect

from autoapi.schema.data import MethodSchema, Type, ParamSchema, ExceptionSchema
from autoapi.schema.interfaces import IMethodBuilder
from autoapi.schema.utils import get_docstring_description_lines, getkind, getdefault, all_classes


class MethodBuilder(IMethodBuilder):
    def build(self, method_name: str, method: callable) -> tuple[MethodSchema, dict[str, Type]]:
        description, params, return_description, raises = '', {}, '', {}
        if method.__doc__:
            description, params, return_description, raises = get_docstring_description_lines(method.__doc__)

        signature = inspect.signature(method)
        method_params = signature.parameters
        schema_params = []
        models = {}
        for param_name, param in method_params.items():
            if param_name == 'self':
                continue
            kind = getkind(param)
            default = getdefault(param)
            annotation_type, models_ = self.annotation_builder.build(param.annotation)
            models.update(**models_)
            param_description = params.get(param_name, '')
            schema_param = ParamSchema(
                name=param_name,
                kind=kind,
                default=default,
                annotation=annotation_type,
                description=param_description,
            )
            schema_params.append(schema_param)

        return_annotation = signature.return_annotation
        returns, models_ = self.annotation_builder.build(return_annotation)
        models.update(**models_)
        is_async = inspect.iscoroutinefunction(method)
        if is_async and not self.settings.use_aio:
            raise ValueError(f'Method "{method.__name__}" can not be async. \n'
                             f'Set config use_aio to True for use async methods')
        result_raises = []
        all_cls = all_classes()
        for exc_name, exc_description in raises.items():
            if exc_cls := all_cls.get(exc_name):
                model_type, models_ = self.type_builder.build(exc_cls)
                models[exc_name] = model_type
                models.update(models_)
                result_raises.append(ExceptionSchema(
                    name=exc_name,
                    description=exc_description,
                    cls=exc_cls,
                    type=model_type,
                ))
        schema = MethodSchema(
            name=method_name,
            params=schema_params,
            returns=returns,
            func=method,
            idempotency=method_name.startswith('get_'),
            is_async=is_async,
            description=description,
            return_description=return_description,
            raises=result_raises,
        )
        return schema, models
