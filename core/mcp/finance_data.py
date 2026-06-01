# 50-Company Financial Dataset for Wall Street AI Analyst Skill
# Contains realistic data across 10 dimensions for 50 major US & Global companies

COMPANIES = [
    {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology", "industry": "Consumer Electronics", "ceo": "Tim Cook", "founded": 1976, "hq": "Cupertino, CA", "base_rev": 383000, "margin": 0.25, "growth": 0.08, "esg_e": 88, "esg_s": 79, "esg_g": 92, "beta": 1.25, "rating": "AA+"},
    {"ticker": "MSFT", "name": "Microsoft Corp.", "sector": "Technology", "industry": "Software-Infrastructure", "ceo": "Satya Nadella", "founded": 1975, "hq": "Redmond, WA", "base_rev": 245000, "margin": 0.35, "growth": 0.14, "esg_e": 91, "esg_s": 85, "esg_g": 94, "beta": 1.15, "rating": "AAA"},
    {"ticker": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology", "industry": "Internet Content & Information", "ceo": "Sundar Pichai", "founded": 1998, "hq": "Mountain View, CA", "base_rev": 307000, "margin": 0.24, "growth": 0.11, "esg_e": 85, "esg_s": 77, "esg_g": 86, "beta": 1.05, "rating": "AA+"},
    {"ticker": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Discretionary", "industry": "Internet Retail", "ceo": "Andy Jassy", "founded": 1994, "hq": "Seattle, WA", "base_rev": 574000, "margin": 0.06, "growth": 0.12, "esg_e": 82, "esg_s": 72, "esg_g": 80, "beta": 1.18, "rating": "AA"},
    {"ticker": "NVDA", "name": "NVIDIA Corp.", "sector": "Technology", "industry": "Semiconductors", "ceo": "Jensen Huang", "founded": 1993, "hq": "Santa Clara, CA", "base_rev": 60000, "margin": 0.48, "growth": 1.25, "esg_e": 78, "esg_s": 79, "esg_g": 88, "beta": 1.75, "rating": "AA"},
    {"ticker": "META", "name": "Meta Platforms Inc.", "sector": "Technology", "industry": "Internet Content & Information", "ceo": "Mark Zuckerberg", "founded": 2004, "hq": "Menlo Park, CA", "base_rev": 134000, "margin": 0.29, "growth": 0.16, "esg_e": 76, "esg_s": 71, "esg_g": 83, "beta": 1.22, "rating": "AA-"},
    {"ticker": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Discretionary", "industry": "Auto Manufacturers", "ceo": "Elon Musk", "founded": 2003, "hq": "Austin, TX", "base_rev": 96000, "margin": 0.13, "growth": 0.19, "esg_e": 94, "esg_s": 65, "esg_g": 72, "beta": 1.55, "rating": "A-"},
    {"ticker": "BRK.A", "name": "Berkshire Hathaway Inc.", "sector": "Financials", "industry": "Multi-Sector Holdings", "ceo": "Warren Buffett", "founded": 1839, "hq": "Omaha, NE", "base_rev": 364000, "margin": 0.10, "growth": 0.05, "esg_e": 62, "esg_s": 68, "esg_g": 85, "beta": 0.65, "rating": "AA+"},
    {"ticker": "LLY", "name": "Eli Lilly & Co.", "sector": "Healthcare", "industry": "Drug Manufacturers-General", "ceo": "David Ricks", "founded": 1876, "hq": "Indianapolis, IN", "base_rev": 34000, "margin": 0.20, "growth": 0.26, "esg_e": 75, "esg_s": 80, "esg_g": 88, "beta": 0.58, "rating": "AA"},
    {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financials", "industry": "Banks-Diversified", "ceo": "Jamie Dimon", "founded": 1799, "hq": "New York, NY", "base_rev": 158000, "margin": 0.31, "growth": 0.07, "esg_e": 71, "esg_s": 76, "esg_g": 89, "beta": 1.08, "rating": "AA-"},
    {"ticker": "V", "name": "Visa Inc.", "sector": "Financials", "industry": "Credit Services", "ceo": "Ryan McInerney", "founded": 1958, "hq": "San Francisco, CA", "base_rev": 32000, "margin": 0.52, "growth": 0.10, "esg_e": 81, "esg_s": 83, "esg_g": 91, "beta": 0.95, "rating": "AA"},
    {"ticker": "UNH", "name": "UnitedHealth Group Inc.", "sector": "Healthcare", "industry": "Healthcare Plans", "ceo": "Andrew Witty", "founded": 1977, "hq": "Minnetonka, MN", "base_rev": 371000, "margin": 0.06, "growth": 0.11, "esg_e": 68, "esg_s": 79, "esg_g": 84, "beta": 0.72, "rating": "A+"},
    {"ticker": "MA", "name": "Mastercard Inc.", "sector": "Financials", "industry": "Credit Services", "ceo": "Michael Miebach", "founded": 1966, "hq": "Purchase, NY", "base_rev": 25000, "margin": 0.46, "growth": 0.12, "esg_e": 84, "esg_s": 82, "esg_g": 90, "beta": 0.98, "rating": "AA"},
    {"ticker": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare", "industry": "Drug Manufacturers-General", "ceo": "Joaquin Duato", "founded": 1886, "hq": "New Brunswick, NJ", "base_rev": 85000, "margin": 0.18, "growth": 0.04, "esg_e": 79, "esg_s": 81, "esg_g": 87, "beta": 0.54, "rating": "AAA"},
    {"ticker": "PG", "name": "Procter & Gamble Co.", "sector": "Consumer Staples", "industry": "Household & Personal Products", "ceo": "Jon Moeller", "founded": 1837, "hq": "Cincinnati, OH", "base_rev": 82000, "margin": 0.18, "growth": 0.03, "esg_e": 83, "esg_s": 79, "esg_g": 89, "beta": 0.42, "rating": "AA-"},
    {"ticker": "HD", "name": "Home Depot Inc.", "sector": "Consumer Discretionary", "industry": "Home Improvement Retail", "ceo": "Ted Decker", "founded": 1978, "hq": "Atlanta, GA", "base_rev": 152000, "margin": 0.10, "growth": 0.02, "esg_e": 74, "esg_s": 77, "esg_g": 82, "beta": 0.96, "rating": "A"},
    {"ticker": "MRK", "name": "Merck & Co. Inc.", "sector": "Healthcare", "industry": "Drug Manufacturers-General", "ceo": "Robert Davis", "founded": 1891, "hq": "Rahway, NJ", "base_rev": 60000, "margin": 0.15, "growth": 0.06, "esg_e": 76, "esg_s": 82, "esg_g": 85, "beta": 0.40, "rating": "AA"},
    {"ticker": "COST", "name": "Costco Wholesale Corp.", "sector": "Consumer Staples", "industry": "Discount Stores", "ceo": "Ron Vachris", "founded": 1983, "hq": "Issaquah, WA", "base_rev": 242000, "margin": 0.03, "growth": 0.06, "esg_e": 72, "esg_s": 75, "esg_g": 81, "beta": 0.78, "rating": "AA-"},
    {"ticker": "ABBV", "name": "AbbVie Inc.", "sector": "Healthcare", "industry": "Drug Manufacturers-General", "ceo": "Richard Gonzalez", "founded": 2013, "hq": "North Chicago, IL", "base_rev": 54000, "margin": 0.17, "growth": 0.02, "esg_e": 70, "esg_s": 78, "esg_g": 83, "beta": 0.55, "rating": "A-"},
    {"ticker": "AMD", "name": "Advanced Micro Devices", "sector": "Technology", "industry": "Semiconductors", "ceo": "Lisa Su", "founded": 1969, "hq": "Santa Clara, CA", "base_rev": 22000, "margin": 0.08, "growth": 0.22, "esg_e": 81, "esg_s": 74, "esg_g": 85, "beta": 1.68, "rating": "A-"},
    {"ticker": "NFLX", "name": "Netflix Inc.", "sector": "Communication Services", "industry": "Entertainment", "ceo": "Ted Sarandos", "founded": 1997, "hq": "Los Gatos, CA", "base_rev": 33000, "margin": 0.18, "growth": 0.15, "esg_e": 73, "esg_s": 78, "esg_g": 82, "beta": 1.28, "rating": "A"},
    {"ticker": "CRM", "name": "Salesforce Inc.", "sector": "Technology", "industry": "Software-Application", "ceo": "Marc Benioff", "founded": 1999, "hq": "San Francisco, CA", "base_rev": 34000, "margin": 0.16, "growth": 0.11, "esg_e": 89, "esg_s": 84, "esg_g": 90, "beta": 1.12, "rating": "AA-"},
    {"ticker": "ADBE", "name": "Adobe Inc.", "sector": "Technology", "industry": "Software-Application", "ceo": "Shantanu Narayen", "founded": 1982, "hq": "San Jose, CA", "base_rev": 19000, "margin": 0.28, "growth": 0.10, "esg_e": 85, "esg_s": 80, "esg_g": 88, "beta": 1.15, "rating": "AA-"},
    {"ticker": "CVX", "name": "Chevron Corp.", "sector": "Energy", "industry": "Oil & Gas Integrated", "ceo": "Mike Wirth", "founded": 1879, "hq": "San Ramon, CA", "base_rev": 200000, "margin": 0.11, "growth": -0.04, "esg_e": 62, "esg_s": 71, "esg_g": 78, "beta": 1.10, "rating": "AA-"},
    {"ticker": "PEP", "name": "PepsiCo Inc.", "sector": "Consumer Staples", "industry": "Beverages-Non-Alcoholic", "ceo": "Ramon Laguarta", "founded": 1898, "hq": "Purchase, NY", "base_rev": 91000, "margin": 0.10, "growth": 0.05, "esg_e": 80, "esg_s": 82, "esg_g": 88, "beta": 0.52, "rating": "A+"},
    {"ticker": "KO", "name": "Coca-Cola Co.", "sector": "Consumer Staples", "industry": "Beverages-Non-Alcoholic", "ceo": "James Quincey", "founded": 1886, "hq": "Atlanta, GA", "base_rev": 45000, "margin": 0.23, "growth": 0.06, "esg_e": 82, "esg_s": 83, "esg_g": 90, "beta": 0.50, "rating": "AA-"},
    {"ticker": "TSM", "name": "Taiwan Semiconductor Mfg", "sector": "Technology", "industry": "Semiconductors", "ceo": "C.C. Wei", "founded": 1887, "hq": "Hsinchu, Taiwan", "base_rev": 70000, "margin": 0.40, "growth": 0.25, "esg_e": 87, "esg_s": 78, "esg_g": 84, "beta": 1.20, "rating": "AA-"},
    {"ticker": "WMT", "name": "Walmart Inc.", "sector": "Consumer Staples", "industry": "Discount Stores", "ceo": "Doug McMillon", "founded": 1962, "hq": "Bentonville, AR", "base_rev": 648000, "margin": 0.02, "growth": 0.05, "esg_e": 70, "esg_s": 73, "esg_g": 78, "beta": 0.52, "rating": "AA"},
    {"ticker": "BAC", "name": "Bank of America Corp.", "sector": "Financials", "industry": "Banks-Diversified", "ceo": "Brian Moynihan", "founded": 1998, "hq": "Charlotte, NC", "base_rev": 98000, "margin": 0.25, "growth": 0.03, "esg_e": 74, "esg_s": 79, "esg_g": 86, "beta": 1.35, "rating": "A+"},
    {"ticker": "XOM", "name": "Exxon Mobil Corp.", "sector": "Energy", "industry": "Oil & Gas Integrated", "ceo": "Darren Woods", "founded": 1882, "hq": "Spring, TX", "base_rev": 344000, "margin": 0.11, "growth": -0.05, "esg_e": 58, "esg_s": 69, "esg_g": 76, "beta": 1.05, "rating": "AA-"},
    {"ticker": "NKE", "name": "NIKE Inc.", "sector": "Consumer Discretionary", "industry": "Footwear & Accessories", "ceo": "John Donahoe", "founded": 1964, "hq": "Beaverton, OR", "base_rev": 51000, "margin": 0.10, "growth": 0.04, "esg_e": 84, "esg_s": 80, "esg_g": 86, "beta": 1.10, "rating": "A-"},
    {"ticker": "DIS", "name": "Walt Disney Co.", "sector": "Communication Services", "industry": "Entertainment", "ceo": "Bob Iger", "founded": 1923, "hq": "Burbank, CA", "base_rev": 88000, "margin": 0.04, "growth": 0.05, "esg_e": 78, "esg_s": 82, "esg_g": 87, "beta": 1.25, "rating": "A-"},
    {"ticker": "QCOM", "name": "QUALCOMM Inc.", "sector": "Technology", "industry": "Semiconductors", "ceo": "Cristiano Amon", "founded": 1985, "hq": "San Diego, CA", "base_rev": 35000, "margin": 0.21, "growth": 0.08, "esg_e": 80, "esg_s": 75, "esg_g": 84, "beta": 1.22, "rating": "A"},
    {"ticker": "INTC", "name": "Intel Corp.", "sector": "Technology", "industry": "Semiconductors", "ceo": "Pat Gelsinger", "founded": 1968, "hq": "Santa Clara, CA", "base_rev": 54000, "margin": 0.02, "growth": -0.02, "esg_e": 85, "esg_s": 76, "esg_g": 82, "beta": 1.20, "rating": "A-"},
    {"ticker": "CSCO", "name": "Cisco Systems Inc.", "sector": "Technology", "industry": "Communication Equipment", "ceo": "Chuck Robbins", "founded": 1984, "hq": "San Jose, CA", "base_rev": 56000, "margin": 0.22, "growth": 0.03, "esg_e": 87, "esg_s": 82, "esg_g": 88, "beta": 0.90, "rating": "AA"},
    {"ticker": "SBUX", "name": "Starbucks Corp.", "sector": "Consumer Discretionary", "industry": "Restaurants", "ceo": "Laxman Narasimhan", "founded": 1971, "hq": "Seattle, WA", "base_rev": 36000, "margin": 0.11, "growth": 0.08, "esg_e": 80, "esg_s": 78, "esg_g": 83, "beta": 0.95, "rating": "A-"},
    {"ticker": "CAT", "name": "Caterpillar Inc.", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "ceo": "D. James Umpleby III", "founded": 1925, "hq": "Deerfield, IL", "base_rev": 67000, "margin": 0.15, "growth": 0.06, "esg_e": 71, "esg_s": 74, "esg_g": 80, "beta": 1.15, "rating": "A"},
    {"ticker": "GE", "name": "General Electric Co.", "sector": "Industrials", "industry": "Specialty Industrial Machinery", "ceo": "H. Lawrence Culp Jr.", "founded": 1892, "hq": "Boston, MA", "base_rev": 68000, "margin": 0.12, "growth": 0.09, "esg_e": 76, "esg_s": 75, "esg_g": 82, "beta": 1.22, "rating": "BBB+"},
    {"ticker": "MCD", "name": "McDonald's Corp.", "sector": "Consumer Discretionary", "industry": "Restaurants", "ceo": "Chris Kempczinski", "founded": 1955, "hq": "Chicago, IL", "base_rev": 25000, "margin": 0.33, "growth": 0.06, "esg_e": 75, "esg_s": 79, "esg_g": 84, "beta": 0.68, "rating": "A"},
    {"ticker": "VZ", "name": "Verizon Communications", "sector": "Communication Services", "industry": "Telecom Services", "ceo": "Hans Vestberg", "founded": 1983, "hq": "New York, NY", "base_rev": 134000, "margin": 0.09, "growth": 0.02, "esg_e": 78, "esg_s": 74, "esg_g": 80, "beta": 0.40, "rating": "A-"},
    {"ticker": "CMG", "name": "Chipotle Mexican Grill", "sector": "Consumer Discretionary", "industry": "Restaurants", "ceo": "Brian Niccol", "founded": 1993, "hq": "Newport Beach, CA", "base_rev": 10000, "margin": 0.12, "growth": 0.15, "esg_e": 79, "esg_s": 75, "esg_g": 81, "beta": 1.30, "rating": "A-"},
    {"ticker": "PFE", "name": "Pfizer Inc.", "sector": "Healthcare", "industry": "Drug Manufacturers-General", "ceo": "Albert Bourla", "founded": 1849, "hq": "New York, NY", "base_rev": 58000, "margin": 0.08, "growth": -0.25, "esg_e": 74, "esg_s": 79, "esg_g": 83, "beta": 0.62, "rating": "A+"},
    {"ticker": "IBM", "name": "International Business Machines", "sector": "Technology", "industry": "Information Technology Services", "ceo": "Arvind Krishna", "founded": 1911, "hq": "Armonk, NY", "base_rev": 62000, "margin": 0.12, "growth": 0.04, "esg_e": 86, "esg_s": 81, "esg_g": 89, "beta": 0.70, "rating": "A-"},
    {"ticker": "MS", "name": "Morgan Stanley", "sector": "Financials", "industry": "Capital Markets", "ceo": "Ted Pick", "founded": 1935, "hq": "New York, NY", "base_rev": 54000, "margin": 0.17, "growth": 0.05, "esg_e": 72, "esg_s": 77, "esg_g": 86, "beta": 1.25, "rating": "A+"},
    {"ticker": "GS", "name": "Goldman Sachs Group Inc.", "sector": "Financials", "industry": "Capital Markets", "ceo": "David Solomon", "founded": 1869, "hq": "New York, NY", "base_rev": 46000, "margin": 0.18, "growth": 0.04, "esg_e": 69, "esg_s": 75, "esg_g": 85, "beta": 1.30, "rating": "A+"},
    {"ticker": "PYPL", "name": "PayPal Holdings Inc.", "sector": "Financials", "industry": "Credit Services", "ceo": "Alex Chriss", "founded": 1998, "hq": "San Jose, CA", "base_rev": 30000, "margin": 0.14, "growth": 0.08, "esg_e": 78, "esg_s": 80, "esg_g": 85, "beta": 1.35, "rating": "A"},
    {"ticker": "TXN", "name": "Texas Instruments Inc.", "sector": "Technology", "industry": "Semiconductors", "ceo": "Haviv Ilan", "founded": 1930, "hq": "Dallas, TX", "base_rev": 17000, "margin": 0.38, "growth": -0.05, "esg_e": 82, "esg_s": 78, "esg_g": 86, "beta": 1.08, "rating": "AA"},
    {"ticker": "HON", "name": "Honeywell International Inc.", "sector": "Industrials", "industry": "Conglomerates", "ceo": "Vimal Kapur", "founded": 1906, "hq": "Charlotte, NC", "base_rev": 37000, "margin": 0.15, "growth": 0.04, "esg_e": 77, "esg_s": 75, "esg_g": 82, "beta": 1.05, "rating": "A"},
    {"ticker": "UNP", "name": "Union Pacific Corp.", "sector": "Industrials", "industry": "Railroads", "ceo": "Jim Vena", "founded": 1862, "hq": "Omaha, NE", "base_rev": 24000, "margin": 0.27, "growth": 0.02, "esg_e": 68, "esg_s": 72, "esg_g": 80, "beta": 0.82, "rating": "A-"},
    {"ticker": "COP", "name": "ConocoPhillips", "sector": "Energy", "industry": "Oil & Gas E&P", "ceo": "Ryan Lance", "founded": 1917, "hq": "Houston, TX", "base_rev": 58000, "margin": 0.19, "growth": -0.06, "esg_e": 65, "esg_s": 70, "esg_g": 79, "beta": 1.28, "rating": "A-"}
]

# Structure the database mapping tickers to rich details
COMPANIES_DB = {}

# Generate details dynamically
for c in COMPANIES:
    ticker = c["ticker"]
    rev = c["base_rev"]
    margin = c["margin"]
    growth = c["growth"]
    
    # Financial statements
    stmt_2023 = {
        "revenue": rev * 0.92,
        "net_income": rev * 0.92 * margin,
        "ebitda": rev * 0.92 * margin * 1.45,
        "cash": rev * 0.92 * 0.18,
        "debt": rev * 0.92 * 0.15
    }
    
    stmt_2024 = {
        "revenue": rev,
        "net_income": rev * margin,
        "ebitda": rev * margin * 1.5,
        "cash": rev * 0.20,
        "debt": rev * 0.16
    }
    
    stmt_2025 = {
        "revenue": rev * (1 + growth),
        "net_income": rev * (1 + growth) * margin * 1.05,
        "ebitda": rev * (1 + growth) * margin * 1.55,
        "cash": rev * (1 + growth) * 0.22,
        "debt": rev * 0.14
    }
    
    # Projections for 2026
    proj_2026 = {
        "revenue": stmt_2025["revenue"] * (1 + growth * 0.9),
        "net_income": stmt_2025["net_income"] * (1 + growth * 0.9),
        "ebitda": stmt_2025["ebitda"] * (1 + growth * 0.9),
        "cash": stmt_2025["cash"] * 1.1,
        "debt": stmt_2025["debt"] * 0.95
    }
    
    # Peers
    peers = [x["ticker"] for x in COMPANIES if x["sector"] == c["sector"] and x["ticker"] != ticker][:4]
    if not peers:
        peers = ["AAPL", "MSFT", "GOOGL"]
        
    # M&A
    ma_targets = {
        "Technology": ("Sigma Analytics", 4200, "Strengthen cloud computing & security pipelines."),
        "Financials": ("Apex Wealth Management", 1800, "Increase retail investment asset under management."),
        "Healthcare": ("BioGenic Research Labs", 2600, "Acquire proprietary mRNA therapy patents."),
        "Consumer Discretionary": ("Swift Logistics Inc.", 950, "Accelerate next-day supply chain deliveries."),
        "Consumer Staples": ("PureHarvest Organics", 600, "Expand organic product shelf holdings."),
        "Energy": ("ClearSky Geothermal", 1200, "Diversify into alternative low-carbon portfolios."),
        "Industrials": ("RoboControl Systems", 1500, "Introduce AI-powered manufacturing machinery automation.")
    }
    ma_info = ma_targets.get(c["sector"], ("Global Solutions", 500, "Expand geographic presence."))
    
    COMPANIES_DB[ticker] = {
        "ticker": ticker,
        "name": c["name"],
        "sector": c["sector"],
        "industry": c["industry"],
        "ceo": c["ceo"],
        "founded": c["founded"],
        "hq": c["hq"],
        "credit_rating": c["rating"],
        "beta": c["beta"],
        "financials": {
            "2023": stmt_2023,
            "2024": stmt_2024,
            "2025": stmt_2025,
            "2026_proj": proj_2026
        },
        "analyst_estimates": {
            "consensus": "Buy" if growth > 0.08 else "Hold",
            "target_price": 150.00 * (1 + growth) if ticker != "BRK.A" else 620000.0,
            "eps_2025": (stmt_2025["net_income"] / 500) if ticker != "BRK.A" else (stmt_2025["net_income"] / 1.5),
            "eps_2026_est": (proj_2026["net_income"] / 490) if ticker != "BRK.A" else (proj_2026["net_income"] / 1.45),
            "num_analysts": 35
        },
        "peer_group": peers,
        "ownership": {
            "institutional": 74.2 if ticker != "TSLA" else 42.5,
            "insider": 1.5 if ticker != "TSLA" else 20.8,
            "top_shareholders": [
                {"name": "The Vanguard Group", "holding": 8.4},
                {"name": "BlackRock Inc.", "holding": 7.2},
                {"name": "Fidelity Management", "holding": 4.5}
            ]
        },
        "esg_scores": {
            "environmental": c["esg_e"],
            "social": c["esg_s"],
            "governance": c["esg_g"],
            "overall": int(c["esg_e"] * 0.4 + c["esg_s"] * 0.3 + c["esg_g"] * 0.3)
        },
        "earnings_call": {
            "transcript_summary": f"Key themes: robust cloud expansion, cost optimization efforts, and strong pipeline demand. Margin resilience noted despite supply-chain friction.",
            "sentiment": "Highly Positive" if growth > 0.08 else "Neutral",
            "key_quote": f"\"Our capital structure remains strong, and we are confident in our long-term growth vectors heading into fiscal 2026.\""
        },
        "macro_sensitivity": {
            "interest_rates": "Low" if c["sector"] in ["Technology", "Healthcare"] else "High",
            "inflation": "Medium",
            "gdp_correlation": "High" if c["sector"] in ["Financials", "Industrials", "Consumer Discretionary"] else "Low"
        },
        "industry_benchmarks": {
            "avg_margin": 0.18,
            "avg_growth": 0.06,
            "avg_debt_equity": 0.45
        },
        "ma_history": {
            "target": ma_info[0],
            "value_m": ma_info[1],
            "rationale": ma_info[2]
        }
    }
