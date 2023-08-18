import datetime
from dateutil.parser import parse

from autoapi.serializers.interface import ITypeSerializer
from autoapi.schema.data import Annotation


class DateTimeSerializer(ITypeSerializer):
    def check(self, annotation: Annotation):
        return annotation.type.type is datetime.datetime

    def serialize(self, content: any, annotation: Annotation) -> str:
        if content is None:
            return content
        if not isinstance(content, datetime.datetime):
            raise ValueError(f'Cannot serialize content = {content} as datetime!')
        return str(content)

    def deserialize(self, content: any, annotation: Annotation) -> datetime.datetime:
        if content is None:
            return content
        return parse(content)
