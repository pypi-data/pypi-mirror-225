from autoapi.schema.data import Type
from autoapi.schema.interfaces import ITypeBuilder


class TypeBuilder(ITypeBuilder):
    def build(self, t: type) -> tuple[Type, dict[str, Type]]:
        for parser in self.type_parsers:
            if parser.check(t):
                return parser.parse(t)
        raise ValueError(f'No builder found for type {t.__name__}')
