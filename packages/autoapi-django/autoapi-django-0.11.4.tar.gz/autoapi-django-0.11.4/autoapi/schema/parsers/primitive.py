from inspect import _empty

from autoapi.schema.interfaces import ITypeParser
from autoapi.schema.data import Type

PRIMITIVE_TYPES = str, int, float, list, dict, bool, _empty, any


class PrimitiveParser(ITypeParser):
    def check(self, t: type) -> bool:
        return t in PRIMITIVE_TYPES

    def parse(self, t: type) -> tuple[Type, dict[str, Type]]:
        return Type(
            name=t.__name__,
            type=t,
            is_model=False,
        ), {}
