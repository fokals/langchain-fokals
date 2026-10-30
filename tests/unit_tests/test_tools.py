"""What a Fokals tool sends, and what it hands back for each kind of answer."""

from __future__ import annotations

import json
import re

import httpx
import pytest
from langchain_core.messages import ToolMessage
from langchain_core.tools import ToolException

from langchain_fokals import (
    ALL_TOOLS,
    FokalsCompanyProfile,
    FokalsFindCompanies,
    FokalsToolkit,
    __version__,
)
from langchain_fokals._generated import EXAMPLES


def handler_for(status: int, body: dict, seen: list[httpx.Request]):
    def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(status, json=body)

    return handle


def tool_with(cls, status: int, body: dict, seen: list[httpx.Request]):
    tool = cls(fokals_api_key="test-key")
    tool._transport = httpx.MockTransport(handler_for(status, body, seen))
    tool._async_transport = httpx.MockTransport(handler_for(status, body, seen))
    return tool


ANSWER = {"message": "Found 2 companies.", "data": {"companies": [{"website": "acme.com"}], "next_cursor": None}}


def test_a_call_is_one_post_with_the_key_and_only_the_arguments_given() -> None:
    seen: list[httpx.Request] = []
    tool = tool_with(FokalsFindCompanies, 200, ANSWER, seen)
    tool.invoke({"technology": "HubSpot", "hiring": True})
    (request,) = seen
    assert request.method == "POST"
    assert str(request.url) == "https://api.fokals.com/v1/find_companies"
    assert request.headers["authorization"] == "Bearer test-key"
    assert request.headers["user-agent"] == f"langchain-fokals/{__version__}"
    assert json.loads(request.content) == {"technology": "HubSpot", "hiring": True}


def test_an_answer_is_its_sentence_then_its_data_and_the_data_is_the_artifact() -> None:
    seen: list[httpx.Request] = []
    tool = tool_with(FokalsFindCompanies, 200, ANSWER, seen)
    message = tool.invoke({"name": tool.name, "args": {"technology": "HubSpot"}, "id": "1", "type": "tool_call"})
    assert isinstance(message, ToolMessage)
    assert message.content.startswith("Found 2 companies.\n")
    assert json.loads(message.content.split("\n", 1)[1]) == ANSWER["data"]
    assert message.artifact == ANSWER["data"]
    assert message.status == "success"


async def test_the_async_call_answers_the_same() -> None:
    seen: list[httpx.Request] = []
    tool = tool_with(FokalsCompanyProfile, 200, ANSWER, seen)
    message = await tool.ainvoke({"name": tool.name, "args": {"company": "acme.com"}, "id": "1", "type": "tool_call"})
    assert message.artifact == ANSWER["data"]
    assert json.loads(seen[0].content) == {"company": "acme.com"}


def test_a_price_to_agree_to_is_passed_on_not_raised() -> None:
    price = {
        "error": {
            "code": "payment_required",
            "message": (
                "This call costs $4.00 for 100 companies. Tell the person the price, "
                "and when they agree call again with max_usd set to 4 or more."
            ),
            "reason": "approval",
            "cost_usd": 4,
        }
    }
    seen: list[httpx.Request] = []
    tool = tool_with(FokalsFindCompanies, 402, price, seen)
    message = tool.invoke({"name": tool.name, "args": {"technology": "HubSpot"}, "id": "1", "type": "tool_call"})
    assert message.status == "success"
    assert "max_usd" in message.content
    assert message.artifact["cost_usd"] == 4


@pytest.mark.parametrize("status", [400, 401, 422, 429, 500])
def test_a_refusal_reaches_the_agent_as_an_error_with_the_apis_words(status: int) -> None:
    body = {"error": {"code": "x", "message": f"Refused with {status}."}}
    seen: list[httpx.Request] = []
    tool = tool_with(FokalsFindCompanies, status, body, seen)
    message = tool.invoke({"name": tool.name, "args": {"technology": "HubSpot"}, "id": "1", "type": "tool_call"})
    assert message.status == "error"
    assert message.content == f"Refused with {status}."
    tool.handle_tool_error = False
    with pytest.raises(ToolException, match=f"Refused with {status}."):
        tool.invoke({"technology": "HubSpot"})


def test_an_answer_that_is_not_json_is_still_an_error_with_words() -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(502, text="Bad gateway")

    tool = FokalsFindCompanies(fokals_api_key="test-key", handle_tool_error=False)
    tool._transport = httpx.MockTransport(handle)
    with pytest.raises(ToolException, match="Fokals answered 502."):
        tool.invoke({"technology": "HubSpot"})


def test_no_key_says_where_to_make_one(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FOKALS_API_KEY", raising=False)
    with pytest.raises(ValueError, match="fokals.com/account"):
        FokalsFindCompanies()
    with pytest.raises(ValueError, match="fokals.com/account"):
        FokalsToolkit()


def test_the_key_is_never_shown() -> None:
    tool = FokalsFindCompanies(fokals_api_key="secret-key")
    assert "secret-key" not in repr(tool)
    assert "secret-key" not in str(tool.model_dump())


def test_the_toolkit_holds_every_tool_or_the_ones_named() -> None:
    toolkit = FokalsToolkit(fokals_api_key="test-key", base_url="https://example.test/v1")
    tools = toolkit.get_tools()
    assert [type(t) for t in tools] == list(ALL_TOOLS)
    assert all(t.base_url == "https://example.test/v1" for t in tools)
    assert all(t.fokals_api_key.get_secret_value() == "test-key" for t in tools)
    some = FokalsToolkit(fokals_api_key="k", include=["find_companies", "fokals_company_profile"]).get_tools()
    assert [t.name for t in some] == ["fokals_find_companies", "fokals_company_profile"]
    with pytest.raises(ValueError, match="No Fokals tool called nothing_here"):
        FokalsToolkit(fokals_api_key="k", include=["nothing_here"]).get_tools()


def test_every_tool_fits_what_chat_models_accept_and_states_no_price() -> None:
    names = {t.model_fields["name"].default for t in ALL_TOOLS}
    for cls in ALL_TOOLS:
        tool = cls(fokals_api_key="k")
        assert re.fullmatch(r"fokals_[a-z_]+", tool.name)
        assert 0 < len(tool.description) <= 1024, tool.name
        # Prices change: the package points to them and never states one.
        assert not re.search(r"\$\d", tool.description), tool.name
        # Another tool is named by its name here.
        for other in re.findall(r"\bfokals_[a-z_]+\b", tool.description):
            assert other in names, (tool.name, other)
        assert tool.name in EXAMPLES
