"""Write langchain_fokals/_generated.py from the Fokals OpenAPI document.

Each tool's name, description and arguments come from the API itself, so the package says
what the API does. Run it again when the API gains or changes a tool:

    python scripts/generate.py                      # reads https://api.fokals.com/v1/openapi.json
    python scripts/generate.py path/to/openapi.json # or a saved copy
"""

from __future__ import annotations

import json
import keyword
import re
import sys
import urllib.request
from pathlib import Path

OPENAPI_URL = "https://api.fokals.com/v1/openapi.json"
OUT = Path(__file__).resolve().parent.parent / "langchain_fokals" / "_generated.py"

# The tools an agent reads data with. Tools that change what an account holds (watches,
# files, funds, requests, reports) are left to the account page and the MCP server.
TOOLS = [
    "find_companies",
    "count_companies",
    "enrich_companies",
    "company_profile",
    "company_changes",
    "search_job_postings",
    "similar_companies",
    "company_connections",
    "identify_company",
    "market_breakdown",
    "vendor_scorecard",
    "companies_like_customers",
    "company_health",
    "likely_next",
    "list_filters",
    "account_balance",
]

# Prices change, so the package never states them. In their place, a paid tool says where
# they are and what to do when a call returns its price.
PAID_TAIL = (
    " Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices."
    " A call that costs more than the account lets run unasked returns its price instead:"
    " tell the person, then call again with max_usd once they agree."
)
MAX_DESCRIPTION = 1024


def load(source: str | None) -> dict:
    if source:
        return json.loads(Path(source).read_text(encoding="utf-8"))
    request = urllib.request.Request(OPENAPI_URL, headers={"User-Agent": "langchain-fokals-generate"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def camel(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


# Every endpoint the API has, filled in by main(): a description that names one is pointed at
# the tool's name here, and a sentence about one this package leaves out is dropped.
ALL_ENDPOINTS: list[str] = []


def rename(text: str) -> str:
    left_out = [e for e in ALL_ENDPOINTS if e not in TOOLS]
    if left_out:
        mention = re.compile(r"\b(" + "|".join(map(re.escape, left_out)) + r")\b")
        sentences = re.split(r"(?<=[.;])\s+", text.strip())
        text = " ".join(s for s in sentences if not mention.search(s))
    ours = re.compile(r"(?<!fokals_)\b(" + "|".join(map(re.escape, TOOLS)) + r")\b")
    return ours.sub(lambda m: "fokals_" + m.group(1), text)


def describe(text: str, paid: bool) -> str:
    text = rename(text)
    text = re.sub(r"\s*Costs \$.*$", "", text.strip(), flags=re.S)
    text = re.sub(r"\s*Free\.\s*$", "", text) if paid else text
    if paid:
        text += PAID_TAIL
    if len(text) > MAX_DESCRIPTION:
        # Drop whole sentences from the middle of the lead until it fits, keeping the tail.
        lead, tail = (text[: -len(PAID_TAIL)], PAID_TAIL) if paid else (text, "")
        sentences = re.split(r"(?<=\.)\s+", lead)
        # What each answer carries goes first (the answer shows it); then the last sentence.
        for i, s in enumerate(sentences):
            if len(" ".join(sentences) + tail) <= MAX_DESCRIPTION:
                break
            if s.startswith("Each company comes with"):
                sentences.pop(i)
        while len(" ".join(sentences) + tail) > MAX_DESCRIPTION and len(sentences) > 1:
            sentences.pop(-1)
        text = " ".join(sentences) + tail
    assert len(text) <= MAX_DESCRIPTION, (len(text), text)
    return text


# Models for objects inside an argument (a customer and the day it bought), written before
# the model that holds them.
NESTED: list[str] = []


def model_of(class_name: str, schema: dict, doc: str) -> list[str]:
    required = set(schema.get("required", []))
    lines = ["", "", f"class {class_name}(BaseModel):", f'    """{doc}"""', ""]
    lines.append('    model_config = ConfigDict(extra="forbid", populate_by_name=True)')
    props = schema.get("properties", {})
    if props:
        lines.append("")
    for prop, sub in props.items():
        lines.append(field(prop, sub, prop in required, f"{class_name}{camel(prop)}"))
    return lines


def py_type(schema: dict, nested_name: str = "Item") -> str:
    if "enum" in schema:
        return "Literal[" + ", ".join(json.dumps(v) for v in schema["enum"]) + "]"
    kind = schema.get("type")
    if kind == "object":
        NESTED.extend(model_of(nested_name, schema, schema.get("description", "One item.")))
        return nested_name
    if kind == "string":
        return "str"
    if kind == "integer":
        return "int"
    if kind == "number":
        return "float"
    if kind == "boolean":
        return "bool"
    if kind == "array":
        return f"list[{py_type(schema.get('items', {}), nested_name + 'Item')}]"
    raise ValueError(f"Unhandled schema: {schema}")


def field(name: str, schema: dict, required: bool, nested_name: str = "Item") -> str:
    args: list[str] = []
    if not required:
        args.append("default=None")
    limits = {
        "minLength": "min_length",
        "maxLength": "max_length",
        "minItems": "min_length",
        "maxItems": "max_length",
        "minimum": "ge",
        "maximum": "le",
        "exclusiveMinimum": "gt",
        "exclusiveMaximum": "lt",
        "pattern": "pattern",
    }
    for key, arg in limits.items():
        if key in schema:
            args.append(f"{arg}={schema[key]!r}")
    if "description" in schema:
        args.append(f"description={rename(schema['description'])!r}")
    kind = py_type(schema, nested_name)
    annotation = kind if required else f"Optional[{kind}]"
    attr = name + "_" if keyword.iskeyword(name) else name
    alias = f", alias={name!r}" if attr != name else ""
    return f"    {attr}: {annotation} = Field({', '.join(args)}{alias})"


def main() -> None:
    doc = load(sys.argv[1] if len(sys.argv) > 1 else None)
    ALL_ENDPOINTS[:] = [p.strip("/") for p, item in doc["paths"].items() if "post" in item]
    out = [
        '"""Written by scripts/generate.py from the Fokals OpenAPI document. Do not edit by hand."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Literal, Optional",
        "",
        "from pydantic import BaseModel, ConfigDict, Field",
        "",
        "from langchain_fokals._base import FokalsBaseTool",
        "",
        f"API_VERSION = {doc['info']['version']!r}",
    ]
    classes: list[str] = []
    examples: dict[str, dict] = {}
    for name in TOOLS:
        op = doc["paths"][f"/{name}"]["post"]
        body = op["requestBody"]["content"]["application/json"]
        schema = body["schema"]
        examples[f"fokals_{name}"] = body.get("example", {})
        model = f"{camel(name)}Input"
        NESTED.clear()
        lines = model_of(model, schema, f"Arguments of {name}.")
        out += NESTED + lines
        tool = f"Fokals{camel(name)}"
        classes.append(tool)
        description = describe(op["description"], bool(op.get("x-fokals-paid")))
        out += [
            "",
            "",
            f"class {tool}(FokalsBaseTool):",
            f'    """{op["summary"]}: the Fokals {name} endpoint as a LangChain tool."""',
            "",
            f"    name: str = {('fokals_' + name)!r}",
            f"    description: str = {description!r}",
            f"    args_schema: type[BaseModel] = {model}",
            f"    endpoint: str = {name!r}",
        ]
    out += ["", "", "ALL_TOOLS: tuple[type[FokalsBaseTool], ...] = (", *[f"    {c}," for c in classes], ")"]
    out += ["", "# The API's own example call for each tool, by tool name."]
    out += [f"EXAMPLES: dict[str, dict] = {examples!r}", ""]
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {len(classes)} tools to {OUT}")


if __name__ == "__main__":
    main()
