import inspect
from typing import Callable


def get_signature(func: Callable) -> inspect.FullArgSpec:
    return inspect.getfullargspec(func)
