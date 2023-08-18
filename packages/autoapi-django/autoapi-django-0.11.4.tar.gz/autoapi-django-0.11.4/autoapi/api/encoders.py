import json
from dataclasses import asdict, is_dataclass

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model, QuerySet


class JsonEncoder(DjangoJSONEncoder):

    def default(self, o):
        if isinstance(o, type):
            return f'<{o.__name__}>'
        if callable(o):
            return f'<{o.__name__}(...)>'
        if is_dataclass(o):
            return asdict(o)
        if isinstance(o, list) or isinstance(o, QuerySet):
            return [
                self.default(el) for el in o
            ]
        print('TYPE OF O', type(o))
        if isinstance(o, Model):
            model_dict = json.loads(serialize('json', [o]))[0]
            return {
                'id': model_dict['pk'],
                **model_dict['fields'],
            }
        return super().default(o)
