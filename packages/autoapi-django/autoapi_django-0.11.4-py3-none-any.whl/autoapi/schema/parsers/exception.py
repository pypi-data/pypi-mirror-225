import typing

from autoapi.schema.interfaces import ITypeParser
from autoapi.schema.data import Type


class ExceptionParser(ITypeParser):
    def check(self, t: type) -> bool:
        return isinstance(t, type) and issubclass(t, BaseException)

    def parse(self, t: typing.Type[BaseException]) -> tuple[Type, dict[str, Type]]:
        props = {}
        models = {}
        for field_name in dir(t):
            if field_name.startswith('_') or callable(getattr(t, field_name)):
                continue
            annotations = getattr(t, '__annotations__', {})
            field_type = annotations.get(field_name, any)
            field_annotation, models_ = self.annotation_builder.build(field_type)
            props[field_name] = field_annotation
            models.update(models_)
        return Type(
            name=t.__name__,
            type=t,
            is_model=True,
            model_fields=props,
            model_path=self._full_path(t),
        ), models