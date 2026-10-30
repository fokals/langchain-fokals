"""Every Fokals tool in one toolkit."""

from __future__ import annotations

from typing import Optional

from langchain_core.tools import BaseTool, BaseToolkit
from langchain_core.utils import secret_from_env
from pydantic import Field, SecretStr

from langchain_fokals._base import DEFAULT_BASE_URL
from langchain_fokals._generated import ALL_TOOLS


class FokalsToolkit(BaseToolkit):
    """Fokals company intelligence as LangChain tools.

    Setup:
        Install ``langchain-fokals`` and set ``FOKALS_API_KEY`` to a key from your account
        page at https://www.fokals.com/account.

        .. code-block:: bash

            pip install -U langchain-fokals
            export FOKALS_API_KEY="your-key"

    Instantiate:
        .. code-block:: python

            from langchain_fokals import FokalsToolkit

            toolkit = FokalsToolkit()
            tools = toolkit.get_tools()

        Pass ``include`` to keep only some tools, by tool name or endpoint:

        .. code-block:: python

            tools = FokalsToolkit(include=["find_companies", "company_profile"]).get_tools()
    """

    fokals_api_key: SecretStr = Field(
        default_factory=secret_from_env(
            "FOKALS_API_KEY",
            error_message=(
                "No Fokals key. Set FOKALS_API_KEY or pass fokals_api_key. "
                "Make a key on your account page at https://www.fokals.com/account."
            ),
        )
    )
    base_url: str = DEFAULT_BASE_URL
    timeout: float = 60.0
    include: Optional[list[str]] = None
    """Tool names (``fokals_find_companies``) or endpoints (``find_companies``) to keep."""

    def get_tools(self) -> list[BaseTool]:
        wanted = {n.removeprefix("fokals_") for n in self.include} if self.include else None
        tools: list[BaseTool] = []
        for cls in ALL_TOOLS:
            tool = cls(fokals_api_key=self.fokals_api_key, base_url=self.base_url, timeout=self.timeout)
            if wanted is None or tool.endpoint in wanted:
                tools.append(tool)
        if wanted is not None:
            unknown = wanted - {t.endpoint for t in tools}  # type: ignore[attr-defined]
            if unknown:
                raise ValueError(f"No Fokals tool called {', '.join(sorted(unknown))}.")
        return tools
