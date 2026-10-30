"""LangChain's standard unit tests, for every Fokals tool."""

from __future__ import annotations

from langchain_tests.unit_tests import ToolsUnitTests

from langchain_fokals import ALL_TOOLS
from langchain_fokals._generated import EXAMPLES


def _suite(tool_class: type) -> type:
    example = EXAMPLES[tool_class.model_fields["name"].default]

    class Suite(ToolsUnitTests):
        @property
        def tool_constructor(self) -> type:
            return tool_class

        @property
        def tool_constructor_params(self) -> dict:
            return {"fokals_api_key": "test-key"}

        @property
        def tool_invoke_params_example(self) -> dict:
            return example

        @property
        def init_from_env_params(self) -> tuple[dict, dict, dict]:
            return {"FOKALS_API_KEY": "env-key"}, {}, {"fokals_api_key": "env-key"}

    Suite.__name__ = f"Test{tool_class.__name__}"
    Suite.__qualname__ = Suite.__name__
    return Suite


for _tool in ALL_TOOLS:
    _suite_class = _suite(_tool)
    globals()[_suite_class.__name__] = _suite_class
del _tool, _suite_class
