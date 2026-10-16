#!/usr/bin/env python3
"""Deterministic decimal arithmetic for stock research."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, InvalidOperation, getcontext

getcontext().prec = 34


def dec(value: object) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise argparse.ArgumentTypeError(f"invalid decimal: {value}") from exc


def fmt(value: Decimal | None, places: int = 6) -> str | None:
    if value is None:
        return None
    quantum = Decimal(1).scaleb(-places)
    return format(value.quantize(quantum), "f").rstrip("0").rstrip(".") or "0"


def emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def verify_market_cap(args: argparse.Namespace) -> None:
    calculated = args.price * args.shares
    variance = None
    if args.reported is not None and args.reported != 0:
        variance = abs(calculated - args.reported) / abs(args.reported) * 100
    emit(
        {
            "command": "verify-market-cap",
            "currency": args.currency,
            "price": fmt(args.price),
            "shares": fmt(args.shares),
            "calculated_market_cap": fmt(calculated),
            "reported_market_cap": fmt(args.reported),
            "variance_percent": fmt(variance, 4),
            "status": "PASS" if variance is None or variance <= Decimal("1") else "INVESTIGATE",
        }
    )


def cross_validate(args: argparse.Namespace) -> None:
    raw = json.loads(args.values)
    if not isinstance(raw, dict) or len(raw) < 2:
        raise SystemExit("--values must be a JSON object with at least two sources")
    items = [(str(k), dec(v)) for k, v in raw.items()]
    reference_name, reference = items[0]
    comparisons = []
    max_variance = Decimal(0)
    for name, value in items[1:]:
        denominator = abs(reference)
        variance = Decimal(0) if value == reference else None
        if denominator != 0:
            variance = abs(value - reference) / denominator * 100
        if variance is None:
            status = "UNDEFINED_REFERENCE_ZERO"
        else:
            max_variance = max(max_variance, variance)
            status = "PASS" if variance <= Decimal("1") else "INVESTIGATE"
        comparisons.append(
            {
                "source": name,
                "value": fmt(value),
                "variance_vs_reference_percent": fmt(variance, 4),
                "status": status,
            }
        )
    emit(
        {
            "command": "cross-validate",
            "field": args.field,
            "unit": args.unit,
            "reference": {"source": reference_name, "value": fmt(reference)},
            "comparisons": comparisons,
            "max_variance_percent": fmt(max_variance, 4),
            "status": "PASS" if max_variance <= Decimal("1") else "INVESTIGATE",
        }
    )


def valuation(args: argparse.Namespace) -> None:
    def ratio(numerator: Decimal, denominator: Decimal | None) -> Decimal | None:
        return None if denominator is None or denominator == 0 else numerator / denominator

    payload = {
        "command": "valuation",
        "currency": args.currency,
        "price": fmt(args.price),
        "pe": fmt(ratio(args.price, args.eps), 4),
        "pb": fmt(ratio(args.price, args.bvps), 4),
        "fcf_yield_percent": fmt(
            None if args.fcf_per_share is None or args.price == 0 else args.fcf_per_share / args.price * 100,
            4,
        ),
        "dividend_yield_percent": fmt(
            None if args.dividend is None or args.price == 0 else args.dividend / args.price * 100,
            4,
        ),
    }
    emit(payload)


def scenario(args: argparse.Namespace) -> None:
    names = ("bull", "base", "bear")
    rows = []
    discount_factor = (Decimal(1) + args.discount_rate) ** args.years
    for name, growth, multiple in zip(names, args.growth, args.exit_multiple):
        future_eps = args.eps * ((Decimal(1) + growth) ** args.years)
        future_price = future_eps * multiple
        present_value = future_price / discount_factor
        upside = None if args.price == 0 else (present_value / args.price - Decimal(1)) * 100
        cagr = None
        if args.price > 0 and future_price >= 0:
            cagr = (future_price / args.price) ** (Decimal(1) / Decimal(args.years)) - Decimal(1)
        rows.append(
            {
                "scenario": name,
                "growth_percent": fmt(growth * 100, 3),
                "exit_multiple": fmt(multiple, 3),
                "future_eps": fmt(future_eps),
                "future_price": fmt(future_price),
                "present_value": fmt(present_value),
                "upside_to_present_value_percent": fmt(upside, 3),
                "undiscounted_price_cagr_percent": fmt(None if cagr is None else cagr * 100, 3),
            }
        )
    emit(
        {
            "command": "scenario",
            "currency": args.currency,
            "current_price": fmt(args.price),
            "starting_eps": fmt(args.eps),
            "years": args.years,
            "discount_rate_percent": fmt(args.discount_rate * 100, 3),
            "scenarios": rows,
            "warning": "Scenario output is arithmetic, not a probability-weighted forecast.",
        }
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    cap = sub.add_parser("verify-market-cap")
    cap.add_argument("--price", type=dec, required=True)
    cap.add_argument("--shares", type=dec, required=True)
    cap.add_argument("--reported", type=dec)
    cap.add_argument("--currency", default="")
    cap.set_defaults(func=verify_market_cap)

    cross = sub.add_parser("cross-validate")
    cross.add_argument("--field", required=True)
    cross.add_argument("--values", required=True, help='JSON such as {"filing": 10, "vendor": 10.01}')
    cross.add_argument("--unit", default="")
    cross.set_defaults(func=cross_validate)

    val = sub.add_parser("valuation")
    val.add_argument("--price", type=dec, required=True)
    val.add_argument("--eps", type=dec)
    val.add_argument("--bvps", type=dec)
    val.add_argument("--fcf-per-share", dest="fcf_per_share", type=dec)
    val.add_argument("--dividend", type=dec)
    val.add_argument("--currency", default="")
    val.set_defaults(func=valuation)

    scen = sub.add_parser("scenario")
    scen.add_argument("--price", type=dec, required=True)
    scen.add_argument("--eps", type=dec, required=True)
    scen.add_argument("--growth", type=dec, nargs=3, metavar=("BULL", "BASE", "BEAR"), required=True,
                      help="annual decimal growth rates, e.g. .18 .10 .02")
    scen.add_argument("--exit-multiple", type=dec, nargs=3, metavar=("BULL", "BASE", "BEAR"), required=True)
    scen.add_argument("--years", type=int, default=3)
    scen.add_argument("--discount-rate", type=dec, default=Decimal("0"))
    scen.add_argument("--currency", default="")
    scen.set_defaults(func=scenario)
    return parser


if __name__ == "__main__":
    arguments = build_parser().parse_args()
    if getattr(arguments, "years", 1) <= 0:
        raise SystemExit("--years must be positive")
    arguments.func(arguments)

