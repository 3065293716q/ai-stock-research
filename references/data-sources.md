# Data and source discipline

## Source hierarchy

Use primary sources before aggregators.

### A shares

1. Exchange and disclosure: SSE, SZSE, BSE, CNInfo.
2. Issuer annual/interim reports, earnings previews, investor-relations records, shareholder-meeting and corporate-action announcements.
3. Government and industry: CSRC, PBOC, NBS, ministries, customs and industry associations.
4. Quotes/estimates: reputable market-data providers. Identify timestamp, adjustment method and upstream vendor.

### U.S. stocks

1. SEC EDGAR filings and issuer investor relations.
2. Exchange, FINRA and official regulatory releases.
3. Government/macro: Federal Reserve/FRED, BLS, BEA and relevant agencies.
4. Quotes/estimates: reputable market-data providers. Treat consensus as market expectations, not fact.

## Independence test

- Two pages repeating the same filing are not two independent facts.
- Two aggregators using the same upstream feed are one source.
- For financial statements, use the filing as canonical and a separately maintained database as the cross-check.
- For a breaking event, use the announcement/regulator and one independent report when interpretation matters.

## Required metadata

Record source URL, publication date, fiscal period, as-of date, currency, units, GAAP/adjusted status, and whether the value is reported, derived or estimated.

## Price-series controls

- Use unadjusted/current price for executable current orders and current market cap.
- Use one consistent adjusted series for historical return, trend and long-horizon price comparison.
- State whether total-return calculations include dividends.
- Exclude all observations after the analysis date.
- Flag stale, halted, missing or conflicting quotes.

## Citation standard

Link every decision-critical current claim near the claim. Prefer direct links to filings, announcements and rule pages. Avoid citing a search-result page.

