import json
from dataclasses import asdict, is_dataclass

from django.core.serializers import serialize
from django.db.models import Model

from autoapi.serializers.interface import ITypeSerializer
from autoapi.schema.data import Annotation
from autoapi.schema.empty import Empty


class ModelSerializer(ITypeSerializer):
    def check(self, annotation: Annotation):
        return annotation.type.is_model

    def serialize(self, content: any, annotation: Annotation) -> dict:
        if content is None:
            return None
        if is_dataclass(content):
            return asdict(content)
        if isinstance(content, Model):
            result = {}
            for field_name, field in annotation.type.model_fields.items():
                attr = getattr(content, field_name)
                result[field_name] = self.content_deserializer.serialize(attr, field)
            return result
        raise ValueError(f'Cannot serialize content = {content} as dictionary!')

    def deserialize(self, content: any, annotation: Annotation) -> any:
        if content is None:
            return content
        if isinstance(content, str):
            content: dict = json.loads(content)
        if not isinstance(content, dict):
            raise ValueError(f'Content {content} is not a dict')
        constructor_kwargs = {}
        for field_name, field in annotation.type.model_fields.items():
            field_content = content.get(field_name, Empty)
            if field_content is not Empty:
                constructor_kwargs[field_name] = self.content_deserializer.deserialize(field_content, field)
        return annotation.type.type(**constructor_kwargs)
