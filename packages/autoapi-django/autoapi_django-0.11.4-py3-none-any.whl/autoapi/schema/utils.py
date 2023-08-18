import builtins
import inspect
import re
import sys
from typing import Union

from autoapi.schema.empty import Empty
from autoapi.schema.enums import ParamKind


def gettype(name: str) -> type:
    return builtins.getattr(builtins, name, None) or globals().get(name, None)


def getkind(param: inspect.Parameter) -> ParamKind:
    return ParamKind(param.kind.name)


def emptycheck(value: any) -> Union[Empty, any]:
    if value is inspect._empty:
        return Empty
    return value


def getdefault(param: inspect.Parameter) -> any:
    default = param.default
    default = emptycheck(default)
    return default


def as_snake_case(s: str) -> str:
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def resolve_service_name(name: str) -> str:
    return as_snake_case(name).replace('_service', '')

def get_tab_length(s: str) -> int:
    result = 0
    for ch in s:
        if ch == ' ':
            result += 1
        else:
            return result
    return result

def remove_spaces_from_begin(s: str) -> str:
    result = ''
    found = False
    for ch in s:
        if ch == ' ' and not found:
            continue
        found = True
        result += ch
    return result

def get_docstring_description_lines(docstring: str) -> tuple[str, dict[str, str], str, dict]:
    """
    Извлекает строки описания из докстринга
    """
    lines = docstring.split('\n')[1:]
    for line in lines:
        if not line:
            del line
    tab_length = get_tab_length(lines[0])
    result_lines = []
    result_params = {}
    result_errors = {}
    result_return = ''
    for line in lines:
        line = line[tab_length:]
        if ':param' in line:
            param_str = line.replace(':param ', '')
            param_name = param_str.split(':')[0].replace(' ', '')
            param_description = ''.join(param_str.split(': ')[1:])
            result_params[param_name] = param_description
        elif ':return:' in line:
            result_return = line.replace(':return:', '')
            if result_return.startswith(' '):
                result_return = result_return[1:]
        elif ':returns:' in line:
            result_return = line.replace(':returns:', '')
            if result_return.startswith(' '):
                result_return = result_return[1:]
        elif ':raise ' in line or ':raises ' in line:
            result_raise = line.replace(':raise ', '')
            result_raise = result_raise.replace(':raises ', '')
            while result_raise.startswith(' '):
                result_raise = result_raise[1:]
            result_raise_parts = result_raise.split(':')
            result_raise_exception_name = result_raise_parts[0]
            result_raise_description = ''.join(result_raise_parts[1:])
            while result_raise_exception_name.startswith(' '):
                result_raise_exception_name = result_raise_exception_name[1:]
            while result_raise_description.startswith(' '):
                result_raise_description = result_raise_description[1:]
            result_errors[result_raise_exception_name] = result_raise_description
        else:
            result_lines.append(line)
    return '\n'.join(result_lines), result_params, result_return, result_errors


def all_classes() -> dict[str, type]:
    all_members = {}
    modules = []
    items = sys.modules.values()
    for item in items:
        modules.append(item)
    for module in modules:
        try:
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    all_members[name] = obj
        except ModuleNotFoundError:
            continue
    return all_members
