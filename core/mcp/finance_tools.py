# Financial Modelling Tools MCP Registry
# Contains 10 premium tools in a single category

from core.mcp.finance_data import COMPANIES_DB

def _get_co(ticker: str) -> dict:
    tk = str(ticker).strip().upper()
    return COMPANIES_DB.get(tk, COMPANIES_DB["AAPL"])

def _execute_tool_impl(tool_name: str, ticker: str) -> str:
    co = _get_co(ticker)
    name = co["name"]
    tk = co["ticker"]
    sector = co["sector"]
    ceo = co["ceo"]

    if tool_name == "finance_company_profile":
        return f"### {name} ({tk}) Profile\n- Founded: {co['founded']}\n- Sector: {sector}\n- CEO: {ceo}\n- Headquarters: {co['hq']}"

    elif tool_name == "finance_swot_analysis":
        return f"### SWOT Analysis ({tk})\n- **Strengths:** Market leader, solid cash reserves.\n- **Weaknesses:** Regulatory headwinds.\n- **Opportunities:** International cloud expansion.\n- **Threats:** Margin pressure from competitors."

    elif tool_name == "finance_income_statement":
        f = co["financials"]
        return f"### Income Statement ({tk})\n- Revenue: ${f['2025']['revenue']:,.1f}M\n- Net Income: ${f['2025']['net_income']:,.1f}M\n- EBITDA: ${f['2025']['ebitda']:,.1f}M"

    elif tool_name == "finance_balance_sheet":
        f = co["financials"]
        return f"### Balance Sheet ({tk})\n- Cash & Equivalents: ${f['2025']['cash']:,.1f}M\n- Total Debt: ${f['2025']['debt']:,.1f}M"

    elif tool_name == "finance_cash_flow":
        f = co["financials"]
        return f"### Cash Flow ({tk})\n- Operating CF: ${f['2025']['ebitda'] * 0.85:,.1f}M\n- Free Cash Flow: ${f['2025']['ebitda'] * 0.85 - f['2025']['revenue'] * 0.05:,.1f}M"

    elif tool_name == "finance_eps_forecast":
        ae = co["analyst_estimates"]
        return f"### EPS Forecast ({tk})\n- 2025 EPS (Actual): ${ae['eps_2025']:.2f}\n- 2026 EPS Estimate: ${ae['eps_2026_est']:.2f}"

    elif tool_name == "finance_dcf_valuation":
        f = co["financials"]["2025"]
        fcf = f["ebitda"] * 0.85 - f["revenue"] * 0.05
        wacc = 8.5
        g = 3.0
        ev = fcf / (wacc / 100.0 - g / 100.0)
        implied_share = (ev - f["debt"] + f["cash"]) / 500
        return f"### DCF Valuation ({tk})\n- Base FCF: ${fcf:,.1f}M\n- Implied Enterprise Value: ${ev:,.1f}M\n- **Implied Share Price: ${(implied_share if implied_share > 0 else 150.0):.2f}**"

    elif tool_name == "finance_valuation_multiples":
        pe = 150.0 / co["analyst_estimates"]["eps_2025"] if tk != "BRK.A" else 20.0
        return f"### Valuation Multiples ({tk})\n- Trailing P/E: {pe:.1f}x\n- EV/EBITDA: {pe * 0.75:.1f}x"

    elif tool_name == "finance_esg_risk":
        esg = co["esg_scores"]
        return f"### ESG Risk Score ({tk})\n- Environmental: {esg['environmental']}/100\n- Social: {esg['social']}/100\n- Governance: {esg['governance']}/100\n- **Overall Rating: {esg['overall']}/100**"

    elif tool_name == "finance_investment_recommendation":
        ae = co["analyst_estimates"]
        return f"### Investment Recommendation ({tk})\n- **Consensus Rating: {ae['consensus'].upper()}**\n- Target Price: ${ae['target_price']:.2f}\n- Rationale: Based on DCF valuation and stable multiples."

    return f"Tool {tool_name} executed on {ticker}."


# ── Registry ─────────────────────────────────────────────────────────────────

# Exactly one single category with 10 tools
TOOL_CATEGORIES = {
    "Financial Intelligence": [
        "finance_company_profile",
        "finance_swot_analysis",
        "finance_income_statement",
        "finance_balance_sheet",
        "finance_cash_flow",
        "finance_eps_forecast",
        "finance_dcf_valuation",
        "finance_valuation_multiples",
        "finance_esg_risk",
        "finance_investment_recommendation"
    ]
}

FINANCE_TOOL_REGISTRY = {}

for category, tools in TOOL_CATEGORIES.items():
    for tool_name in tools:
        def make_fn(name):
            return lambda ticker, **kwargs: _execute_tool_impl(name, ticker)

        FINANCE_TOOL_REGISTRY[tool_name] = {
            "name": tool_name,
            "description": f"[{category}] Fetches {tool_name.replace('finance_', '').replace('_', ' ').title()} for a stock ticker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g. AAPL, MSFT, TSLA)"
                    }
                },
                "required": ["ticker"]
            },
            "fn": make_fn(tool_name)
        }
