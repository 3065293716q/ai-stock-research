# AI Stock Research

A reusable, evidence-first workflow for researching A-share and U.S. stocks. It combines business, financial, industry, and market analysis with bull/bear review, valuation scenarios, and position-aware decision support.

## Contents

- `SKILL.md` — workflow and research standards
- `references/` — data sources, attribution, market rules, action policy, research framework, and report template
- `scripts/research_math.py` — source reconciliation, valuation, and scenario calculations
- `scripts/trade_units.py` — trade-size and A-share lot checks
- `agents/openai.yaml` — optional assistant interface metadata

## Usage

Read `SKILL.md` and the linked references before running a research task. Python utilities can be invoked directly with `python3 scripts/research_math.py --help` and `python3 scripts/trade_units.py --help`. Verify any market data with current primary sources before making decisions.

This project is decision support for research and education. It does not place trades or guarantee investment outcomes. Upstream ideas and licenses are credited in `references/attribution.md`.
