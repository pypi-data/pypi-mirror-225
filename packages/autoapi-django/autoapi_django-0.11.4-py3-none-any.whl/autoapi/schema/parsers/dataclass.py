from dataclasses import fields, is_dataclass
from typing import get_type_hints

from autoapi.schema.interfaces import ITypeParser
from autoapi.schema.data import Type


class DataclassParser(ITypeParser):
    def check(self, t: type) -> bool:
        return is_dataclass(t)

    def parse(self, t: type) -> tuple[Type, dict[str, Type]]:
        resolved_hints = get_type_hints(t)
        field_names = [field.name for field in fields(t)]
        dataclass_fields = {
            name: resolved_hints[name]
            for name in field_names
        }
        model_fields = {}
        models = {}
        for field_name, field_type in dataclass_fields.items():
            field_annotation, models_ = self.annotation_builder.build(field_type)
            model_fields[field_name] = field_annotation
            models.update(models_)
        return Type(
            name=t.__name__,
            type=t,
            is_model=True,
            model_fields=model_fields,
            model_path=self._full_path(t),
        ), models
