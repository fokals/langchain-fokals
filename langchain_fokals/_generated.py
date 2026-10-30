"""Written by scripts/generate.py from the Fokals OpenAPI document. Do not edit by hand."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from langchain_fokals._base import FokalsBaseTool

API_VERSION = "v1"


class FindCompaniesInput(BaseModel):
    """Arguments of find_companies."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    technology: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='A technology the company runs on its website, by name: "Shopify", "HubSpot". The stance a website states towards AI is found the same way: "Blocks GPTBot (OpenAI)", "llms.txt for AI assistants", "WebMCP tools for AI agents".',
    )
    buying_topic: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='A buying topic the company shows signs of, by name or id: "Marketing automation". fokals_list_filters with kind buying_topics has them all.',
    )
    hiring: Optional[bool] = Field(default=None, description="true keeps only companies with open roles now.")
    industry: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=60,
        description="One of: fashion_apparel, beauty_personal_care, health_wellness, food_beverage, home_garden, consumer_electronics, software_saas, finance_insurance, education, travel_hospitality, automotive, real_estate, entertainment_media, gaming, sports_outdoors, retail_marketplace, professional_services, telecom_utilities, nonprofit_public, pets, other.",
    )
    business_model: Optional[str] = Field(
        default=None, min_length=1, max_length=20, description="One of: b2b, b2c, both."
    )
    country: Optional[str] = Field(
        default=None,
        pattern="^[A-Za-z]{2}$",
        description="A country as a two-letter code: US, GB, DE. Matches the head office's country where it is known, otherwise the main market the company's website serves: country and market_country in an answer.",
    )
    listed: Optional[bool] = Field(
        default=None, description="true keeps only companies with a stock exchange listing, their own or a parent's."
    )
    changed_since: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}-\\d{2}-\\d{2}$",
        description="Keeps only companies whose website changed on or after this date, YYYY-MM-DD.",
    )
    region: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=60,
        description='The state or province of the head office: "CA", "Ontario". Held where a filing or the company\'s own website gives it.',
    )
    sic: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}$",
        description="A four-digit SIC industry code. Held for companies that file with the SEC.",
    )
    announcement: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=40,
        description="A type of announcement the company made lately. One of: product_launch, partnership, acquisition_made, acquired_or_merged, funding_round, leadership_change, layoffs_restructuring, expansion, incident, financial_results, award_or_recognition, regulatory_or_legal.",
    )
    announced_since: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}-\\d{2}-\\d{2}$",
        description="With announcement: made on or after this date, YYYY-MM-DD. 30 days ago unless given.",
    )
    name_contains: Optional[str] = Field(
        default=None, min_length=2, max_length=80, description="Text the company's name or website address holds."
    )
    agent_ready_min: Optional[int] = Field(
        default=None,
        ge=50,
        le=100,
        description="Keeps only companies whose agent readiness score is at least this, from 50 to 100. The score, from 0 to 100, says how ready a company's website is for AI agents: to be found, to show its prices, to sell and to be acted on.",
    )
    agent_ready_part: Optional[Literal["find", "price", "buy", "act"]] = Field(
        default=None,
        description="One of the four parts of agent readiness that must be strong: find, price, buy or act. With agent_ready_min, or alone for a score of 50 or more.",
    )
    agent_ready_part_min: Optional[int] = Field(
        default=None,
        ge=1,
        le=25,
        description="With agent_ready_part: the least points of its 25 that part holds. 15 unless given.",
    )
    project: Optional[Literal["migration", "first_team", "compliance", "expansion", "ai_build"]] = Field(
        default=None,
        description="A project the company's job ads state: migration (a move from one system to another), first_team (the first team of a function), compliance (work towards a certification), expansion (into a new country or region), ai_build (building an AI product).",
    )
    project_detail: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='With project, what narrows it. migration: a system by name, on either side ("Salesforce"), or "to HubSpot", "from Salesforce", "Salesforce to HubSpot". first_team: a job function (data_analytics, sales). compliance: soc2, iso27001, hipaa, pci, fedramp, gdpr. expansion: a two-letter country code or a region (europe, dach). ai_build: agents, llm, ml, ai.',
    )
    project_days: Optional[int] = Field(
        default=None,
        ge=7,
        le=365,
        description="With project: stated in job ads on a board in the last this many days. 90 unless given.",
    )
    price_change: Optional[
        Literal[
            "price_raised", "price_cut", "free_plan_removed", "free_plan_added", "usage_pricing_added", "ai_addon_added"
        ]
    ] = Field(
        default=None,
        description="A change the company's pricing page showed lately: price_raised, price_cut, free_plan_removed, free_plan_added, usage_pricing_added, ai_addon_added.",
    )
    price_changed_since: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}-\\d{2}-\\d{2}$",
        description="With price_change: on or after this date, YYYY-MM-DD. 90 days ago unless given.",
    )
    health_band: Optional[Literal["distress", "watch", "growing", "breakout"]] = Field(
        default=None,
        description="The company's health in the latest week: distress (signs of distress), watch (worth watching), growing or breakout (breaking out).",
    )
    shift: Optional[Literal["upmarket", "downmarket", "ai_pivot", "new_buyer", "price_up", "price_down"]] = Field(
        default=None,
        description="A shift in positioning the company shows in the latest week: upmarket, downmarket, ai_pivot (turning to AI), new_buyer (selling to a new buyer), price_up or price_down.",
    )
    limit: Optional[int] = Field(
        default=None, ge=1, le=1000, description="How many companies to return. 25 unless given."
    )
    cursor: Optional[str] = Field(
        default=None, max_length=2000, description="next_cursor of the answer before, to carry on where it ended."
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsFindCompanies(FokalsBaseTool):
    """Find companies by signal: the Fokals find_companies endpoint as a LangChain tool."""

    name: str = "fokals_find_companies"
    description: str = "Finds companies by what they show: a technology they run, a buying topic they show signs of, whether they are hiring, an announcement they made lately (funding, a launch, a partnership, a leadership change), a project their job ads state (a migration, a first team, a certification, an expansion, an AI build), a change on their pricing page, how ready their website is for AI agents, their health this week (a band, or a shift in positioning), their industry, business model or country, and how lately their website changed. The companies whose website changed most lately come first. Give at least one filter; fokals_count_companies says how many match, free, before this is called. At most 100 companies a call. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree."
    args_schema: type[BaseModel] = FindCompaniesInput
    endpoint: str = "find_companies"


class CountCompaniesInput(BaseModel):
    """Arguments of count_companies."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    technology: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='A technology the company runs on its website, by name: "Shopify", "HubSpot". The stance a website states towards AI is found the same way: "Blocks GPTBot (OpenAI)", "llms.txt for AI assistants", "WebMCP tools for AI agents".',
    )
    buying_topic: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='A buying topic the company shows signs of, by name or id: "Marketing automation". fokals_list_filters with kind buying_topics has them all.',
    )
    hiring: Optional[bool] = Field(default=None, description="true keeps only companies with open roles now.")
    industry: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=60,
        description="One of: fashion_apparel, beauty_personal_care, health_wellness, food_beverage, home_garden, consumer_electronics, software_saas, finance_insurance, education, travel_hospitality, automotive, real_estate, entertainment_media, gaming, sports_outdoors, retail_marketplace, professional_services, telecom_utilities, nonprofit_public, pets, other.",
    )
    business_model: Optional[str] = Field(
        default=None, min_length=1, max_length=20, description="One of: b2b, b2c, both."
    )
    country: Optional[str] = Field(
        default=None,
        pattern="^[A-Za-z]{2}$",
        description="A country as a two-letter code: US, GB, DE. Matches the head office's country where it is known, otherwise the main market the company's website serves: country and market_country in an answer.",
    )
    listed: Optional[bool] = Field(
        default=None, description="true keeps only companies with a stock exchange listing, their own or a parent's."
    )
    changed_since: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}-\\d{2}-\\d{2}$",
        description="Keeps only companies whose website changed on or after this date, YYYY-MM-DD.",
    )
    region: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=60,
        description='The state or province of the head office: "CA", "Ontario". Held where a filing or the company\'s own website gives it.',
    )
    sic: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}$",
        description="A four-digit SIC industry code. Held for companies that file with the SEC.",
    )
    announcement: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=40,
        description="A type of announcement the company made lately. One of: product_launch, partnership, acquisition_made, acquired_or_merged, funding_round, leadership_change, layoffs_restructuring, expansion, incident, financial_results, award_or_recognition, regulatory_or_legal.",
    )
    announced_since: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}-\\d{2}-\\d{2}$",
        description="With announcement: made on or after this date, YYYY-MM-DD. 30 days ago unless given.",
    )
    name_contains: Optional[str] = Field(
        default=None, min_length=2, max_length=80, description="Text the company's name or website address holds."
    )
    agent_ready_min: Optional[int] = Field(
        default=None,
        ge=50,
        le=100,
        description="Keeps only companies whose agent readiness score is at least this, from 50 to 100. The score, from 0 to 100, says how ready a company's website is for AI agents: to be found, to show its prices, to sell and to be acted on.",
    )
    agent_ready_part: Optional[Literal["find", "price", "buy", "act"]] = Field(
        default=None,
        description="One of the four parts of agent readiness that must be strong: find, price, buy or act. With agent_ready_min, or alone for a score of 50 or more.",
    )
    agent_ready_part_min: Optional[int] = Field(
        default=None,
        ge=1,
        le=25,
        description="With agent_ready_part: the least points of its 25 that part holds. 15 unless given.",
    )
    project: Optional[Literal["migration", "first_team", "compliance", "expansion", "ai_build"]] = Field(
        default=None,
        description="A project the company's job ads state: migration (a move from one system to another), first_team (the first team of a function), compliance (work towards a certification), expansion (into a new country or region), ai_build (building an AI product).",
    )
    project_detail: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='With project, what narrows it. migration: a system by name, on either side ("Salesforce"), or "to HubSpot", "from Salesforce", "Salesforce to HubSpot". first_team: a job function (data_analytics, sales). compliance: soc2, iso27001, hipaa, pci, fedramp, gdpr. expansion: a two-letter country code or a region (europe, dach). ai_build: agents, llm, ml, ai.',
    )
    project_days: Optional[int] = Field(
        default=None,
        ge=7,
        le=365,
        description="With project: stated in job ads on a board in the last this many days. 90 unless given.",
    )
    price_change: Optional[
        Literal[
            "price_raised", "price_cut", "free_plan_removed", "free_plan_added", "usage_pricing_added", "ai_addon_added"
        ]
    ] = Field(
        default=None,
        description="A change the company's pricing page showed lately: price_raised, price_cut, free_plan_removed, free_plan_added, usage_pricing_added, ai_addon_added.",
    )
    price_changed_since: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}-\\d{2}-\\d{2}$",
        description="With price_change: on or after this date, YYYY-MM-DD. 90 days ago unless given.",
    )
    health_band: Optional[Literal["distress", "watch", "growing", "breakout"]] = Field(
        default=None,
        description="The company's health in the latest week: distress (signs of distress), watch (worth watching), growing or breakout (breaking out).",
    )
    shift: Optional[Literal["upmarket", "downmarket", "ai_pivot", "new_buyer", "price_up", "price_down"]] = Field(
        default=None,
        description="A shift in positioning the company shows in the latest week: upmarket, downmarket, ai_pivot (turning to AI), new_buyer (selling to a new buyer), price_up or price_down.",
    )


class FokalsCountCompanies(FokalsBaseTool):
    """Count companies: the Fokals count_companies endpoint as a LangChain tool."""

    name: str = "fokals_count_companies"
    description: str = "Counts the companies that match a set of filters, and says what it would cost to get them. Free. Takes the same filters as fokals_find_companies. Use it before fokals_find_companies, so the person knows the size and the price of what they are asking for."
    args_schema: type[BaseModel] = CountCompaniesInput
    endpoint: str = "count_companies"


class EnrichCompaniesInput(BaseModel):
    """Arguments of enrich_companies."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    companies: list[str] = Field(
        min_length=1,
        max_length=1000,
        description='The person\'s own companies, each as a website address ("acme.com"), a name ("Acme Inc") or an id from an earlier answer.',
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsEnrichCompanies(FokalsBaseTool):
    """Enrich a list of companies: the Fokals enrich_companies endpoint as a LangChain tool."""

    name: str = "fokals_enrich_companies"
    description: str = "Takes the person's own list of companies, by website address or name, and returns what is held on each: industry and business model, the technologies its website runs, open roles and hiring in the last 30 days, buying topics it shows signs of, its agent readiness score, the projects its job ads state, its health band this week, and when its website last changed. Use it to fill in, score or rank a list of accounts, leads or customers. A website address finds a company more surely than a name. At most 100 companies a call; send a longer list in parts. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree."
    args_schema: type[BaseModel] = EnrichCompaniesInput
    endpoint: str = "enrich_companies"


class CompanyProfileInput(BaseModel):
    """Arguments of company_profile."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    company: str = Field(
        min_length=1,
        max_length=200,
        description='The company, as a website address ("acme.com"), a name or an id from an earlier answer.',
    )
    sections: Optional[
        list[
            Literal[
                "technology",
                "hiring",
                "buying_topics",
                "announcements",
                "changes",
                "traffic",
                "agent_readiness",
                "projects",
                "internal_tools",
                "health",
                "likely_next",
            ]
        ]
    ] = Field(
        default=None,
        min_length=1,
        description="Which parts to return: technology, hiring, buying_topics, announcements, changes, traffic, agent_readiness, projects, internal_tools, health, fokals_likely_next. All of them unless given; ask for fewer to keep the answer short.",
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsCompanyProfile(FokalsBaseTool):
    """Company profile: the Fokals company_profile endpoint as a LangChain tool."""

    name: str = "fokals_company_profile"
    description: str = "One company in depth: what it sells and to whom, every technology its website runs and since when, its open roles by function, seniority and country with the latest postings, the buying topics it shows signs of with the signals behind them, its latest announcements by type, the latest changes on its website, how its traffic ranks, its agent readiness score with the evidence behind it, the projects its job ads state, the back-office software they name that its website does not show, its weekly health with the reasons, and the technologies it is likeliest to add next. Use it to research an account before a call, to explain why a company is on a list, or to compare companies. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree."
    args_schema: type[BaseModel] = CompanyProfileInput
    endpoint: str = "company_profile"


class CompanyChangesInput(BaseModel):
    """Arguments of company_changes."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    companies: list[str] = Field(
        min_length=1,
        max_length=1000,
        description='The person\'s own companies, each as a website address ("acme.com"), a name or an id from an earlier answer.',
    )
    since: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}-\\d{2}-\\d{2}$",
        description="What changed on or after this date, YYYY-MM-DD. 7 days ago unless given; at most 90 days back.",
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsCompanyChanges(FokalsBaseTool):
    """What changed at my companies: the Fokals company_changes endpoint as a LangChain tool."""

    name: str = "fokals_company_changes"
    description: str = "What is new at the person's own companies since a date: changes on each website (a technology added or dropped, a new market, language, currency, page or app, a price raised or cut, a plan or a free plan added or dropped, a sales motion or customer size that moved, a title reworded) and the company's announcements by type (funding, launches, partnerships, leadership changes, expansion). Each change comes in plain words. Use it for a weekly check on a list of accounts, or to find a timely reason to get in touch. A company with nothing new costs nothing and is named as such. At most 100 companies a call. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree."
    args_schema: type[BaseModel] = CompanyChangesInput
    endpoint: str = "company_changes"


class SearchJobPostingsInput(BaseModel):
    """Arguments of search_job_postings."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=80,
        description='Text the job title holds: "account executive", "data engineer".',
    )
    job_function: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=40,
        description="One of: software_engineering, hardware_engineering, data_analytics, data_science_ml, product_management, design, marketing_brand, marketing_performance, marketing_content_social, sales, sales_development, customer_success_support, operations, supply_chain_logistics, manufacturing_production, finance_accounting, legal_compliance, people_hr, it_security, research_science, healthcare_clinical, retail_store, hospitality_food, education_training, executive_leadership, other.",
    )
    seniority: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=20,
        description="One of: intern, entry, mid, senior, lead_principal, manager, director, vp, c_level.",
    )
    country: Optional[str] = Field(
        default=None, pattern="^[A-Za-z]{2}$", description="Where the job is, as a two-letter country code: US, GB, DE."
    )
    work_mode: Optional[Literal["onsite", "hybrid", "remote"]] = Field(
        default=None, description="onsite, hybrid or remote."
    )
    technology: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='A technology the posting asks for, by name: "Snowflake", "Salesforce".',
    )
    industry: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=60,
        description="The hiring company's industry. One of: fashion_apparel, beauty_personal_care, health_wellness, food_beverage, home_garden, consumer_electronics, software_saas, finance_insurance, education, travel_hospitality, automotive, real_estate, entertainment_media, gaming, sports_outdoors, retail_marketplace, professional_services, telecom_utilities, nonprofit_public, pets, other.",
    )
    seen_since: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}-\\d{2}-\\d{2}$",
        description="Only postings first seen on or after this date, YYYY-MM-DD.",
    )
    min_salary_usd: Optional[float] = Field(
        default=None,
        ge=1,
        le=10000000,
        description="Only postings that state pay of at least this much a year, in US dollars.",
    )
    companies: Optional[list[str]] = Field(
        default=None,
        min_length=1,
        max_length=1000,
        description="Search only at these companies (the person's own list), each as a website address, a name or an id.",
    )
    limit: Optional[int] = Field(
        default=None, ge=1, le=50, description="How many postings to return. 20 unless given, 50 at most."
    )
    cursor: Optional[str] = Field(
        default=None, max_length=2000, description="next_cursor of the answer before, to carry on where it ended."
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsSearchJobPostings(FokalsBaseTool):
    """Search job postings: the Fokals search_job_postings endpoint as a LangChain tool."""

    name: str = "fokals_search_job_postings"
    description: str = "Searches the open job postings of companies: by words in the title, function, seniority, country, remote or on site, a technology the posting asks for, the hiring company's industry, pay, and how lately the posting appeared. The latest postings come first, each with its company, function, seniority, pay where stated, and link. Use it to find who is hiring for a role, to spot a team being built, or to check hiring at a list of accounts. Give at least one filter. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree."
    args_schema: type[BaseModel] = SearchJobPostingsInput
    endpoint: str = "search_job_postings"


class SimilarCompaniesInput(BaseModel):
    """Arguments of similar_companies."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    company: str = Field(
        min_length=1, max_length=200, description="The company to start from, as a website address, a name or an id."
    )
    kind: Optional[Literal["lookalikes", "competitors"]] = Field(
        default=None,
        description="lookalikes (unless given): companies of the same kind, to sell to as one sells to this one. competitors: companies that sell the same kind of thing to the same kind of customer.",
    )
    limit: Optional[int] = Field(
        default=None, ge=1, le=1000, description="How many companies to return. 10 unless given."
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsSimilarCompanies(FokalsBaseTool):
    """Similar companies and competitors: the Fokals similar_companies endpoint as a LangChain tool."""

    name: str = "fokals_similar_companies"
    description: str = "Finds companies like a given one, the most alike first, each with what it shares with the one given: the labels in common (business model, offering, customer size, pricing, growth stage, home country) and the technologies in common. Ask for lookalikes to grow a list from a best customer, or for competitors to see who sells the same kind of thing to the same kind of customer. The company given is not charged. At most 100 companies a call. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree."
    args_schema: type[BaseModel] = SimilarCompaniesInput
    endpoint: str = "similar_companies"


class CompanyConnectionsInput(BaseModel):
    """Arguments of company_connections."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    company: str = Field(
        min_length=1, max_length=200, description="The company, as a website address, a name or an id."
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsCompanyConnections(FokalsBaseTool):
    """Customers, partners, integrations and investors: the Fokals company_connections endpoint as a LangChain tool."""

    name: str = "fokals_company_connections"
    description: str = 'The other companies a company\'s own website names, and as what: its customers, partners, integrations and investors, each by website and, where held, by name. And the reverse: the companies whose websites name this one, and as what, which shows whose customer or partner it is. Taken from links a page puts under a heading of its own ("Trusted by", "Our partners", "Integrations", "Backed by") and seen in the last 60 days; a company whose pages name nobody that way has none. Only the company asked about is charged. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree.'
    args_schema: type[BaseModel] = CompanyConnectionsInput
    endpoint: str = "company_connections"


class IdentifyCompanyInput(BaseModel):
    """Arguments of identify_company."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    company: str = Field(min_length=2, max_length=200, description="A company name, part of one, or a website address.")


class FokalsIdentifyCompany(FokalsBaseTool):
    """Which company is meant: the Fokals identify_company endpoint as a LangChain tool."""

    name: str = "fokals_identify_company"
    description: str = "Lists the companies a name or a website address could mean, the surest first, each with its website, country, industry and whether it has been read. Free. Use it when a name is ambiguous or a paid tool said a company is not held, then pass the id of the right one to the other tools."
    args_schema: type[BaseModel] = IdentifyCompanyInput
    endpoint: str = "identify_company"


class MarketBreakdownInput(BaseModel):
    """Arguments of market_breakdown."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    technology: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='A technology the company runs on its website, by name: "Shopify", "HubSpot". The stance a website states towards AI is found the same way: "Blocks GPTBot (OpenAI)", "llms.txt for AI assistants", "WebMCP tools for AI agents".',
    )
    buying_topic: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='A buying topic the company shows signs of, by name or id: "Marketing automation". fokals_list_filters with kind buying_topics has them all.',
    )
    hiring: Optional[bool] = Field(default=None, description="true keeps only companies with open roles now.")
    industry: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=60,
        description="One of: fashion_apparel, beauty_personal_care, health_wellness, food_beverage, home_garden, consumer_electronics, software_saas, finance_insurance, education, travel_hospitality, automotive, real_estate, entertainment_media, gaming, sports_outdoors, retail_marketplace, professional_services, telecom_utilities, nonprofit_public, pets, other.",
    )
    business_model: Optional[str] = Field(
        default=None, min_length=1, max_length=20, description="One of: b2b, b2c, both."
    )
    country: Optional[str] = Field(
        default=None,
        pattern="^[A-Za-z]{2}$",
        description="A country as a two-letter code: US, GB, DE. Matches the head office's country where it is known, otherwise the main market the company's website serves: country and market_country in an answer.",
    )
    listed: Optional[bool] = Field(
        default=None, description="true keeps only companies with a stock exchange listing, their own or a parent's."
    )
    changed_since: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}-\\d{2}-\\d{2}$",
        description="Keeps only companies whose website changed on or after this date, YYYY-MM-DD.",
    )
    region: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=60,
        description='The state or province of the head office: "CA", "Ontario". Held where a filing or the company\'s own website gives it.',
    )
    sic: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}$",
        description="A four-digit SIC industry code. Held for companies that file with the SEC.",
    )
    announcement: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=40,
        description="A type of announcement the company made lately. One of: product_launch, partnership, acquisition_made, acquired_or_merged, funding_round, leadership_change, layoffs_restructuring, expansion, incident, financial_results, award_or_recognition, regulatory_or_legal.",
    )
    announced_since: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}-\\d{2}-\\d{2}$",
        description="With announcement: made on or after this date, YYYY-MM-DD. 30 days ago unless given.",
    )
    name_contains: Optional[str] = Field(
        default=None, min_length=2, max_length=80, description="Text the company's name or website address holds."
    )
    agent_ready_min: Optional[int] = Field(
        default=None,
        ge=50,
        le=100,
        description="Keeps only companies whose agent readiness score is at least this, from 50 to 100. The score, from 0 to 100, says how ready a company's website is for AI agents: to be found, to show its prices, to sell and to be acted on.",
    )
    agent_ready_part: Optional[Literal["find", "price", "buy", "act"]] = Field(
        default=None,
        description="One of the four parts of agent readiness that must be strong: find, price, buy or act. With agent_ready_min, or alone for a score of 50 or more.",
    )
    agent_ready_part_min: Optional[int] = Field(
        default=None,
        ge=1,
        le=25,
        description="With agent_ready_part: the least points of its 25 that part holds. 15 unless given.",
    )
    project: Optional[Literal["migration", "first_team", "compliance", "expansion", "ai_build"]] = Field(
        default=None,
        description="A project the company's job ads state: migration (a move from one system to another), first_team (the first team of a function), compliance (work towards a certification), expansion (into a new country or region), ai_build (building an AI product).",
    )
    project_detail: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='With project, what narrows it. migration: a system by name, on either side ("Salesforce"), or "to HubSpot", "from Salesforce", "Salesforce to HubSpot". first_team: a job function (data_analytics, sales). compliance: soc2, iso27001, hipaa, pci, fedramp, gdpr. expansion: a two-letter country code or a region (europe, dach). ai_build: agents, llm, ml, ai.',
    )
    project_days: Optional[int] = Field(
        default=None,
        ge=7,
        le=365,
        description="With project: stated in job ads on a board in the last this many days. 90 unless given.",
    )
    price_change: Optional[
        Literal[
            "price_raised", "price_cut", "free_plan_removed", "free_plan_added", "usage_pricing_added", "ai_addon_added"
        ]
    ] = Field(
        default=None,
        description="A change the company's pricing page showed lately: price_raised, price_cut, free_plan_removed, free_plan_added, usage_pricing_added, ai_addon_added.",
    )
    price_changed_since: Optional[str] = Field(
        default=None,
        pattern="^\\d{4}-\\d{2}-\\d{2}$",
        description="With price_change: on or after this date, YYYY-MM-DD. 90 days ago unless given.",
    )
    health_band: Optional[Literal["distress", "watch", "growing", "breakout"]] = Field(
        default=None,
        description="The company's health in the latest week: distress (signs of distress), watch (worth watching), growing or breakout (breaking out).",
    )
    shift: Optional[Literal["upmarket", "downmarket", "ai_pivot", "new_buyer", "price_up", "price_down"]] = Field(
        default=None,
        description="A shift in positioning the company shows in the latest week: upmarket, downmarket, ai_pivot (turning to AI), new_buyer (selling to a new buyer), price_up or price_down.",
    )
    by: Literal[
        "industry",
        "business_model",
        "country",
        "growth_stage",
        "customer_size",
        "price_tier",
        "sales_motion",
        "pricing_model",
        "region",
        "sic",
        "technology",
        "buying_topic",
    ] = Field(
        description="The attribute to divide the companies by. country is the head office's country where it is known, otherwise the main market the company's website serves; region is the head office's state or province."
    )
    limit: Optional[int] = Field(
        default=None, ge=1, le=50, description="How many values to return, the largest first. 15 unless given."
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsMarketBreakdown(FokalsBaseTool):
    """Market breakdown: the Fokals market_breakdown endpoint as a LangChain tool."""

    name: str = "fokals_market_breakdown"
    description: str = "Answers a question about a market as a whole: how the companies that match a set of filters divide by one attribute (industry, business_model, country, growth_stage, customer_size, price_tier, sales_motion, pricing_model, region, sic, technology, buying_topic), with the number of companies under each value and the total. Takes the same filters as fokals_find_companies, or none for every company held. Use it to size a segment, to see which technologies or buying topics lead in an industry, or which countries a kind of company is in. It returns counts, not companies. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree."
    args_schema: type[BaseModel] = MarketBreakdownInput
    endpoint: str = "market_breakdown"


class VendorScorecardInput(BaseModel):
    """Arguments of vendor_scorecard."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    technology: str = Field(
        min_length=1, max_length=80, description='The technology, by name or id: "HubSpot", "Shopify", "Intercom".'
    )
    months: Optional[int] = Field(
        default=None, ge=1, le=12, description="How many closed months to return, the latest first. 6 unless given."
    )
    segment: Optional[Literal["all", "size", "industry", "growth_stage", "country"]] = Field(
        default=None,
        description="How the companies are divided: all (unless given), size (by employees), industry, growth_stage or country. Divided, each month comes once for each segment, the 20 largest first.",
    )
    include_rivals_in_category: Optional[bool] = Field(
        default=None,
        description="true adds the technologies of the same category, ranked by companies gained net in the latest month held.",
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsVendorScorecard(FokalsBaseTool):
    """Vendor scorecard: the Fokals vendor_scorecard endpoint as a LangChain tool."""

    name: str = "fokals_vendor_scorecard"
    description: str = "A technology vendor's scorecard, month by month: how many companies ran it at the start of each month, how many took it up and how many dropped it, the net change and the churn rate, and the rival tools the companies that took it up came from and the ones that dropped it moved to; with the last 30 days to today beside them. Divide it by company size, industry, growth stage or country to see where it wins and where it loses (industry and growth stage are the companies' labels today), and ask for the other technologies of its category ranked by net gain. A month marked partial was not observed from its first day. Use it for competitive research on a vendor, to see where a rival is losing customers, or to size a vendor's momentum. It returns counts, not companies. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree."
    args_schema: type[BaseModel] = VendorScorecardInput
    endpoint: str = "vendor_scorecard"


class CompaniesLikeCustomersInputCustomersItem(BaseModel):
    """One item."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    company: str = Field(
        min_length=1,
        max_length=200,
        description='A customer, as a website address ("acme.com"), a name or an id from an earlier answer.',
    )
    bought_on: Optional[str] = Field(
        default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$", description="The day it bought, YYYY-MM-DD, where known."
    )


class CompaniesLikeCustomersInput(BaseModel):
    """Arguments of companies_like_customers."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    customers: list[CompaniesLikeCustomersInputCustomersItem] = Field(
        min_length=1,
        max_length=20,
        description="The person's own customers, 1 to 20, each with the day it bought where known.",
    )
    technology: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='The technology the customers bought, by name, where it is one: "HubSpot". Companies already running it are left out.',
    )
    country: Optional[str] = Field(
        default=None,
        pattern="^[A-Za-z]{2}$",
        description="Only companies in this country, as a two-letter code. Matches the head office's country where it is known, otherwise the main market the company's website serves.",
    )
    industry: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=60,
        description="Only companies of this industry. One of: fashion_apparel, beauty_personal_care, health_wellness, food_beverage, home_garden, consumer_electronics, software_saas, finance_insurance, education, travel_hospitality, automotive, real_estate, entertainment_media, gaming, sports_outdoors, retail_marketplace, professional_services, telecom_utilities, nonprofit_public, pets, other.",
    )
    limit: Optional[int] = Field(
        default=None, ge=1, le=100, description="How many companies to return. 25 unless given."
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsCompaniesLikeCustomers(FokalsBaseTool):
    """Companies like my customers: the Fokals companies_like_customers endpoint as a LangChain tool."""

    name: str = "fokals_companies_like_customers"
    description: str = "Finds the companies that look today the way the person's own customers looked when they bought. Give up to 20 customers, by website, name or id, each with the day it bought where known, and the technology they bought where there is one. The answer also says for which customers a buying moment was found, and what most of them did before buying. Results are strongest when the customers' buying dates are known or a technology is given; without either, companies are matched on how alike they are to the customers today. The customers, and companies already running the technology, are left out. At most 100 companies a call. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree."
    args_schema: type[BaseModel] = CompaniesLikeCustomersInput
    endpoint: str = "companies_like_customers"


class CompanyHealthInput(BaseModel):
    """Arguments of company_health."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    companies: list[str] = Field(
        min_length=1,
        max_length=1000,
        description='The person\'s own companies, each as a website address ("acme.com"), a name or an id from an earlier answer.',
    )
    weeks: Optional[int] = Field(
        default=None, ge=1, le=13, description="How many weeks of scores to return, oldest first. 13 unless given."
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsCompanyHealth(FokalsBaseTool):
    """Company health: the Fokals company_health endpoint as a LangChain tool."""

    name: str = "fokals_company_health"
    description: str = "A weekly health reading for each of the person's companies: a band in words (signs of distress, worth watching, steady, growing, breaking out), a distress score and a breakout score from 0 to 100, the reasons in plain words, the shifts in positioning it shows (moving upmarket or downmarket, turning to AI, selling to a new buyer, prices going up or down), and the scores week by week. Use it to spot accounts at risk or taking off, and to time an approach. A company with no health reading costs nothing and is named as such. At most 100 companies a call. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree."
    args_schema: type[BaseModel] = CompanyHealthInput
    endpoint: str = "company_health"


class LikelyNextInput(BaseModel):
    """Arguments of likely_next."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    companies: Optional[list[str]] = Field(
        default=None,
        min_length=1,
        max_length=1000,
        description="The person's own companies, each as a website address, a name or an id: the technologies each is likeliest to add next. Give these or a technology.",
    )
    technology: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description='A technology, by name: "HubSpot". The companies likeliest to add it next. Give this or companies.',
    )
    country: Optional[str] = Field(
        default=None,
        pattern="^[A-Za-z]{2}$",
        description="With technology: only companies in this country. Matches the head office's country where it is known, otherwise the main market the company's website serves.",
    )
    industry: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=60,
        description="With technology: only companies of this industry. One of: fashion_apparel, beauty_personal_care, health_wellness, food_beverage, home_garden, consumer_electronics, software_saas, finance_insurance, education, travel_hospitality, automotive, real_estate, entertainment_media, gaming, sports_outdoors, retail_marketplace, professional_services, telecom_utilities, nonprofit_public, pets, other.",
    )
    limit: Optional[int] = Field(
        default=None, ge=1, le=100, description="With technology: how many companies to return. 25 unless given."
    )
    cursor: Optional[str] = Field(
        default=None,
        max_length=200,
        description="With technology: next_cursor of the answer before, to carry on where it ended.",
    )
    max_usd: Optional[float] = Field(
        default=None,
        ge=0,
        le=100000,
        description="The most the person has agreed to pay for this call, in US dollars. Leave it out unless a call has returned its price and the person agreed to it.",
    )


class FokalsLikelyNext(FokalsBaseTool):
    """Likely next technologies: the Fokals likely_next endpoint as a LangChain tool."""

    name: str = "fokals_likely_next"
    description: str = "What companies are likely to add next. Give the person's own companies to get, for each, the technologies it is likeliest to add in the coming weeks, each with an estimated likelihood (0 to 1), with the support counts behind it: the changes behind it in plain words, how many companies made the same change and how many of them then added the technology. A likelihood is an estimate, never a certainty. Or give a technology to get the companies likeliest to add it next, likeliest first, a page at a time, with the changes that most often come before it. Use it to reach an account before it buys, or to build a list of the next buyers of a product. At most 100 companies a call. Paid from the Fokals balance at the prices on https://api.fokals.com/v1/prices. A call that costs more than the account lets run unasked returns its price instead: tell the person, then call again with max_usd once they agree."
    args_schema: type[BaseModel] = LikelyNextInput
    endpoint: str = "likely_next"


class ListFiltersInput(BaseModel):
    """Arguments of list_filters."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    kind: Literal[
        "technologies", "buying_topics", "industries", "business_models", "countries", "announcement_types"
    ] = Field(description="Which list to return.")
    search: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description="Text a name holds. Needed for technologies beyond the most used: there are thousands.",
    )
    limit: Optional[int] = Field(default=None, ge=1, le=200, description="How many to return. 50 unless given.")


class FokalsListFilters(FokalsBaseTool):
    """List filter values: the Fokals list_filters endpoint as a LangChain tool."""

    name: str = "fokals_list_filters"
    description: str = "Lists the values fokals_find_companies and fokals_count_companies filter by, with the number of companies under each where it is known: technologies (search by name), buying topics, industries, business models, countries (by the head office's country where it is known, otherwise the main market the company's website serves), and the types of announcement. Free."
    args_schema: type[BaseModel] = ListFiltersInput
    endpoint: str = "list_filters"


class AccountBalanceInput(BaseModel):
    """Arguments of account_balance."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class FokalsAccountBalance(FokalsBaseTool):
    """Balance and prices: the Fokals account_balance endpoint as a LangChain tool."""

    name: str = "fokals_account_balance"
    description: str = "The person's prepaid balance and the dates it expires, what they have spent this month and on which tools, their monthly spending limit, the prices, and where to add funds. Free."
    args_schema: type[BaseModel] = AccountBalanceInput
    endpoint: str = "account_balance"


ALL_TOOLS: tuple[type[FokalsBaseTool], ...] = (
    FokalsFindCompanies,
    FokalsCountCompanies,
    FokalsEnrichCompanies,
    FokalsCompanyProfile,
    FokalsCompanyChanges,
    FokalsSearchJobPostings,
    FokalsSimilarCompanies,
    FokalsCompanyConnections,
    FokalsIdentifyCompany,
    FokalsMarketBreakdown,
    FokalsVendorScorecard,
    FokalsCompaniesLikeCustomers,
    FokalsCompanyHealth,
    FokalsLikelyNext,
    FokalsListFilters,
    FokalsAccountBalance,
)

# The API's own example call for each tool, by tool name.
EXAMPLES: dict[str, dict] = {
    "fokals_find_companies": {"technology": "HubSpot", "hiring": True, "country": "US", "limit": 10},
    "fokals_count_companies": {"technology": "HubSpot", "hiring": True, "country": "US"},
    "fokals_enrich_companies": {"companies": ["stripe.com", "shopify.com"]},
    "fokals_company_profile": {"company": "stripe.com"},
    "fokals_company_changes": {"companies": ["stripe.com", "shopify.com"], "since": "2026-10-01"},
    "fokals_search_job_postings": {"title": "data engineer", "country": "US", "work_mode": "remote", "limit": 10},
    "fokals_similar_companies": {"company": "shopify.com", "kind": "lookalikes", "limit": 10},
    "fokals_company_connections": {"company": "stripe.com"},
    "fokals_identify_company": {"company": "Stripe"},
    "fokals_market_breakdown": {"technology": "Shopify", "by": "country", "limit": 10},
    "fokals_vendor_scorecard": {"technology": "HubSpot", "months": 6, "segment": "size"},
    "fokals_companies_like_customers": {
        "customers": [
            {"company": "notion.so", "bought_on": "2026-09-15"},
            {"company": "figma.com"},
            {"company": "linear.app"},
        ],
        "technology": "HubSpot",
        "limit": 25,
    },
    "fokals_company_health": {"companies": ["stripe.com", "shopify.com"], "weeks": 13},
    "fokals_likely_next": {"technology": "Klaviyo", "country": "US", "limit": 25},
    "fokals_list_filters": {"kind": "buying_topics", "search": "marketing", "limit": 20},
    "fokals_account_balance": {},
}
