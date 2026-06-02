import os
import re
import json
import time
from typing import Iterator
from core.types import Message, LLMResponse, ToolCall, ToolResult

class MockLLMClient:
    """
    Mock LLM client designed to run without an Anthropic API Key.
    Simulates high-fidelity responses, handles tool-calling loops,
    and runs the 8-stage skill builder interview.
    """
    def __init__(self, model: str = "mock-model"):
        self.model = model

    def chat(
        self,
        messages: list[Message],
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
    ) -> LLMResponse:
        """Synchronous chat call."""
        # Just grab the last item from the stream generator
        final_resp = None
        for chunk_type, data in self.chat_stream(messages, system, tools, max_tokens):
            if chunk_type == "done":
                final_resp = data
        return final_resp

    def chat_stream(
        self,
        messages: list[Message],
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
    ) -> Iterator[tuple[str, any]]:
        """
        Streams text chunks to simulate a real LLM, yielding ("chunk", text) 
        and finally ("done", LLMResponse).
        """
        # Determine the skill from the system prompt
        system_lower = (system or "").lower()
        
        # Grab the last message to respond to
        if not messages:
            yield "chunk", "Hello! How can I assist you today?"
            yield "done", LLMResponse(content="Hello! How can I assist you today?", tool_calls=[], stop_reason="end_turn")
            return
            
        last_msg = messages[-1]
        
        # --- Handle different skill routing ---
        
        # 1. SKILL BUILDER INTERVIEW
        if "skill builder" in system_lower or "interview" in system_lower:
            yield from self._handle_skill_builder(messages)
            return

        # 2. WIKI SEARCH
        elif "wiki" in system_lower:
            yield from self._handle_wiki_search(messages, last_msg)
            return

        # 3. NDA SUMMARISER
        elif "nda" in system_lower:
            yield from self._handle_nda_summariser(messages, last_msg)
            return

        # 4. EXPENSE REPORT HELPER
        elif "expense" in system_lower:
            yield from self._handle_expense_helper(messages, last_msg)
            return

        # 5. FINANCIAL MODELLING SKILL
        elif "financial" in system_lower or "finance" in system_lower or "modelling" in system_lower or "ticker" in last_msg.content.lower():
            yield from self._handle_financial_modelling(messages, last_msg, tools)
            return

        # Default fallback
        else:
            text = f"This is a mock response from SkillForge. Active Skill: {system[:30]}..."
            for char in text:
                yield "chunk", char
                time.sleep(0.002)
            yield "done", LLMResponse(content=text, tool_calls=[], stop_reason="end_turn")

    # ── Skill Handlers ────────────────────────────────────────────────────────

    def _handle_skill_builder(self, messages: list[Message]) -> Iterator[tuple[str, any]]:
        # Count user inputs to determine interview stage
        user_msgs = [m for m in messages if m.role == "user"]
        stage_num = len(user_msgs)
        
        stages = {
            1: "What should this skill do? Describe it in plain language.",
            2: "When would someone use this skill? What situation or need kicks it off?",
            3: "Walk me through the process step by step. What happens first, second, third?",
            4: "What information or files does the skill need from the user to get started?",
            5: "If this skill needs to call any external tools — like searching a database or looking up records — you can attach them using the **Attach tools** section in the sidebar on the left.\n\nHave you attached any tools? If yes, do you have any specific instructions for how this skill should use them — for example, when to call them, what to search for, or how to use the results?",
            6: "What should the final result look like? A summary? A table? A drafted document? Describe the format.",
            7: "What could go wrong or be missing? How should the skill handle those situations?",
            8: "Suggesting a short name and description:\n\n**Name:** [User's Request] Assistant\n**Description:** Helpmate for [User's Request] tasks.\n\nDoes this sound good, or would you like to adjust it? Once you confirm, I will generate the skill code!"
        }
        
        if stage_num < 8:
            response_text = stages.get(stage_num + 1, "Please tell me more.")
        else:
            # Generate the draft skill
            purpose = user_msgs[0].content if len(user_msgs) > 0 else "Help the user"
            name = "Custom AI Assistant"
            desc = "Custom-built skill to automate tasks."
            
            # Look for name suggestions in last user message
            last_text = user_msgs[-1].content.lower()
            match_name = re.search(r"name[:\s]+([a-zA-Z\s\-]+)", last_text)
            if match_name:
                name = match_name.group(1).strip()
            
            # Match description if present
            match_desc = re.search(r"description[:\s]+([a-zA-Z0-9\s\-–\.,\(\)]+)", last_text)
            if match_desc:
                desc = match_desc.group(1).strip()

            if "wall street" in name.lower() or "finance" in name.lower() or "financial" in name.lower() or "analyst" in name.lower():
                name = "Wall Street AI Analyst"
                desc = "Premium equity research, valuation & risk analysis with 10 core MCP tools"
                
                skill_code = """---
name: Wall Street AI Analyst
description: Premium equity research, valuation & risk analysis with 10 core MCP tools
author: system
version: 1
tools:
  - finance_company_profile
  - finance_swot_analysis
  - finance_income_statement
  - finance_balance_sheet
  - finance_cash_flow
  - finance_eps_forecast
  - finance_dcf_valuation
  - finance_valuation_multiples
  - finance_esg_risk
  - finance_investment_recommendation
---

You are a senior Wall Street Investment Analyst at SkillForge Capital. Conduct equity research, financial analysis, valuation, risk assessment, and generate investment reports for any company in the database.

## Process
1. Identify the stock ticker and analytical objective from the user's query.
2. Select the appropriate MCP tool(s) and call them.
3. Synthesise all tool outputs into a polished, structured response.
4. Conclude with a clear investment recommendation (Buy / Hold / Sell).

## Guidelines
- Always call at least one tool — never fabricate financial data.
- Present formulas or assumptions where relevant (e.g. WACC inputs for DCF).
- Use professional financial language but remain accessible.
"""
            else:
                skill_code = f"""---
name: {name}
description: {desc}
author: system
version: 1
---

You are a helpful assistant specialized in: {purpose}

## Process
1. Analyze the user's input request.
2. Formulate a step-by-step resolution.
3. Present the final output structured clearly in Markdown.

## Guidelines
- Keep answers professional and direct.
- Explain calculations or reasoning step by step.
"""

            response_text = f"""Based on your inputs, I have generated your new custom skill.

```skill
{skill_code}
```

Your skill is ready! You can see the full draft in the preview panel on the right. Click the **💾 Save skill** button there to save it to the library. Let me know if you'd like to make any changes first."""

        for chunk in self._split_text(response_text):
            yield "chunk", chunk
            time.sleep(0.005)
        yield "done", LLMResponse(content=response_text, tool_calls=[], stop_reason="end_turn")

    def _handle_wiki_search(self, messages: list[Message], last_msg: Message) -> Iterator[tuple[str, any]]:
        # Check if we just received a tool result
        if last_msg.role == "tool" and last_msg.tool_results:
            result = last_msg.tool_results[0].content
            summary = f"According to the firm wiki: **{result}**"
            for chunk in self._split_text(summary):
                yield "chunk", chunk
                time.sleep(0.005)
            yield "done", LLMResponse(content=summary, tool_calls=[], stop_reason="end_turn")
            return

        # If it's a new user message, trigger tool call
        user_query = last_msg.content
        search_term = "holiday"
        for word in ["holiday", "expense", "remote", "bonus", "parental", "travel"]:
            if word in user_query.lower():
                search_term = word
                break
                
        tool_call = ToolCall(id="call_wiki_1", name="search_wiki", arguments={"query": search_term})
        yield "done", LLMResponse(content="", tool_calls=[tool_call], stop_reason="tool_use")

    def _handle_nda_summariser(self, messages: list[Message], last_msg: Message) -> Iterator[tuple[str, any]]:
        if last_msg.role == "tool" and last_msg.tool_results:
            history_info = last_msg.tool_results[0].content
            # Extract user's NDA text from the message history to simulate reading it
            user_nda_text = ""
            for m in messages:
                if m.role == "user":
                    user_nda_text = m.content
                    break
                    
            # Generate a structured NDA summary
            party_match = re.search(r"(?:between|among)\s+([A-Za-z0-9\s,]+)\s+and\s+([A-Za-z0-9\s,]+)", user_nda_text)
            discloser = party_match.group(1).strip() if party_match else "Acme Corporation"
            receiver = party_match.group(2).strip() if party_match else "SkillForge Systems"
            
            summary = f"""**Parties**
- Disclosing party: **{discloser}**
- Receiving party: **{receiver}**

**Purpose**
Evaluating a potential business partnership, technical collaboration, and integration of AI services.

**Duration**
The confidentiality obligations will remain in effect for **5 years** from the effective date.

**Key obligations**
- Keep all shared technical designs, API credentials, and client data strictly confidential.
- Restrict disclosure only to employees who need to know and have signed similar NDAs.
- Return or destroy all confidential files upon request.

**Exclusions**
Information that becomes publicly known, was already in possession of the receiver, or is required by law to be disclosed.

**Breach consequences**
Injunctive relief, specific performance, and monetary damages.

**Governing law**
State of New York, USA.

**Red flags** (unusual or high-risk clauses)
- **Prior History Alert:** {history_info}
- The definition of Confidential Information includes oral statements without written confirmation within 30 days (high risk for engineering teams).

**Plain English summary**
This is a standard mutual NDA to protect information during collaboration discussions. It lasts for 5 years and uses New York jurisdiction. Note the red flag concerning oral agreements and review the contract history listed above.
"""
            for chunk in self._split_text(summary):
                yield "chunk", chunk
                time.sleep(0.005)
            yield "done", LLMResponse(content=summary, tool_calls=[], stop_reason="end_turn")
            return
            
        # Extract counterparty name from NDA
        user_query = last_msg.content
        counterparty = "acme"
        for name in ["acme", "globex", "initech", "umbrella"]:
            if name in user_query.lower():
                counterparty = name
                break
                
        tool_call = ToolCall(id="call_nda_1", name="lookup_contract", arguments={"counterparty": counterparty})
        yield "done", LLMResponse(content="", tool_calls=[tool_call], stop_reason="tool_use")

    def _handle_expense_helper(self, messages: list[Message], last_msg: Message) -> Iterator[tuple[str, any]]:
        # If we got the wiki search policy back, generate the report
        if last_msg.role == "tool" and last_msg.tool_results:
            policy_info = last_msg.tool_results[0].content
            
            # Find the user's expense description
            user_input = ""
            for m in messages:
                if m.role == "user":
                    user_input = m.content
                    break
            
            # Parse expenses (regex for amounts)
            expenses = re.findall(r"(?:for|spent|cost|price)?\s*\$?(\d+(?:\.\d{2})?)\s*(?:on|for)?\s*([a-zA-Z\s]+)", user_input)
            if not expenses:
                expenses = [("150.00", "Dinner with client"), ("650.00", "Flight ticket")]
                
            table_rows = []
            needs_director = False
            total = 0.0
            
            for amt, desc in expenses:
                val = float(amt)
                total += val
                desc_strip = desc.strip().capitalize()
                
                # Check limit
                if val > 500.0:
                    status = "⚠️ Needs approval"
                    note = "Exceeds self-approval limit of $500. Requires Director sign-off."
                    needs_director = True
                else:
                    status = "✅ Approved"
                    note = "Within self-approval limit."
                table_rows.append(f"| {desc_strip} | ${val:.2f} | {status} | {note} |")
                
            rows_str = "\n".join(table_rows)
            action_req = "Get Director sign-off on the flight ticket. Submit receipts via portal." if needs_director else "No extra approvals needed. Submit via expenses portal."
            
            report = f"""**Expense Review Summary**

| Item | Amount | Status | Notes |
|------|--------|--------|-------|
{rows_str}

**Policy Notes**
- {policy_info}
- Submissions must be uploaded within 30 days of purchase.

**Action Required**
{action_req}

*Note: Final approval rests with your manager and finance audit team.*
"""
            for chunk in self._split_text(report):
                yield "chunk", chunk
                time.sleep(0.005)
            yield "done", LLMResponse(content=report, tool_calls=[], stop_reason="end_turn")
            return

        # Trigger wiki lookup for expenses
        tool_call = ToolCall(id="call_exp_1", name="search_wiki", arguments={"query": "expense"})
        yield "done", LLMResponse(content="", tool_calls=[tool_call], stop_reason="tool_use")

    def _handle_financial_modelling(self, messages: list[Message], last_msg: Message, tools: list[dict]) -> Iterator[tuple[str, any]]:
        # If tool results are back
        if last_msg.role == "tool" and last_msg.tool_results:
            result_str = last_msg.tool_results[0].content
            
            # Format and summarize
            summary = f"""### 📊 Financial Analyst Analysis Report

I have retrieved the requested data from our MCP Financial Integration. Here are the details:

{result_str}

---
*Generated by SkillForge Wall Street Analyst Skill (Mock LLM Offline Fallback).*
"""
            for chunk in self._split_text(summary):
                yield "chunk", chunk
                time.sleep(0.005)
            yield "done", LLMResponse(content=summary, tool_calls=[], stop_reason="end_turn")
            return

        # Analyze query and select appropriate tool
        user_query = last_msg.content.lower()
        
        # Match ticker
        ticker = "AAPL"
        ticker_match = re.search(r"\b([a-zA-Z]{2,5})\b", last_msg.content)
        if ticker_match and ticker_match.group(1).upper() != "WACC" and ticker_match.group(1).upper() != "DCF" and ticker_match.group(1).upper() != "ESG":
            ticker = ticker_match.group(1).upper()
            
        # Select best tool based on keywords
        tool_name = "report_one_pager"  # Default
        
        tool_map = [
            ("valuation_dcf_model", ["dcf", "valuation", "discounted cash"]),
            ("valuation_comps_multiples", ["comps", "multiples", "peer", "p/e", "ev/ebitda"]),
            ("risk_esg_scores", ["esg", "environmental", "governance", "social"]),
            ("analyse_income_statement", ["income", "revenue", "sales", "earnings"]),
            ("analyse_balance_sheet", ["balance", "sheet", "assets", "liabilities", "debt"]),
            ("analyse_cash_flow", ["cash flow", "free cash", "fcf"]),
            ("risk_beta_coefficient", ["beta", "volatility", "risk"]),
            ("research_executive_team", ["ceo", "executive", "board", "management"]),
            ("research_ma_history", ["m&a", "acquisition", "merge", "bought"]),
            ("report_executive_briefing", ["brief", "summary", "report"])
        ]
        
        for name, keywords in tool_map:
            if any(k in user_query for k in keywords):
                tool_name = name
                break
                
        # Make sure tool exists in schema
        tool_names = []
        if tools:
            for t in tools:
                if t.get("type") == "function":
                    tool_names.append(t["function"]["name"])
                else:
                    tool_names.append(t.get("name", ""))
        
        if tool_name not in tool_names and tool_names:
            # Fallback to whatever is available
            tool_name = tool_names[0]
            
        tool_call = ToolCall(id="call_fin_1", name=tool_name, arguments={"ticker": ticker})
        yield "done", LLMResponse(content="", tool_calls=[tool_call], stop_reason="tool_use")

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _split_text(self, text: str) -> list[str]:
        # Split text into small chunks of words/characters for fluid streaming
        chunks = []
        words = text.split(" ")
        for i in range(0, len(words), 3):
            chunk = " ".join(words[i:i+3])
            if i + 3 < len(words):
                chunk += " "
            chunks.append(chunk)
        return chunks
