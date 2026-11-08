"""Weekly medical watcher: official-source news + deep check of one page."""
import anyio, datetime, glob, os, re
from claude_agent_sdk import ClaudeAgentOptions, query, ResultMessage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
B = os.path.join(ROOT, ".github/bot")

# topic list from page titles
topics = []
for p in sorted(glob.glob(f"{ROOT}/ops/*.html")):
    h = open(p, encoding="utf-8").read()
    m = re.search(r'data-l="ru"[^>]*>\s*(?:<[^>]+>\s*)*([^<]{3,120})', h)
    topics.append(f"- {os.path.basename(p)}: {m.group(1).strip() if m else ''}")
open(f"{B}/topics.md", "w", encoding="utf-8").write("\n".join(topics) + "\n")

pages = sorted(p for p in glob.glob(f"{ROOT}/ops/*.html") if "sitemap" not in p)
week = datetime.date.today().isocalendar()[1]
page = os.path.relpath(pages[week % len(pages)], ROOT)
open(f"{B}/watch_page.txt", "w").write(page + "\n")
if not os.path.exists(f"{B}/watch_seen.md"):
    open(f"{B}/watch_seen.md", "w").write("# Уже найденные источники\n")


async def main():
    opts = ClaudeAgentOptions(
        cwd=ROOT,
        model=os.environ.get("WATCH_MODEL", "claude-opus-5-5"),
        system_prompt=open(f"{B}/WATCH.md", encoding="utf-8").read(),
        max_turns=80,
        max_budget_usd=float(os.environ.get("WATCH_BUDGET_USD", "5")),
        permission_mode="acceptEdits",
        allowed_tools=["Read", "Write", "Edit", "Glob", "Grep",
                       "WebSearch", "WebFetch"],
        setting_sources=[],
    )
    cost = None
    async for m in query(prompt=f"Сегодня {datetime.date.today()}. "
                         f"Страница для глубокой проверки: {page}. Выполни задачу.",
                         options=opts):
        if isinstance(m, ResultMessage):
            cost = m.total_cost_usd
    print(f"COST_USD={cost}")
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as fh:
        fh.write(f"cost={cost}\npage={page}\n")

anyio.run(main)
