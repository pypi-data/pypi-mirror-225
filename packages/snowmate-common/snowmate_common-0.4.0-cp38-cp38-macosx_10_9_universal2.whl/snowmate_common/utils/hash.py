import ast
import hashlib
import inspect
import textwrap
from typing import Callable, List

import astor

cached_hashes = {}


def _get_node_body_without_docstrings(node_body: List[ast.AST]) -> List[ast.AST]:
    return [
        node_body_element
        for node_body_element in node_body
        if not isinstance(node_body_element, ast.Expr)
        or not isinstance(node_body_element.value, ast.Str)
    ]


def get_hash(function_object: Callable, full_name: str = None) -> str:
    """
    Returns the hash of the code of the function, ignoring whitespace, comments and docstrings.

    Args:function_object: a callable object (function, method, etc.)

    Returns: A string representing the hash of the code of the function.
    """
    # In the runner, we copy the function to a different file which causes a change in the qualname.
    # So we need to use the full name of the function instead.
    cache_full_name = function_object.__qualname__ if full_name is None else full_name
    if cached_hashes.get(cache_full_name):
        return cached_hashes[cache_full_name]
    source_code = textwrap.dedent(inspect.getsource(function_object))
    ast_source_code_object = ast.parse(source_code)

    # Remove docstrings from the AST.
    for ast_node in ast.iter_child_nodes(ast_source_code_object):
        if isinstance(ast_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ast_node.decorator_list = []
            ast_node.returns = None
            ast_node.body = _get_node_body_without_docstrings(ast_node.body)

    code_without_docstrings = astor.to_source(ast_source_code_object)
    function_hash = hashlib.md5(code_without_docstrings.encode()).hexdigest()
    cached_hashes[cache_full_name] = function_hash
    return function_hash
