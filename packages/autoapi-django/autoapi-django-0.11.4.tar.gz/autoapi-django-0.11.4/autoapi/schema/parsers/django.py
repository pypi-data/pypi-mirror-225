import typing
import datetime

from django.core.files import File
from django.db.models import Model, Field

from autoapi.schema.interfaces import ITypeParser
from autoapi.schema.data import Type


class DjangoModelParser(ITypeParser):
    FIELDS_TYPES_MAPPING = {
        'AutoField': int,
        'BigAutoField': int,
        'DateTimeField': datetime.datetime,
        'DateField': datetime.date,
        'TimeField': datetime.time,
        'BooleanField': bool,
        'TextField': str,
        'CharField': str,
        'EmailField': str,
        'IntegerField': int,
        'FloatField': float,
        'ImageField': File,
        'FileField': File,
    }

    def check(self, t: type) -> bool:
        return isinstance(t, type) and issubclass(t, Model)

    def parse(self, t: typing.Type[Model]) -> tuple[Type, dict[str, Type]]:
        props = {}
        models = {}
        for field in t._meta.fields:
            field: Field
            field_name = type(field).__name__
            if field_name == 'ForeignKey':
                field_annotation, models_ = self.annotation_builder.build(field.related_model)
            else:
                field_type = self.FIELDS_TYPES_MAPPING[field_name]
                field_annotation, models_ = self.annotation_builder.build(field_type)
            props[field.name] = field_annotation
            models.update(models_)
        return Type(
            name=t.__name__,
            type=t,
            is_model=True,
            model_fields=props,
            model_path=self._full_path(t),
        ), models
