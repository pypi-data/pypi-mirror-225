from dataclasses import dataclass, field
from typing import Callable, Optional, Union

from autoapi.schema.empty import Empty
from autoapi.schema.enums import ParamKind


@dataclass
class StringAnnotation:
    """
    Строковая аннотация
    """
    type: str


@dataclass
class TypeAnnotation:
    """
    Используется когда аннотация типа указана
    объектом из typing или типом данных
    """
    type: 'Type'
    is_generic: bool
    generic_annotations: list['Annotation']


Annotation = Union[StringAnnotation, TypeAnnotation]


@dataclass
class Type:
    name: str
    type: type
    is_model: bool
    model_fields: dict[str, Annotation] = field(default_factory=dict)
    model_path: str = field(default='')


@dataclass
class ServiceSchema:
    cls: type
    name: str
    methods: list['MethodSchema']
    description: str = ''


@dataclass
class MethodSchema:
    name: str
    params: list['ParamSchema']
    returns: Union[Empty, 'Annotation']
    raises: list['ExceptionSchema']
    func: Callable
    idempotency: bool
    is_async: bool
    description: str = ''
    return_description: str = ''

    def __repr_params(self) -> str:
        results = []
        for param in self.params:
            result = param.name
            if param.annotation:
                result += f': {param.annotation.type.name}'
            results.append(result)
        return ', '.join(results)

    def __str__(self):
        return f'{self.name}({self.__repr_params()}) -> {self.returns.type.name}'


@dataclass
class ParamSchema:
    name: str
    kind: ParamKind
    default: Union[Empty, any]
    annotation: Optional['Annotation']
    description: str = ''


@dataclass
class ExceptionSchema:
    name: str
    description: str
    cls: type
    type: Type
    is_generic: bool = False
