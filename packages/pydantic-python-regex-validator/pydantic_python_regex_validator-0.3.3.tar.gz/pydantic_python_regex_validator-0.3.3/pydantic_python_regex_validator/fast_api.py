"""Helper functions for fastapi."""
from platform import python_version
from typing import Optional, Type

from fastapi import Query
from fastapi.params import Body

from pydantic_python_regex_validator.regex import Regex

if python_version()[:3] == "3.8":
    from typing_extensions import Annotated
else:
    from typing import Annotated


def RegexQuery(  # noqa: N802
    pattern: str,
    allow_none: bool = False,  # noqa: FBT001, FBT002
    query_params: Optional[dict] = None,
) -> Type[str]:
    """Create a type that can enforce regex (using python) on a query string in fastapi.

    :param pattern: The pattern to be enforced.
    :param allow_none: Whether the string passed can be None
    :param query_params: Any kwargs to be passed to the query.
    :return: A type that fastapi can use to enforce regex patterns.
    """
    t = Optional[str] if allow_none else str
    q = query_params if query_params else {}
    return Annotated[t, Query(**q), Regex(pattern=pattern)]


def RegexBody(  # noqa: N802
    pattern: str,
    allow_none: bool = False,  # noqa: FBT001, FBT002
    body_params: Optional[dict] = None,
) -> Type[str]:
    """Create a type that can enforce regex (using python) on a body string in fastapi.

    :param pattern: The pattern to be enforced.
    :param allow_none:
    :param body_params: Any kwargs to be passed to the query.
    :return: A type that fastapi can use to enforce regex patterns.
    """
    if allow_none:
        ...
    b = body_params if body_params else {}
    return Annotated[str, Body(**b), Regex(pattern=pattern)]
