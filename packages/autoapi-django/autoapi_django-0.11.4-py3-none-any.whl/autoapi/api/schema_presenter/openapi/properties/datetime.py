import datetime

from autoapi.api.schema_presenter.openapi.properties.interface import IComponentBuilder
from autoapi.schema.data import Type, Annotation


class DateTimeComponentBuilder(IComponentBuilder):

    def check(self, annotation: Annotation) -> bool:
        return annotation.type.type is datetime.datetime

    def parse(self, annotation: Annotation) -> dict:
        return {
            'type': 'string',
            'format': 'date-time'
        }
