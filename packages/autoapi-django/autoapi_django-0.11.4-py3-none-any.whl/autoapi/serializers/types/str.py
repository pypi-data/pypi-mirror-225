from autoapi.serializers.interface import ITypeSerializer
from autoapi.schema.data import Annotation


class StrSerializer(ITypeSerializer):
    def check(self, annotation: Annotation):
        return annotation.type.type is str

    def serialize(self, content: any, annotation: Annotation) -> str:
        if content is None:
            return content
        if not isinstance(content, str):
            raise ValueError(f'Cannot serialize content = {content} as string!')
        return content

    def deserialize(self, content: any, annotation: Annotation) -> any:
        if content is None:
            return content
        return str(content)
