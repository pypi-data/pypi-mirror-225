import datetime

from typing import get_type_hints

from autoapi.schema.interfaces import ITypeParser
from autoapi.schema.data import Type


class TimeParser(ITypeParser):
    def check(self, t: type) -> bool:
        return t is datetime.time

    def parse(self, t: type) -> tuple[Type, dict[str, Type]]:
        return Type(
            name=t.__name__,
            type=t,
            is_model=False,
            model_fields=dict(),
            model_path=""
        ), tuple()
