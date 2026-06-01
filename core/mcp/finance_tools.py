# Financial Modelling Tools MCP Registry
# Contains 18 tools (3 per category) mapped to the company database

from core.mcp.finance_data import COMPANIES_DB


def _get_co(ticker: str) -> dict:
    tk = str(ticker).strip().upper()
    return COMPANIES_DB.get(tk, COMPANIES_DB["AAPL"])


def _execute_tool_impl(tool_name: str, ticker: str) -> str:
    co = _get_co(ticker)
    name = co["name"]
    tk = co["ticker"]
    sector = co["sector"]
    industry = co["industry"]
    ceo = co["ceo"]

    # ── Research (3) ─────────────────────────────────────────────────────────
    if tool_name == "research_company_profile":
        return f"### {name} ({tk}) Company Profile\n- Founded: {co['founded']}\n- Headquarters: {co['hq']}\n- Sector: {sector}\n- Industry: {industry}\n- CEO: {ceo}"

    elif tool_name == "research_executive_team":
        return f"### Executive Leadership for {name}\n- CEO: {ceo}\n- Executive Board size: 11 members\n- Compensation Committee Chair: John J. Miller\n- Audit Committee Chair: Susan K. Vance"

    elif tool_name == "research_swot_analysis":
        return f"### SWOT Analysis ({tk})\n- **Strengths:** Market leader, solid cash reserves.\n- **Weaknesses:** Regulatory headwinds.\n- **Opportunities:** International cloud expansion.\n- **Threats:** Margin pressure from competitors."

    # ── Financial Analysis (3) ───────────────────────────────────────────────
    elif tool_name == "analyse_income_statement":
        f = co["financials"]
        return f"### Income Statement for {name} ($ in Millions)\n| Metric | 2023 | 2024 | 2025 |\n|---|---|---|---|\n| Revenue | ${f['2023']['revenue']:,.1f} | ${f['2024']['revenue']:,.1f} | ${f['2025']['revenue']:,.1f} |\n| Net Income | ${f['2023']['net_income']:,.1f} | ${f['2024']['net_income']:,.1f} | ${f['2025']['net_income']:,.1f} |\n| EBITDA | ${f['2023']['ebitda']:,.1f} | ${f['2024']['ebitda']:,.1f} | ${f['2025']['ebitda']:,.1f} |"

    elif tool_name == "analyse_balance_sheet":
        f = co["financials"]
        return f"### Balance Sheet for {name} ($ in Millions)\n| Metric | 2023 | 2024 | 2025 |\n|---|---|---|---|\n| Cash & Equivalents | ${f['2023']['cash']:,.1f} | ${f['2024']['cash']:,.1f} | ${f['2025']['cash']:,.1f} |\n| Total Debt | ${f['2023']['debt']:,.1f} | ${f['2024']['debt']:,.1f} | ${f['2025']['debt']:,.1f} |"

    elif tool_name == "analyse_cash_flow":
        f = co["financials"]
        return f"### Cash Flow Statement ({tk}) ($ in Millions)\n| Metric | 2023 | 2024 | 2025 |\n|---|---|---|---|\n| Operating CF | ${f['2023']['ebitda'] * 0.85:,.1f} | ${f['2024']['ebitda'] * 0.85:,.1f} | ${f['2025']['ebitda'] * 0.85:,.1f} |\n| Free Cash Flow | ${f['2023']['ebitda'] * 0.85 - f['2023']['revenue'] * 0.05:,.1f} | ${f['2024']['ebitda'] * 0.85 - f['2024']['revenue'] * 0.05:,.1f} | ${f['2025']['ebitda'] * 0.85 - f['2025']['revenue'] * 0.05:,.1f} |"

    # ── Forecasting (3) ──────────────────────────────────────────────────────
    elif tool_name == "forecast_revenue_growth":
        f = co["financials"]
        return f"### Revenue Forecast ({tk})\n- 2025 (Actual): ${f['2025']['revenue']:,.1f}M\n- 2026 (Projected): ${f['2026_proj']['revenue']:,.1f}M"

    elif tool_name == "forecast_eps_estimates":
        ae = co["analyst_estimates"]
        return f"### EPS Forecast ({tk})\n- 2025 EPS (Actual): ${ae['eps_2025']:.2f}\n- 2026 EPS Estimate: ${ae['eps_2026_est']:.2f}"

    elif tool_name == "forecast_analyst_consensus":
        ae = co["analyst_estimates"]
        return f"### Analyst Consensus ({tk})\n- Recommendation: **{ae['consensus']}**\n- Target Price: ${ae['target_price']:.2f}\n- Analysts: {ae['num_analysts']}"

    # ── Valuation (3) ────────────────────────────────────────────────────────
    elif tool_name == "valuation_dcf_model":
        f = co["financials"]["2025"]
        fcf = f["ebitda"] * 0.85 - f["revenue"] * 0.05
        wacc = 8.5
        g = 3.0
        ev = fcf / (wacc / 100.0 - g / 100.0)
        implied_share = (ev - f["debt"] + f["cash"]) / 500
        if implied_share < 0:
            implied_share = 150.0
        return f"### DCF Valuation ({tk})\n- Base FCF: ${fcf:,.1f}M\n- WACC: {wacc}%\n- Terminal Growth: {g}%\n- Enterprise Value: ${ev:,.1f}M\n- **Implied Share Price: ${implied_share:.2f}**\n- Analyst Target: ${co['analyst_estimates']['target_price']:.2f}"

    elif tool_name == "valuation_comps_multiples":
        pe = 150.0 / co["analyst_estimates"]["eps_2025"] if tk != "BRK.A" else 20.0
        return f"### Valuation Multiples ({tk})\n- Trailing P/E: {pe:.1f}x\n- EV/EBITDA: {pe * 0.75:.1f}x\n- Price/Sales: {pe * 0.25:.1f}x"

    elif tool_name == "valuation_peer_comparison":
        pe = 150.0 / co["analyst_estimates"]["eps_2025"] if tk != "BRK.A" else 20.0
        p_str = ", ".join([f"{p}: {pe * 0.95:.1f}x" for p in co["peer_group"]])
        return f"### Peer Comparison (P/E)\n- {tk}: {pe:.1f}x\n- Peers: {p_str}"

    # ── Risk (3) ─────────────────────────────────────────────────────────────
    elif tool_name == "risk_esg_scores":
        esg = co["esg_scores"]
        return f"### ESG Scores ({tk})\n- Environmental: {esg['environmental']}/100\n- Social: {esg['social']}/100\n- Governance: {esg['governance']}/100\n- **Overall: {esg['overall']}/100**"

    elif tool_name == "risk_beta_coefficient":
        return f"### Beta & Volatility ({tk})\n- Beta: {co['beta']}\n- 30-Day Volatility: 22.4%\n- Risk Category: {'High Volatility' if co['beta'] > 1.2 else 'Defensive'}"

    elif tool_name == "risk_credit_rating":
        return f"### Credit Rating ({tk})\n- Rating: **{co['credit_rating']}**\n- Outlook: Stable\n- Default Risk: Low"

    # ── Reporting (3) ────────────────────────────────────────────────────────
    elif tool_name == "report_one_pager":
        f = co["financials"]["2025"]
        pe = 150.0 / co["analyst_estimates"]["eps_2025"] if tk != "BRK.A" else 20.0
        return f"""### 📊 {name} ({tk}) — Investment One-Pager

**Profile:** {ceo} | {sector} | {co['hq']}

**Financials (2025):**
- Revenue: ${f['revenue']:,.1f}M | EBITDA: ${f['ebitda']:,.1f}M | Net Income: ${f['net_income']:,.1f}M

**Valuation:** P/E {pe:.1f}x | Beta {co['beta']} | ESG {co['esg_scores']['overall']}/100 | Credit {co['credit_rating']}

**Outlook:** {co['earnings_call']['transcript_summary']}
"""

    elif tool_name == "report_executive_briefing":
        return f"### Executive Briefing — {name} ({tk})\n- Stable operating profile with low credit risk and {co['earnings_call']['sentiment'].lower()} outlook.\n- Key focus: tracking expansion margins in Q3."

    elif tool_name == "report_investment_recommendation":
        return f"### Investment Recommendation ({tk})\n- **Rating: OVERWEIGHT / BUY**\n- Rationale: Valuation discount vs peers, strong WACC-to-ROE spreads, minimal litigation risk."

    return f"Tool {tool_name} executed on {ticker}."


# ── Registry ─────────────────────────────────────────────────────────────────

TOOL_CATEGORIES = {
    "Research": [
        "research_company_profile", "research_executive_team", "research_swot_analysis"
    ],
    "Financial Analysis": [
        "analyse_income_statement", "analyse_balance_sheet", "analyse_cash_flow"
    ],
    "Forecasting": [
        "forecast_revenue_growth", "forecast_eps_estimates", "forecast_analyst_consensus"
    ],
    "Valuation": [
        "valuation_dcf_model", "valuation_comps_multiples", "valuation_peer_comparison"
    ],
    "Risk": [
        "risk_esg_scores", "risk_beta_coefficient", "risk_credit_rating"
    ],
    "Reporting": [
        "report_one_pager", "report_executive_briefing", "report_investment_recommendation"
    ]
}

FINANCE_TOOL_REGISTRY = {}

for category, tools in TOOL_CATEGORIES.items():
    for tool_name in tools:
        def make_fn(name):
            return lambda ticker, **kwargs: _execute_tool_impl(name, ticker)

        FINANCE_TOOL_REGISTRY[tool_name] = {
            "name": tool_name,
            "description": f"[{category}] {tool_name.replace('_', ' ').title()} — retrieves data for a given stock ticker.",
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
