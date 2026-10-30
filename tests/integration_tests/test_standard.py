"""LangChain's standard integration tests against the live API.

They run only with FOKALS_API_KEY set, and only on the free tools, so they cost nothing.
"""

from __future__ import annotations

import os

import pytest
from langchain_tests.integration_tests import ToolsIntegrationTests

from langchain_fokals import (
    FokalsAccountBalance,
    FokalsCountCompanies,
    FokalsIdentifyCompany,
    FokalsListFilters,
)
from langchain_fokals._generated import EXAMPLES

pytestmark = pytest.mark.skipif(not os.environ.get("FOKALS_API_KEY"), reason="FOKALS_API_KEY is not set")


def _suite(tool_class: type) -> type:
    example = EXAMPLES[tool_class.model_fields["name"].default]

    class Suite(ToolsIntegrationTests):
        @property
        def tool_constructor(self) -> type:
            return tool_class

        @property
        def tool_constructor_params(self) -> dict:
            return {}

        @property
        def tool_invoke_params_example(self) -> dict:
            return example

    Suite.__name__ = f"Test{tool_class.__name__}Live"
    Suite.__qualname__ = Suite.__name__
    return Suite


for _tool in (FokalsIdentifyCompany, FokalsCountCompanies, FokalsListFilters, FokalsAccountBalance):
    _suite_class = _suite(_tool)
    globals()[_suite_class.__name__] = _suite_class
del _tool, _suite_class
