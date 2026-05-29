"""
Automated Daily Report: API -> CSV (+ optional Slack/Telegram alert)
====================================================================
Fetches live currency exchange rates from a free, no-auth API, builds a
clean dated CSV report, and (optionally) pushes a summary to Slack or
Telegram. Designed to run on a schedule (cron / Task Scheduler) every morning.

This is the reusable skeleton for "pull data from an API -> deliver it
somewhere automatically" — the most common automation request.

API used: https://open.er-api.com  (free, no API key required)

Optional notifications (set via environment variables):
  SLACK_WEBHOOK_URL    -> posts a summary to a Slack channel
  TELEGRAM_BOT_TOKEN   -> with TELEGRAM_CHAT_ID, sends a Telegram message
  TELEGRAM_CHAT_ID
"""

import os
import csv
import sys
import argparse
from datetime import datetime, timezone

import requests

API_URL = "https://open.er-api.com/v6/latest/{base}"

# Currencies to include in the report
WATCH = ["EUR", "GBP", "JPY", "VND", "CNY", "AUD", "CAD"]


def fetch_rates(base: str) -> dict:
    """Fetch latest exchange rates for `base` currency."""
    resp = requests.get(API_URL.format(base=base), timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if data.get("result") != "success":
        raise RuntimeError(f"API error: {data.get('error-type', 'unknown')}")
    return data["rates"]


def build_rows(base: str, rates: dict, stamp: str) -> list[dict]:
    """Pick the watched currencies into clean report rows."""
    rows = []
    for code in WATCH:
        if code in rates:
            rows.append(
                {
                    "date": stamp,
                    "base": base,
                    "currency": code,
                    "rate": round(rates[code], 4),
                }
            )
    return rows


def write_csv(rows: list[dict], path: str) -> None:
    """Append rows to a CSV (creates with header if new)."""
    file_exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "base", "currency", "rate"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)
    print(f"[OK] Wrote {len(rows)} rows -> {path}")


def format_summary(base: str, rows: list[dict], stamp: str) -> str:
    """Human-readable one-message summary."""
    lines = [f"Exchange rates for 1 {base} ({stamp}):"]
    for r in rows:
        lines.append(f"  {r['currency']}: {r['rate']}")
    return "\n".join(lines)


def notify_slack(text: str) -> None:
    url = os.environ.get("SLACK_WEBHOOK_URL")
    if not url:
        return
    try:
        requests.post(url, json={"text": text}, timeout=10).raise_for_status()
        print("[OK] Sent Slack notification")
    except requests.RequestException as exc:
        print(f"[WARN] Slack notify failed: {exc}", file=sys.stderr)


def notify_telegram(text: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat_id):
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        ).raise_for_status()
        print("[OK] Sent Telegram notification")
    except requests.RequestException as exc:
        print(f"[WARN] Telegram notify failed: {exc}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily exchange-rate report.")
    parser.add_argument("--base", default="USD", help="base currency (default USD)")
    parser.add_argument("--out", default="rates_report.csv", help="output CSV path")
    parser.add_argument("--quiet", action="store_true", help="don't print the summary")
    args = parser.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    try:
        rates = fetch_rates(args.base)
    except Exception as exc:  # noqa: BLE001 - report any failure clearly
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    rows = build_rows(args.base, rates, stamp)
    if not rows:
        print("[ERROR] None of the watched currencies were returned.", file=sys.stderr)
        return 1

    write_csv(rows, args.out)

    summary = format_summary(args.base, rows, stamp)
    if not args.quiet:
        print("\n" + summary)

    notify_slack(summary)
    notify_telegram(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
