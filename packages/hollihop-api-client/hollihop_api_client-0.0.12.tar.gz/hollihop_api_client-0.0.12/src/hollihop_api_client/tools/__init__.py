import phonenumbers
from functools import lru_cache
from typing import Any
import logging

keyword_tuple = ('False', 'await', 'else', 'import', 'pass',
                 'None', 'break', 'except', 'in', 'raise',
                 'True', 'class', 'finally', 'is', 'return',
                 'and', 'continue', 'for', 'lambda', 'try',
                 'as', 'def', 'from', 'nonlocal', 'while',
                 'assert', 'del', 'global', 'not', 'with',
                 'async', 'elif', 'if', 'or', 'yield',
                 )


def dict_to_camel(data: dict[Any, Any]) -> dict[Any, Any]:
    converted: dict[Any, Any] = {}
    for k, v in data.items():
        if isinstance(k, str):
            key = to_camel(k)
        else:
            key = k

        if isinstance(v, dict):
            converted[key] = dict_to_camel(v)
        elif isinstance(v, list):
            converted[key] = [dict_to_camel(
                x) if isinstance(x, dict) else x for x in v]
        elif isinstance(v, tuple):
            converted[key] = tuple(dict_to_camel(
                x) if isinstance(x, dict) else x for x in v)
        else:
            converted[key] = data[k]

    return converted


def dict_to_snake(data: dict[Any, Any]) -> dict[Any, Any]:
    converted: dict[Any, Any] = {}
    for k, v in data.items():
        if isinstance(k, str):
            if k.lower() in keyword_tuple:
                key = k.capitalize()
            elif 'EMail' in k:
                key = to_snake(k.replace('EMail', 'Email'))
            else:
                key = to_snake(k)
        else:
            key = k

        if isinstance(v, dict):
            converted[key] = dict_to_snake(v)
        elif isinstance(v, list):
            converted[key] = [dict_to_snake(
                x) if isinstance(x, dict) else x for x in v]
        elif isinstance(v, tuple):
            converted[key] = tuple(dict_to_snake(
                x) if isinstance(x, dict) else x for x in v)
        else:
            converted[key] = data[k]

    return converted


def dict_to_pascal(data: dict[Any, Any]) -> dict[Any, Any]:
    converted: dict[Any, Any] = {}
    for k, v in data.items():
        if isinstance(k, str):
            key = to_pascal(k)
        else:
            key = k

        if isinstance(v, dict):
            converted[key] = dict_to_pascal(v)
        elif isinstance(v, list):
            converted[key] = [dict_to_pascal(
                x) if isinstance(x, dict) else x for x in v]
        elif isinstance(v, tuple):
            converted[key] = tuple(dict_to_pascal(
                x) if isinstance(x, dict) else x for x in v)
        else:
            converted[key] = data[k]

    return converted


@lru_cache(maxsize=4096)
def to_camel(snake_string: str) -> str:
    words = _split_snake(snake_string)

    return words[0] + "".join(word.title() for word in words[1:])


@lru_cache(maxsize=4096)
def to_snake(camel_string: str) -> str:
    return "".join([f"_{c}" if c.isupper() else c for c in camel_string]).lstrip("_").lower()


@lru_cache(maxsize=4096)
def to_pascal(snake_string: str) -> str:
    words = _split_snake(snake_string)

    return "".join(word.title() for word in words)


def _split_snake(snake_string: str) -> list[str]:
    return snake_string.split("_")


def format_phone(phone: str) -> str:
    try:
        return phonenumbers.format_number(
            phonenumbers.parse(phone, 'RU'),
            phonenumbers.PhoneNumberFormat.E164
        )
    except Exception as error:
        logging.error(
            'Number is not formatted\nError – {error}'.format(error=error))
        return phone
