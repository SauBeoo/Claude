# E-commerce Product Scraper → Clean Excel Export

A small, production-style web scraper that walks a paginated product catalogue and
exports clean, de-duplicated data to a formatted Excel file.

**The problem it solves:** copying product data (names, prices, ratings, links) by
hand is slow and error-prone. This pulls it in seconds into a spreadsheet you can
actually use.

## What it extracts

| Field | Example |
|-------|---------|
| Title | *A Light in the Attic* |
| Price (GBP) | 51.77 |
| Rating | 3 |
| Availability | In stock |
| URL | https://... |

## Features

- **Pagination handling** — follows "next" links automatically
- **Retry + backoff** on failed requests
- **De-duplication** by product URL
- **Polite crawling** — 1 request/second, real User-Agent
- **Formatted Excel output** — auto-fit columns, indexed rows

## Quick start

```bash
pip install -r requirements.txt
python scraper.py --pages 3 --out products.xlsx
```

Arguments:
- `--pages` — max number of catalogue pages to scrape (default: 3)
- `--out` — output Excel filename (default: `products.xlsx`)

## How it adapts to client work

The demo targets [books.toscrape.com](https://books.toscrape.com) (a public site
built for scraping practice). For a real catalogue, only `parse_product()` and the
CSS selectors change — the pagination, retry, de-dup, and Excel-export machinery
stay the same.

> ⚠️ I only scrape publicly available data and respect each site's Terms of Service
> and robots.txt.

## Tech

Python · requests · BeautifulSoup · pandas · openpyxl
