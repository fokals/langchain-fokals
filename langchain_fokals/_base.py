"""The base every Fokals tool shares: the key, the address and one HTTP call."""

from __future__ import annotations

import json
from typing import Any, Literal, Optional

import httpx
from langchain_core.callbacks import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain_core.tools import BaseTool, ToolException
from langchain_core.utils import secret_from_env
from pydantic import Field, PrivateAttr, SecretStr

from langchain_fokals._version import __version__

DEFAULT_BASE_URL = "https://api.fokals.com/v1"
USER_AGENT = f"langchain-fokals/{__version__}"


class FokalsBaseTool(BaseTool):
    """A Fokals API endpoint as a LangChain tool.

    The key is read from the ``FOKALS_API_KEY`` environment variable unless it is passed as
    ``fokals_api_key``. Make a key on your account page at https://www.fokals.com/account.

    Each call returns the API's own sentence about what it did, followed by the data as JSON.
    The data is also the tool message's artifact. A call that would cost more than the account
    lets run unasked is not an error: it returns its price, and the agent asks the person and
    calls again with ``max_usd``.
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
    """The Fokals key, from FOKALS_API_KEY unless given."""

    base_url: str = DEFAULT_BASE_URL
    """The API's address."""

    timeout: float = 60.0
    """Seconds to wait for an answer."""

    endpoint: str = ""
    """The endpoint this tool calls, as in POST {base_url}/{endpoint}."""

    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    handle_tool_error: bool = True

    # Where requests go instead of the network, in tests.
    _transport: Optional[httpx.BaseTransport] = PrivateAttr(default=None)
    _async_transport: Optional[httpx.AsyncBaseTransport] = PrivateAttr(default=None)

    def _request(self, kwargs: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
        body = {k: v for k, v in kwargs.items() if v is not None}
        headers = {
            "Authorization": f"Bearer {self.fokals_api_key.get_secret_value()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        return f"{self.base_url.rstrip('/')}/{self.endpoint}", json.dumps(body), headers

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any]]:
        url, body, headers = self._request(kwargs)
        try:
            with httpx.Client(timeout=self.timeout, transport=self._transport) as client:
                response = client.post(url, content=body, headers=headers)
        except httpx.HTTPError as e:
            raise ToolException(f"Fokals could not be reached: {e.__class__.__name__}.") from e
        return answer_of(response)

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any]]:
        url, body, headers = self._request(kwargs)
        try:
            async with httpx.AsyncClient(timeout=self.timeout, transport=self._async_transport) as client:
                response = await client.post(url, content=body, headers=headers)
        except httpx.HTTPError as e:
            raise ToolException(f"Fokals could not be reached: {e.__class__.__name__}.") from e
        return answer_of(response)


def answer_of(response: httpx.Response) -> tuple[str, dict[str, Any]]:
    """What a response is handed back as: content for the model and the data as artifact."""
    try:
        body = response.json()
    except ValueError:
        body = {}
    if not isinstance(body, dict):
        body = {}
    if response.status_code == 200:
        message = str(body.get("message", "")).strip()
        data = body.get("data") if isinstance(body.get("data"), dict) else {}
        return f"{message}\n{json.dumps(data, ensure_ascii=False)}".strip(), data
    error = body.get("error") if isinstance(body.get("error"), dict) else {}
    message = str(error.get("message") or f"Fokals answered {response.status_code}.")
    if response.status_code == 402:
        # The price, and what makes the call run: passed on for the agent to ask about.
        return message, dict(error)
    raise ToolException(message)
