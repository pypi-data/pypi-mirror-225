import datetime

from autoapi.api.schema_presenter.openapi.properties.interface import IComponentBuilder
from autoapi.schema.data import Type, Annotation


class DateComponentBuilder(IComponentBuilder):

    def check(self, annotation: Annotation) -> bool:
        return annotation.type.type is datetime.date

    def parse(self, annotation: Annotation) -> dict:
        return {
            'type': 'string',
            'format': 'date',
        }
