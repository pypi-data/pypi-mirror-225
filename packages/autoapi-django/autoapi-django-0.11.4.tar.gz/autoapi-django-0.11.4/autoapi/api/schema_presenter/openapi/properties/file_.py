from django.core.files import File

from autoapi.api.schema_presenter.openapi.properties.interface import IComponentBuilder
from autoapi.schema.data import Type, Annotation


class FileComponentBuilder(IComponentBuilder):

    def check(self, annotation: Annotation) -> bool:
        return annotation.type.type is File

    def parse(self, annotation: Annotation) -> dict:
        return {}
