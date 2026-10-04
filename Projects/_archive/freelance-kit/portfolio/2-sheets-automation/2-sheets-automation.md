# Google Sheets Automation → Auto-Email & Daily Summary

A Google Apps Script that turns a plain order-tracking sheet into a hands-free
workflow. No more manually emailing customers or tallying up the day's orders.

**The problem it solves:** small teams waste time on the same spreadsheet ritual
every day — emailing "your order is done", stamping timestamps, counting pending
items. This does it automatically.

## What it does

1. **Instant customer email on completion** — set a row's `Status` to **Done** and
   the script auto-stamps the completion time and emails that customer a
   confirmation. Zero clicks.
2. **Scheduled daily summary** — every morning at 8am the owner gets an email:
   how many orders are pending (and their total value) vs. completed.
3. **Custom menu** — a `⚙️ Automation` menu so non-technical users can trigger
   actions from the toolbar.

## Sheet layout

| A: Order ID | B: Customer | C: Email | D: Amount | E: Status | F: Completed At |
|---|---|---|---|---|---|
| 1001 | Acme Co | ops@acme.com | 250 | Pending | |

`Status` is either `Pending` or `Done`.

## Setup (2 minutes)

1. Open your sheet → **Extensions ▸ Apps Script**.
2. Paste `Code.gs`.
3. Change `OWNER_EMAIL` at the top to your address.
4. Make sure the tab is named `Orders` (or change `SHEET_NAME`).
5. Reload the sheet — the `⚙️ Automation` menu appears.
6. To enable the daily email, run **createDailyTrigger** once (menu or editor) and
   approve the permission prompt.

That's it. Editing a Status to `Done` now emails the customer automatically.

## How it adapts to client work

The same pattern — *trigger → read row → act* — covers most "do something when a
cell changes" requests: notify a Slack channel, append to another sheet, generate
an invoice, update a CRM via API. The structure here is the reusable skeleton.

## Tech

Google Apps Script · MailApp · time-driven & onEdit triggers
