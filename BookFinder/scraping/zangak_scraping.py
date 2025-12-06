import requests
from bs4 import BeautifulSoup
import time
import csv

BASE_URL = "https://zangakbookstore.am"
START_URL = BASE_URL + "/en/"

def get_soup(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def find_all_category_urls():
    soup = get_soup(START_URL)
    books_header = soup.find(
        "a",
        class_="category-name",
        string=lambda s: s and s.strip() == "Books"
    )
    if not books_header:
        return []

    parent = books_header.find_parent("div", class_="category-item")
    subcat_box = parent.find("div", class_="sub-category")

    categories = []

    for a in subcat_box.select("a.category-name"):
        cat_name = a.get_text(strip=True)
        href = a.get("href")
        if not href:
            continue

        if href.startswith("/"):
            href = BASE_URL + href
        elif not href.startswith("http"):
            href = BASE_URL + "/" + href.lstrip("/")
        href = href.split("#")[0]

        categories.append((href, cat_name))

    return categories

def scrape_prices_from_category(category_url):
    books = []
    page = 1

    while True:
        url = category_url if page == 1 else f"{category_url}?page={page}"
        soup = get_soup(url)

        items = soup.select("div.list-item div.product-item")
        if not items:
            break

        for it in items:
            a_tag = it.select_one("h1 a")
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True)
            print(f"Found book title: {title}")

            # English-only check
            if not all(ord(c) < 128 for c in title):
                continue
            print(" → Accepted as English book.")

            price_tag = it.select_one("div.product-price")
            price = price_tag.get_text(strip=True) if price_tag else ""
            print(price)
            url = a_tag["href"]
            if not url.startswith("http"):
                url = BASE_URL + url

            books.append({"title": title, "price": price, "url": url})

        # Stop if no more pages
        next_button = soup.select_one("button.view-more-button")
        if not next_button:
            break

        page += 1
        time.sleep(1)

    return books


def save_csv(books, filename="zangak_price.csv"):
    keys = ["title", "price", "url"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(books)
    print(f"Saved {len(books)} books to {filename}")

if __name__ == "__main__":
    all_books = []

    categories = find_all_category_urls()
    print(f"Found {len(categories)} categories.\n")

    for idx, (cat_url, cat_name) in enumerate(categories, start=1):
        print(f"[{idx}/{len(categories)}] Scraping category: {cat_name}")
        books_in_cat = scrape_prices_from_category(cat_url)
        print(f"   → Found {len(books_in_cat)} English books in this category.\n")
        all_books.extend(books_in_cat)

        # Optional: incremental save
        save_csv(all_books)

        time.sleep(0.5)

    # Final save
    save_csv(all_books)
    print("\nScraping complete.")