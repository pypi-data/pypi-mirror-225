from django.core.files import File

from autoapi.serializers.interface import ITypeSerializer
from autoapi.schema.data import Annotation


class FileSerializer(ITypeSerializer):
    def check(self, annotation: Annotation):
        return annotation.type.type is File

    def serialize(self, content: any, annotation: Annotation) -> File:
        return content

    def deserialize(self, content: any, annotation: Annotation) -> None:
        return None
