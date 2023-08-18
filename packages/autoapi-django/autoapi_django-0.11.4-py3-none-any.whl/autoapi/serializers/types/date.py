import datetime

from autoapi.serializers.interface import ITypeSerializer
from autoapi.schema.data import Annotation


class DateSerializer(ITypeSerializer):
    def check(self, annotation: Annotation):
        return annotation.type.type is datetime.date

    def serialize(self, content: any, annotation: Annotation) -> str:
        if content is None:
            return content
        if not isinstance(content, datetime.date):
            raise ValueError(f'Cannot serialize content = {content} as date!')
        return str(content)

    def deserialize(self, content: any, annotation: Annotation) -> datetime.date:
        if content is None:
            return content
        return datetime.date.fromisoformat(content)
