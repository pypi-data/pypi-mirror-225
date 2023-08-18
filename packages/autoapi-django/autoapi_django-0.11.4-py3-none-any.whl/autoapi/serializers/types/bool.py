from autoapi.serializers.interface import ITypeSerializer
from autoapi.schema.data import Annotation


class BoolSerializer(ITypeSerializer):
    def check(self, annotation: Annotation) -> bool:
        return annotation.type.type is bool

    def serialize(self, content: any, annotation: Annotation) -> bool:
        if content is None:
            return content
        if not isinstance(content, bool):
            raise ValueError(f'Cannot serialize content = {content} as boolean!')
        return content

    def deserialize(self, content: any, annotation: Annotation) -> bool:
        if content is None:
            return content
        if not isinstance(content, bool):
            raise ValueError(f'Cannot deserialize content = {content} as boolean!')
        return content
