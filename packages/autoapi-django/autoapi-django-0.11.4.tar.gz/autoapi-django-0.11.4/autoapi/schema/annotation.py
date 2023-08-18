from types import GenericAlias
from typing import get_args

from autoapi.schema.data import Annotation, Type, StringAnnotation, TypeAnnotation
from autoapi.schema.interfaces import IAnnotationBuilder


class AnnotationBuilder(IAnnotationBuilder):
    def build(self, t: type) -> tuple[Annotation, dict[str, Type]]:
        if isinstance(t, str):
            return StringAnnotation(type=t), {}
        is_generic = isinstance(t, GenericAlias)
        models = {}
        if is_generic:
            annotation_type = t.__origin__
            generic_types = [*get_args(t)]
            generic_annotations = []
            for generic_type in generic_types:
                generic_annotation, models_ = self.build(generic_type)
                generic_annotations.append(generic_annotation)
                models.update(models_)
        else:
            annotation_type = t
            generic_annotations = []
        type_schema, models_ = self.type_builder.build(annotation_type)
        if type_schema.is_model:
            models[type_schema.model_path] = type_schema
        models.update(models_)
        return TypeAnnotation(
            type=type_schema,
            is_generic=is_generic,
            generic_annotations=generic_annotations,
        ), models
