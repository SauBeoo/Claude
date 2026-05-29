"""
E-commerce Product Scraper -> Clean Excel Export
=================================================
Scrapes product data (title, price, rating, availability, URL) from a paginated
catalog and exports it to a clean, formatted Excel file.

Demo target: https://books.toscrape.com  (a public site built FOR scraping practice)

This is portfolio/demo code. For client work the same structure adapts to any
public catalog by adjusting the CSS selectors in parse_product().
"""

import sys
import time
import argparse
from dataclasses import dataclass, asdict
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"

# Maps the site's word-based rating class to an integer.
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}


@dataclass
class Product:
    title: str
    price_gbp: float
    rating: int
    availability: str
    url: str


def fetch(url: str, retries: int = 3) -> BeautifulSoup:
    """GET a page with simple retry/backoff; return parsed soup."""
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except requests.RequestException as exc:
            if attempt == retries:
                raise
            wait = attempt * 2
            print(f"  ! request failed ({exc}); retry {attempt}/{retries} in {wait}s")
            time.sleep(wait)


def parse_product(card) -> Product:
    """Extract one product from a single <article class='product_pod'> card."""
    title = card.h3.a["title"].strip()

    price_text = card.select_one("p.price_color").get_text(strip=True)
    # Strip currency symbol + any stray non-breaking chars -> float
    price = float(price_text.replace("£", "").replace("Â", "").strip())

    rating_class = card.select_one("p.star-rating")["class"]  # e.g. ['star-rating', 'Three']
    rating_word = next((c for c in rating_class if c in RATING_MAP), None)
    rating = RATING_MAP.get(rating_word, 0)

    availability = card.select_one("p.instock.availability").get_text(strip=True)

    relative = card.h3.a["href"]
    url = urljoin(BASE_URL, relative)

    return Product(title, price, rating, availability, url)


def scrape(max_pages: int) -> list[Product]:
    """Walk the paginated catalogue and collect products."""
    products: list[Product] = []
    next_url = START_URL
    page = 0

    while next_url and page < max_pages:
        page += 1
        print(f"[page {page}] {next_url}")
        soup = fetch(next_url)

        for card in soup.select("article.product_pod"):
            products.append(parse_product(card))

        # Resolve the "next" link if present
        next_link = soup.select_one("li.next a")
        next_url = urljoin(next_url, next_link["href"]) if next_link else None

        time.sleep(1)  # be polite: 1 req/sec

    return products


def export_excel(products: list[Product], path: str) -> None:
    """Write products to a formatted Excel file (auto-fit columns + de-dup)."""
    df = pd.DataFrame(asdict(p) for p in products)
    df = df.drop_duplicates(subset="url").reset_index(drop=True)
    df.index += 1
    df.index.name = "No."

    df = df.rename(
        columns={
            "title": "Title",
            "price_gbp": "Price (GBP)",
            "rating": "Rating",
            "availability": "Availability",
            "url": "URL",
        }
    )

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Products")
        ws = writer.sheets["Products"]
        # Auto-fit column widths (cap at 60 chars)
        for col_cells in ws.columns:
            length = max(len(str(c.value)) if c.value is not None else 0 for c in col_cells)
            letter = col_cells[0].column_letter
            ws.column_dimensions[letter].width = min(length + 2, 60)

    print(f"\n[OK] Exported {len(df)} products -> {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape a product catalogue to Excel.")
    parser.add_argument("--pages", type=int, default=3, help="max pages to scrape (default 3)")
    parser.add_argument("--out", default="products.xlsx", help="output Excel file")
    args = parser.parse_args()

    products = scrape(args.pages)
    if not products:
        print("No products found.", file=sys.stderr)
        return 1

    export_excel(products, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
