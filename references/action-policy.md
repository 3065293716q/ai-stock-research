# Action and execution policy

## Decision hierarchy

Decide in this order:

1. Verify security identity, data freshness and tradability.
2. Check fatal red lines and thesis health.
3. Estimate value under bear/base/bull scenarios.
4. Assess market timing and event risk.
5. Apply position, cost, concentration, cash and legal-order constraints.
6. Select one current action and convert it into quantities.

## Action meanings

- `BUY`: no position; evidence and price/timing justify opening now.
- `ADD`: existing position; thesis intact, valuation attractive, concentration acceptable and the new lot improves expected asymmetry.
- `HOLD`: existing position; thesis intact and neither buy nor sell trigger is active.
- `WAIT`: do not transact; name the exact event or price confirmation required.
- `REDUCE`: sell a legal, meaningful portion because risk/concentration/valuation worsened but the thesis is not fully broken.
- `SELL`: exit all sellable shares because thesis/red-line/opportunity-cost evidence warrants it.

## Default rules

- `BUY/ADD` requires no fatal red line, at least medium evidence confidence, a quantified downside case, adequate margin of safety and an executable trigger.
- `SELL` follows a verified thesis break, fatal red line, unacceptable risk, or decisively inferior opportunity cost. Do not wait for break-even.
- `REDUCE` is allowed only when remaining shares form a sensible position and the market's order rules permit it. For a single 100-share SSE/SZSE lot, use `HOLD` or `SELL`, not `REDUCE`.
- `WAIT` is a valid decisive action. Include the trigger that changes it to `BUY`, `HOLD`, or `SELL`.
- Never recommend chasing a large one-day move without a new value estimate and market confirmation.

## Level construction

Provide:

1. `Now`: current action and executable quantity.
2. `Entry zone`: valuation-supported range; include a no-chase ceiling.
3. `Confirmation`: dated price/volume or event condition.
4. `Add rule`: a second legal lot only if thesis and concentration checks still pass.
5. `Failure rule`: price and/or fundamental invalidation; specify whether it triggers review or immediate exit.
6. `Profit/valuation rule`: target zone, valuation excess or trailing condition for reduction/exit.
7. `Review date`: next filing, catalyst or maximum validity period.

Do not set every exit as a fixed percentage below entry. Separate:

- a trading stop for a short-horizon setup;
- a thesis stop for fundamental impairment;
- a valuation exit for excessive expectations;
- a portfolio exit for concentration/opportunity cost.

## Position sizing

Use the lower of:

- allocation cap: portfolio value × maximum target weight;
- cash budget;
- risk cap: portfolio value × risk fraction ÷ (entry price − executable risk level), when a meaningful price risk level exists.

Round to legal units with `scripts/trade_units.py`. State that gaps and price limits can produce losses beyond the nominal risk level.

## Confidence

Report separate confidence for:

- evidence quality;
- business/valuation thesis;
- timing/execution.

Do not compress them into one unexplained number.

