"""Runs the site bot with the Claude Agent SDK (paid from Max API credits)."""
import anyio, os, sys
from claude_agent_sdk import (ClaudeAgentOptions, query, AssistantMessage,
                              ResultMessage, TextBlock)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BUDGET = float(os.environ.get("BOT_BUDGET_USD", "2.0"))
MODEL = os.environ.get("BOT_MODEL", "claude-sonnet-5-5")
rules = open(os.path.join(ROOT, ".github/bot/RULES.md"), encoding="utf-8").read()


async def main():
    opts = ClaudeAgentOptions(
        cwd=ROOT,
        model=MODEL,
        system_prompt=rules,
        max_turns=60,
        max_budget_usd=BUDGET,
        permission_mode="acceptEdits",
        allowed_tools=["Read", "Edit", "Write", "Glob", "Grep",
                       "Bash(python3 .github/bot/checks.py)"],
        disallowed_tools=["WebFetch", "WebSearch"],
        setting_sources=[],
    )
    cost = None
    async for m in query(prompt="Выполни сегодняшний проход по правилам.", options=opts):
        if isinstance(m, AssistantMessage):
            for b in m.content:
                if isinstance(b, TextBlock):
                    print(b.text[:500])
        elif isinstance(m, ResultMessage):
            cost = m.total_cost_usd
    print(f"COST_USD={cost}")
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as fh:
        fh.write(f"cost={cost}\n")

anyio.run(main)
