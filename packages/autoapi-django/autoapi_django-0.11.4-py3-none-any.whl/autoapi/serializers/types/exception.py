import json

from autoapi.serializers.interface import ITypeSerializer
from autoapi.schema.data import Annotation


class ExceptionSerializer(ITypeSerializer):
    def check(self, annotation: Annotation):
        t = annotation.type.type
        return isinstance(t, type) and issubclass(t, BaseException)

    # def serialize(self, content: any, annotation: Annotation) -> any:
    #     if not isinstance(content, Exception)

    def deserialize(self, content: any, annotation: Annotation) -> any:
        if type(content) is str:
            content = json.loads(content)
        instance = annotation.type.type()
        if isinstance(content, dict):
            for key, value in content.items():
                setattr(instance, key, value)
        return instance
