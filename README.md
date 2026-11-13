# langchain-fokals

[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/fokals/langchain-fokals/badge)](https://scorecard.dev/viewer/?uri=github.com/fokals/langchain-fokals)

LangChain tools for [Fokals](https://www.fokals.com).

AI-powered company intelligence on how companies around the world grow, change and compete. Fokals derives advanced signals from company data, covering everything from technology and hiring to funding, buying intent and company health. Refreshed every day and brought together into a clear view of every market.

This package gives a LangChain agent that data as tools: find companies by what they show, enrich a list of accounts, profile one company in depth, follow what changed, and size a market.

## Install

```bash
pip install -U langchain-fokals
```

## Get a key

Sign up at [fokals.com](https://www.fokals.com/signup) and make a key on your [account page](https://www.fokals.com/account). Then set it:

```bash
export FOKALS_API_KEY="your-key"
```

Or pass it to a tool or the toolkit as `fokals_api_key`.

## Use it in an agent

With `langchain` and a model package installed (`pip install -U langchain langchain-anthropic`):

```python
from langchain.agents import create_agent
from langchain_fokals import FokalsToolkit

tools = FokalsToolkit().get_tools()
agent = create_agent("anthropic:claude-sonnet-5-5", tools)

result = agent.invoke({"messages": [{"role": "user", "content": "Which US companies running HubSpot are hiring now?"}]})
print(result["messages"][-1].content)
```

To give the agent only some tools, name them:

```python
tools = FokalsToolkit(include=["find_companies", "company_profile", "count_companies"]).get_tools()
```

## Call a tool directly

```python
from langchain_fokals import FokalsCompanyProfile

profile = FokalsCompanyProfile()
print(profile.invoke({"company": "stripe.com", "sections": ["technology", "hiring"]}))
```

Each tool returns the API's own sentence about what it did, followed by the data as JSON. Called with a tool call, the data is also the tool message's `artifact`.

## Tools

| Tool | What it does | Cost |
| --- | --- | --- |
| `fokals_find_companies` | Finds companies by a technology they run, a buying topic, hiring, an announcement, a project in their job ads, a pricing change, agent readiness, health, industry or country | Paid |
| `fokals_count_companies` | Counts the companies that match the same filters, and says what getting them would cost | Free |
| `fokals_enrich_companies` | Fills in your own list of companies, by website or name, up to 100 a call | Paid |
| `fokals_company_profile` | One company in depth: technologies and since when, open roles, buying topics, announcements, website changes, traffic, health and likely next technologies | Paid |
| `fokals_company_changes` | What is new at your companies since a date: website changes and announcements, in plain words | Paid |
| `fokals_search_job_postings` | Searches open job postings by title, function, seniority, country, work mode, technology and pay | Paid |
| `fokals_similar_companies` | Lookalikes of a company, or its competitors, with what they share | Paid |
| `fokals_company_connections` | The customers, partners, integrations and investors a company's website names, and who names it | Paid |
| `fokals_identify_company` | Which company a name or website address means | Free |
| `fokals_market_breakdown` | How a market divides by industry, country, technology, buying topic and more | Paid |
| `fokals_vendor_scorecard` | A technology vendor month by month: companies won and lost, churn, and the rivals they came from or moved to | Paid |
| `fokals_companies_like_customers` | Companies that look today the way your customers looked when they bought | Paid |
| `fokals_company_health` | A company's health this week, with the reasons | Paid |
| `fokals_likely_next` | The technologies a company is likeliest to add next | Paid |
| `fokals_intent_history` | The buying topics a company shows signs of, week by week, with the signals behind them | Paid |
| `fokals_sales_team` | The sales team a company's job ads show, by role, segment and country, with the pay they state | Paid |
| `fokals_funding_filings` | A company's notices of a private fundraise (Form D), with the amounts | Paid |
| `fokals_headcount_history` | How many people a company employed over the years | Paid |
| `fokals_traffic_history` | How popular a company's website has been, month by month | Paid |
| `fokals_signal_feed` | Every buying signal across all companies from a day on | Paid |
| `fokals_announcement_feed` | Every announcement across all companies from a day on | Paid |
| `fokals_change_feed` | Every website change across all companies from a day on | Paid |
| `fokals_listed_securities` | Stock listings with their identifiers and the company each belongs to | Paid |
| `fokals_market_trends` | How a measure of the market has moved over time, by industry, country, size or exchange | Paid |
| `fokals_market_movers` | The market figures that moved most on one day | Paid |
| `fokals_sales_pay_benchmarks` | Advertised sales pay by role and country | Paid |
| `fokals_list_filters` | The values the search tools filter by, the market measures and the sales roles | Free |
| `fokals_account_balance` | The balance, what this month has spent, and the prices | Free |

## Prices

Paid tools are charged from your prepaid Fokals balance at the prices on the [pricing page](https://www.fokals.com/pricing), also at [api.fokals.com/v1/prices](https://api.fokals.com/v1/prices). A company that is not found costs nothing.

A call that would cost more than your account lets run unasked does not run. It returns its price instead, and the tool passes that on to the agent: the agent tells the person, and when they agree it calls again with `max_usd`. This is a normal answer, not an error.

## Errors

A refused call (a bad argument, a key that is not valid, too many calls in a minute) reaches the agent as an error tool message in the API's own words, so the agent can correct itself. Set `handle_tool_error=False` on a tool to raise `ToolException` instead.

## Prefer MCP?

Fokals is also a remote MCP server at `https://mcp.fokals.com/mcp`, with the same account, balance and prices. Use it from LangChain with [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters). See [fokals.com/docs/connect](https://www.fokals.com/docs/connect).

## Development

The tools are written from the API's own OpenAPI document, so their names, descriptions and arguments match the API:

```bash
python scripts/generate.py
```

Tests:

```bash
pip install -e . --group test
pytest tests/unit_tests --disable-socket --allow-unix-socket
FOKALS_API_KEY=your-key pytest tests/integration_tests   # free tools only
```

## Licence

MIT
