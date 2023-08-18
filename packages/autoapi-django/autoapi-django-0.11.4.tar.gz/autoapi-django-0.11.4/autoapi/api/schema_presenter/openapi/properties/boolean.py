from autoapi.api.schema_presenter.openapi.properties.interface import IComponentBuilder
from autoapi.schema.data import Type, Annotation


class BooleanBuilder(IComponentBuilder):

    def check(self, annotation: Annotation) -> bool:
        return annotation.type.type is bool

    def parse(self, annotation: Annotation) -> dict:
        return {
            'type': 'boolean'
        }
