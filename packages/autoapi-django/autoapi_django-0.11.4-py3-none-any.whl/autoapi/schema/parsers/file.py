from django.core.files import File

from autoapi.schema.interfaces import ITypeParser
from autoapi.schema.data import Type


class DjangoFileParser(ITypeParser):

    def check(self, t: type) -> bool:
        return t is File

    def parse(self, t: type) -> tuple[Type, dict[str, Type]]:
        return Type(
            name='File',
            type=t,
            is_model=False,
            model_path=self._full_path(t),
        ), {}