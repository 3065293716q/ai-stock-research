#!/usr/bin/env python3
"""Validate and size executable A-share and U.S.-stock orders."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, ROUND_DOWN, InvalidOperation, getcontext

getcontext().prec = 34


def dec(value: object) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise argparse.ArgumentTypeError(f"invalid decimal: {value}") from exc


def floor_int(value: Decimal) -> int:
    return int(value.to_integral_value(rounding=ROUND_DOWN))


def emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def buy(args: argparse.Namespace) -> None:
    if args.price <= 0:
        raise SystemExit("--price must be positive")
    budgets = [args.cash]
    if args.portfolio_value is not None and args.max_weight is not None:
        budgets.append(args.portfolio_value * args.max_weight)
    budget = min(budgets)
    effective_price = args.price * (Decimal(1) + args.fee_buffer_bps / Decimal(10000))
    shares_by_cash = floor_int(budget / effective_price)
    shares_by_risk = None
    risk_budget = None
    if args.portfolio_value is not None and args.risk_fraction is not None and args.risk_level is not None:
        loss_per_share = args.price - args.risk_level
        if loss_per_share <= 0:
            raise SystemExit("--risk-level must be below --price for long-position sizing")
        risk_budget = args.portfolio_value * args.risk_fraction
        shares_by_risk = floor_int(risk_budget / loss_per_share)
    raw = min(shares_by_cash, shares_by_risk) if shares_by_risk is not None else shares_by_cash

    if args.market == "cn-sse-szse":
        quantity = raw // 100 * 100
        legal = quantity >= 100
        unit_rule = "minimum 100 shares; buy quantity must be a multiple of 100"
    elif args.market == "cn-bse":
        quantity = raw
        legal = quantity >= 100
        unit_rule = "minimum 100 shares; quantities may increase by one share"
    elif args.allow_fractional:
        quantity = str((budget / effective_price).quantize(Decimal("0.000001"), rounding=ROUND_DOWN))
        legal = Decimal(quantity) > 0
        unit_rule = "fractional order assumed; verify broker support"
    else:
        quantity = raw
        legal = quantity >= 1
        unit_rule = "whole-share order; no universal 100-share minimum"

    numeric_quantity = Decimal(str(quantity))
    estimated_cost = numeric_quantity * args.price
    emit(
        {
            "command": "buy",
            "market": args.market,
            "valid": legal,
            "quantity": quantity,
            "price": str(args.price),
            "estimated_notional": str(estimated_cost),
            "budget_used_for_sizing": str(budget),
            "shares_by_cash_before_rounding": shares_by_cash,
            "shares_by_risk_before_rounding": shares_by_risk,
            "risk_budget": None if risk_budget is None else str(risk_budget),
            "unit_rule": unit_rule,
            "warning": "Risk-level sizing does not guarantee the exit price; gaps, limit-down and liquidity can enlarge losses.",
        }
    )


def valid_sse_szse_sell(holdings: int, quantity: int) -> tuple[bool, str]:
    if quantity <= 0 or quantity > holdings:
        return False, "quantity must be between 1 and total holdings"
    odd = holdings % 100
    if odd == 0:
        return (quantity % 100 == 0, "round-lot holdings require a 100-share-multiple sell")
    if quantity % 100 == 0:
        return True, "valid round-lot sell; odd remainder remains"
    if quantity % 100 == odd:
        return True, "valid sell including the entire odd-lot remainder once"
    return False, "invalid split of the odd-lot remainder"


def sell(args: argparse.Namespace) -> None:
    holdings = args.holdings
    sellable = holdings if args.sellable is None else args.sellable
    if holdings < 0 or sellable < 0 or sellable > holdings:
        raise SystemExit("require 0 <= sellable <= holdings")
    quantity = sellable if args.all else args.quantity
    if quantity is None:
        raise SystemExit("provide --quantity or --all")
    if quantity > sellable:
        legal, reason = False, "requested quantity exceeds shares sellable now (possible T+1 lock)"
    elif args.market == "cn-sse-szse":
        legal, reason = valid_sse_szse_sell(holdings, quantity)
    elif args.market == "cn-bse":
        legal = quantity == holdings or quantity >= 100
        reason = "BSE partial sell must be at least 100 shares; a final sub-100 balance is sold once"
    else:
        legal = quantity >= 1
        reason = "whole-share U.S. sell assumed; verify fractional/tax-lot broker rules"

    remaining = holdings - quantity if legal else holdings
    emit(
        {
            "command": "sell",
            "market": args.market,
            "valid": legal,
            "requested_quantity": quantity,
            "holdings": holdings,
            "sellable_now": sellable,
            "temporarily_unsellable": holdings - sellable,
            "remaining_after_order": remaining,
            "reason": reason,
            "t_plus_one_warning": (
                "A-share shares bought today may not be sellable until the next trading day."
                if args.market.startswith("cn-") and holdings != sellable
                else None
            ),
        }
    )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    markets = ("cn-sse-szse", "cn-bse", "us")

    b = sub.add_parser("buy")
    b.add_argument("--market", choices=markets, required=True)
    b.add_argument("--price", type=dec, required=True)
    b.add_argument("--cash", type=dec, required=True)
    b.add_argument("--portfolio-value", type=dec)
    b.add_argument("--max-weight", type=dec, help="decimal, e.g. .10")
    b.add_argument("--risk-fraction", type=dec, help="decimal, e.g. .01")
    b.add_argument("--risk-level", type=dec)
    b.add_argument("--fee-buffer-bps", type=dec, default=Decimal("10"))
    b.add_argument("--allow-fractional", action="store_true")
    b.set_defaults(func=buy)

    s = sub.add_parser("sell")
    s.add_argument("--market", choices=markets, required=True)
    s.add_argument("--holdings", type=int, required=True)
    s.add_argument("--sellable", type=int)
    group = s.add_mutually_exclusive_group(required=True)
    group.add_argument("--quantity", type=int)
    group.add_argument("--all", action="store_true")
    s.set_defaults(func=sell)
    return root


if __name__ == "__main__":
    arguments = parser().parse_args()
    arguments.func(arguments)

