---
name: ai-stock-research
description: Research and evaluate A-share and U.S. stocks with current-data verification, multi-angle fundamental/industry/valuation/technical/risk analysis, bull-bear challenge, position-aware decision making, and executable trading discipline. Use when Codex needs to analyze a stock or holding, decide what to do now, assess whether to buy/add/hold/reduce/sell/wait, define entry and exit timing, calculate A-share 100-share lot orders, review earnings or price moves, compare a thesis with new evidence, or create a disciplined A-share/U.S.-stock action plan.
---

# AI Stock Research

Deliver evidence-backed research and finish with one clear, executable action. Treat the system as decision support, not an autonomous trading system or a promise of returns.

## Start every run

1. Confirm the current date, timezone, ticker, company identity, exchange, listing board, currency, and analysis horizon.
2. Determine the user's state: no position or holding; shares; sellable shares; average cost; cash available; portfolio size; maximum acceptable loss; account type; and whether any shares were bought today.
3. Do not block on missing optional details. Use conservative defaults, label them, and provide both an unpositioned plan and a position-aware adjustment. Ask only when ticker identity is ambiguous or a missing fact would reverse the action.
4. Browse for anything current or decision-critical. Prefer primary sources. State quote and data timestamps.
5. Read [references/data-sources.md](references/data-sources.md). Read [references/market-rules.md](references/market-rules.md) for execution. Read [references/action-policy.md](references/action-policy.md) before deciding. Use [references/report-template.md](references/report-template.md) for the final answer.

## Choose depth

- **Quick screen**: Use when the user asks for a fast view or supplies many tickers. Check identity, latest event, financial quality, valuation, trend, and red flags. End with `DEEP RESEARCH / WATCH / REJECT`.
- **Full research**: Default for one stock or a buy/sell question. Run the full workflow below.
- **Event update**: Use for earnings, announcements, or abnormal price moves. Compare the event with the existing thesis and decide whether it is a value event, expectation reset, liquidity/technical move, or unresolved.
- **Thesis review**: Use when prior research or a cost basis exists. Test each original assumption and red line; do not rewrite history to fit the latest price.

## Build a verified evidence packet

Collect and timestamp:

- current and recent adjusted price/volume history, benchmark and sector-relative returns;
- latest annual and interim filings, earnings release, guidance, and material announcements;
- 3-5 year revenue, margins, operating income, net income, operating cash flow, capex, free cash flow, ROE/ROIC, cash and debt;
- share count, dilution, buybacks, dividends, insider/major-holder transactions;
- segment economics, customers, suppliers, competitors, industry cycle, policy and macro exposures;
- valuation history, relevant peers, consensus only as a comparison, and major catalysts/risks.

For exact numbers, follow these controls:

- Use the filing/exchange as the canonical source and at least one independent cross-check for every decision-critical value.
- Distinguish GAAP from adjusted measures and reported currency from converted currency.
- Treat two websites fed by the same vendor as one source.
- Never use future information in historical analysis. State the latest trading row actually used.
- Use `scripts/research_math.py`; do not rely on mental arithmetic for market cap, cross-source variance, valuation, or scenarios.
- If critical values disagree by more than 1%, investigate accounting period, units, share class, FX, restatement, and GAAP/non-GAAP definitions. Do not average incompatible values.
- Label each substantive statement `Fact`, `Inference`, or `Scenario` while drafting. The final prose may be natural, but retain source links and uncertainty.

Rate researchability:

- `A`: abundant primary data; emphasize non-consensus evidence and disconfirmation.
- `B`: adequate but incomplete; identify estimates and confidence.
- `C`: sparse/new/opaque; do not fill gaps with plausible prose. Return `WAIT` when missing evidence prevents a responsible trade.

## Run the research team

When multi-agent tools are available and the request is full research, run independent analysts in parallel. Give each the ticker, date, market, horizon, evidence standards, and user position, but do not leak the other analysts' conclusions.

1. **Business analyst**: business model, segment economics, moat, unit economics, reinvestment runway.
2. **Financial/valuation analyst**: accounting quality, cash conversion, balance sheet, dilution, normalized earnings, valuation scenarios.
3. **Industry/management analyst**: cycle, competitors, policy, management credibility, governance, capital allocation.
4. **Market/risk analyst**: verified price/volume structure, relative strength, catalysts, positioning, downside paths, execution constraints.

If multi-agent tools are unavailable, execute the same four passes sequentially. Do not pretend parallel agents ran.

Then perform two adversarial passes:

- **Bull case**: state the strongest evidence-based upside case and what the market may underappreciate.
- **Bear case / pre-mortem**: state how the investment loses money, what would falsify the thesis, and why a smart investor would avoid or short it.

Have the lead resolve conflicts by evidence quality, not by averaging scores. Preserve unresolved disagreement in the final confidence rating.

## Analyze in decision order

1. **Business quality**: Explain in one sentence how the company makes money. Test pricing power, switching costs, network effects, scale, regulation, cyclicality, and capital intensity.
2. **Financial quality**: Normalize earnings; inspect cash conversion, working capital, leverage, returns on capital, dilution, and one-offs. Flag accounting or governance red lines.
3. **Industry and management**: Judge cycle position, competitive direction, management promises versus delivery, and capital allocation.
4. **Valuation**: Use at least two appropriate methods. Prefer DCF/owner earnings for stable cash generators, normalized multiples for cyclicals, unit economics plus scenarios for growth firms, and asset value for financial/resource businesses. Run bear/base/bull assumptions with `scripts/research_math.py scenario`.
5. **Market structure**: Use adjusted history consistently for trends. Check benchmark-relative strength, volume, 20/50/200-day structure when available, volatility, gaps, support/resistance backed by dated observations, and event risk. Technicals time the trade; they do not override a broken thesis.
6. **Position context**: Compare current price with cost, position weight, cash, concentration, tax/account constraints, and opportunity cost. Never anchor a hold decision solely to break-even.

Read [references/research-framework.md](references/research-framework.md) for scoring and red-line details.

## Produce a disciplined action

Choose exactly one current action:

- `BUY` — open a position now or at a stated near-term entry condition;
- `ADD` — increase an existing position;
- `HOLD` — keep the position and do nothing now;
- `WAIT` — do not trade until a named price/event confirmation;
- `REDUCE` — sell an executable portion only when position size and lot rules make this meaningful;
- `SELL` — exit all sellable shares; state how to handle temporarily unsellable shares.

Do not use `HOLD` as a refuge. If evidence is insufficient, choose `WAIT`. If the thesis is broken or a fatal red line is verified, valuation cheapness alone does not prevent `SELL`.

Define three separate levels:

- **Value level**: price range offering the required margin of safety.
- **Timing level**: market confirmation or pullback condition for execution.
- **Invalidation level**: business, earnings, or price condition that makes the plan wrong.

Never invent a precise level. Derive it from verified valuation, dated market structure, volatility, and catalysts. Use ranges when precision is not supported. State the plan's validity window and next review event.

## Convert judgment into legal orders

For A shares, always read [references/market-rules.md](references/market-rules.md) and run `scripts/trade_units.py` before recommending quantities.

- Buying through auction trading normally requires 100 shares or an integer multiple.
- A 100-share holding normally cannot be partially reduced; the meaningful choices are hold or sell all 100.
- A larger round-lot holding can be partially sold in 100-share units when partial de-risking is justified.
- If an odd-lot balance exists, do not split the odd-lot remainder across multiple sell orders; validate the proposed sell quantity.
- Respect T+1 sellability: shares bought today may be held but unavailable to sell today.
- Distinguish theoretical stop levels from executable exits during limit-down, suspension, or illiquidity.

Use all-or-nothing by default when the holding is one lot, when a partial order would be uneconomic, or when the thesis is binary. Use staged orders only when the user owns enough legal lots and valuation/uncertainty genuinely supports staging.

For U.S. stocks, do not impose the A-share 100-share minimum. Check broker support for fractional shares, account type, settlement, day-trading, short-sale, tax, and extended-hours constraints when relevant.

## Persist learning when authorized

When the user asks to save research, write:

- `reports/<ticker>/<date>-research.md` for the report;
- `reports/<ticker>/thesis.md` for the current thesis, 3-7 testable assumptions, red lines, valuation anchors, and review triggers;
- `reports/decision-log.md` for the dated action, benchmark, horizon, and later outcome.

On later reviews, compare the old thesis with new evidence before reading the old action. Record raw return, benchmark-relative return, what held or failed, and one reusable lesson. Never claim a strategy is validated from a handful of decisions.

## Quality gate

Before answering, verify all of the following:

- ticker/company/board/currency and current date are correct;
- latest quote and filings have timestamps and links;
- decision-critical numbers have primary evidence and independent checks;
- valuation arithmetic was computed by script;
- bull and bear cases address each other;
- the current action is singular and justified;
- entry, add, reduce/sell, invalidation, target/review, and no-chase conditions are stated;
- A-share quantities pass the lot/T+1 feasibility check;
- facts, inferences, scenarios, and unknowns are distinguishable;
- no language promises profit, certainty, or guaranteed stop execution.

