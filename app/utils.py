import random
import string
from typing import Any, Iterable, Type

ALPHA_NUM = string.ascii_uppercase + string.ascii_lowercase + string.digits


def generate_name(length: int = 20) -> str:
    return "".join(random.choices(ALPHA_NUM, k=length))


def pydantic_to_dict(objects: Type[Iterable]) -> Iterable[Any]:
    """Casts iterable of pydantic models to iterable of dicts."""

    cast_type = type(objects)  # e.g. list, tuple, set, etc.
    return cast_type(obj.dict() for obj in objects)
