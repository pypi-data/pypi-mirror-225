from autoapi.api.schema_presenter.openapi.properties.interface import IComponentBuilder
from autoapi.schema.data import Type, Annotation


class IntComponentBuilder(IComponentBuilder):

    def check(self, annotation: Annotation) -> bool:
        return annotation.type.type is int

    def parse(self, annotation: Annotation) -> dict:
        return {
            'type': 'number'
        }
