from autoapi.serializers.interface import ITypeSerializer
from autoapi.schema.data import Annotation


class FloatSerializer(ITypeSerializer):
    def check(self, annotation: Annotation):
        return annotation.type.type is float

    def serialize(self, content: any, annotation: Annotation) -> float:
        if content is None:
            return content
        if type(content) not in (int, float):
            raise ValueError(f'Cannot serialize content = {content} as float!')
        return float(content)

    def deserialize(self, content: any, annotation: Annotation) -> float:
        if content is None:
            return content
        return float(content)
