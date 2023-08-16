"""Main logic module for the Python Regex class."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from pydantic_core import CoreSchema, PydanticCustomError, core_schema

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
    from pydantic.json_schema import JsonSchemaValue


@dataclass
class Regex:
    """A python regex validator for pydantic using python regex.

    Due to changes made in pydantic V2, some support is lost for regex
    validation, namely using look around. This is taken directly from their
    docs as a workaround to use these features by invoking python's regex.
    """

    pattern: str
    allow_none: bool = False

    def __get_pydantic_core_schema__(
        self: Regex,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Tells pydantic how to handle the validation.

        We define a match function that's used for validating against the object passed in.
        """
        regex = re.compile(self.pattern)

        def match(v: str | None) -> str | None:
            if v is None and self.allow_none:
                return v

            if not regex.match(v):
                msg = "string_pattern_mismatch"
                raise PydanticCustomError(
                    msg,
                    "String should match pattern '{pattern}'",
                    {"pattern": self.pattern},
                )
            return v

        return core_schema.no_info_after_validator_function(
            match,
            handler(source_type),
        )

    def __get_pydantic_json_schema__(
        self: Regex,
        core_schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        """By overriding __get_pydantic_json_schema__, the pattern is visible in the json schema."""
        json_schema = handler(core_schema)
        json_schema["pattern"] = self.pattern
        return json_schema
