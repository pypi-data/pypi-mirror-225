import json
from typing import List

from autoapi.serializers.interface import ITypeSerializer
from autoapi.schema.data import Annotation


class ListSerializer(ITypeSerializer):
    def check(self, annotation: Annotation):
        return annotation.type.type in (list, List)

    def serialize(self, content: any, annotation: Annotation) -> list:
        if content is None:
            return content
        if not isinstance(content, list):
            raise ValueError(f'Cannot serialize content = {content} as list!')
        return [
            self.content_deserializer.serialize(c, annotation.generic_annotations[0])
            for c in content
        ]

    def deserialize(self, content: any, annotation: Annotation) -> any:
        if content is None:
            return content
        if isinstance(content, str):
            content: list[any] = json.loads(content)
        if not isinstance(content, list):
            raise ValueError(f'Content {content} is not a list')
        return [
            self.content_deserializer.deserialize(data, annotation.generic_annotations[0])
            for data in content
        ]
