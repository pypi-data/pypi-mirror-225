import datetime

from autoapi.serializers.interface import ITypeSerializer
from autoapi.schema.data import Annotation


class TimeSerializer(ITypeSerializer):
    def check(self, annotation: Annotation):
        return annotation.type.type is datetime.time

    def serialize(self, content: any, annotation: Annotation) -> datetime.time:
        if content is None:
            return content
        if not isinstance(content, datetime.time):
            raise ValueError(f'Cannot serialize content = {content} as datetime.time!')
        return content

    def deserialize(self, content: any, annotation: Annotation) -> any:
        if content is None:
            return content
        return datetime.time.fromisoformat(content)
