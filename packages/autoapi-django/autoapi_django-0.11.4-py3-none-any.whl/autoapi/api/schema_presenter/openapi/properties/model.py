from autoapi.api.schema_presenter.openapi.properties.interface import IComponentBuilder
from autoapi.schema.data import Type, Annotation


class DjangoModelComponentBuilder(IComponentBuilder):

    def check(self, annotation: Annotation) -> bool:
        return annotation.type.is_model

    def parse(self, annotation: Annotation) -> dict:
        return {
            '$ref': f'#/components/schemas/{annotation.type.name}',
        }
