from django.core.files import File

from autoapi.serializers.interface import ISerializer
from autoapi.schema.data import Annotation


class Serializer(ISerializer):
    NOT_ALLOWED_TYPES = [
        File,
    ]

    def serialize(self, content: str | list | dict, annotation: Annotation) -> any:
        for not_allowed_type in self.NOT_ALLOWED_TYPES:
            if isinstance(content, not_allowed_type):
                return None
        if content is None:
            return None
        for parser in self.content_parsers:
            if parser.check(annotation):
                return parser.serialize(content, annotation)

        raise ValueError(f'Cannot serialize {annotation}: no parser :(')

    def deserialize(self, content: str | list | dict, annotation: Annotation) -> any:
        for parser in self.content_parsers:
            if parser.check(annotation):
                return parser.deserialize(content, annotation)

        raise ValueError(f'Cannot deserialize {annotation}: no parser :(')
