# Market execution rules

Verify current rules at execution time. The following baseline is current as of 2026-07-11 and is not a substitute for the user's broker rules.

## Mainland A shares

### Share quantities

- SSE and SZSE auction buys: 100 shares or an integer multiple.
- If holdings are exact round lots, sell in 100-share multiples.
- If holdings contain an odd-lot remainder below 100 shares, that remainder may be sold once by itself or together with round lots; do not split the odd remainder into multiple odd-lot sells.
- Example: with 500 shares, 200 + 300 is valid; 201 + 299 is not. With 299 shares, 100 + 199 or 200 + 99 can be valid because the 99-share odd remainder is disposed of once.
- BSE differs: each auction order is at least 100 shares and may increase one share at a time. Do not apply the SSE/SZSE integer-multiple rule to BSE without checking the current rule.

Official rules:

- SSE 2026 Trading Rules: https://www.sse.com.cn/lawandrules/sselawsrules2025/trade/universal/c/c_20260424_10816492.shtml
- SSE sell-quantity examples: https://www.sse.com.cn/lawandrules/guide/stock/jyglywznylc/tz/c/c_20230209_5716007.shtml
- SZSE 2026 Trading Rules PDF: https://docs.static.szse.cn/www/lawrules/rule/trade/current/W020260424690713155663.pdf
- BSE Trading Rules: https://www.bse.cn/jygl_list/200010919.html

### Sellability and execution

- Treat ordinary A-share stock purchases as T+1 sellable: shares bought today are generally not available to sell until the next trading day.
- Use broker-displayed `sellable shares` as the executable ceiling; holdings and sellable shares can differ.
- A stop is a decision trigger, not a fill guarantee. Limit-down, suspension, gaps and poor liquidity can prevent execution.
- Check trading status, ex-rights/ex-dividend effects, corporate actions, price cage, call-auction phase and current price limit before placing an order.

### Price limits baseline

- SSE/SZSE main-board ordinary and main-board risk-warning shares: generally 10% under the 2026 rules, subject to exceptions.
- STAR Market and ChiNext: generally 20%; IPO shares generally have no daily price limit for the first five trading days.
- BSE: generally 30%; first trading day may have no daily price limit.
- Other exceptions, delisting periods and special instruments require current rule verification.

Official references:

- SSE 2026 rules and STAR provisions: https://www.sse.com.cn/lawandrules/sselawsrules2025/stocks/exchange/c/c_20260424_10816482.shtml
- SZSE 2026 rule revision explanation: https://docs.static.szse.cn/www/lawrules/rule/allrules/bussiness/W020260424690713346617.pdf
- ChiNext investor rules: https://investor.szse.cn/knowledge/qa/t20200721_579820.html

### Cost and practicality

- Obtain the user's actual commission minimum, transfer fees and taxes from the broker; rates can change and differ by account.
- Reject a nominally legal 100-share trade when fees, spread or illiquidity make it economically meaningless.
- For one-lot positions, choose between holding and selling the full lot; do not recommend an impossible 50-share trim on SSE/SZSE.

## U.S. stocks

- There is no universal 100-share minimum for ordinary retail stock purchases. A 100-share round lot is market terminology, not a required retail order size.
- Whole-share orders can generally start at one share; fractional-share support and order types are broker-specific.
- Standard settlement is T+1, but trading restrictions depend on cash/margin account rules, settled funds, broker policy and current day-trading regulation.
- Check extended-hours liquidity, limit-order use, tax lots, wash-sale exposure, short-sale availability and currency conversion when relevant.

Official settlement reference: https://www.finra.org/investors/insights/understanding-settlement-cycles

