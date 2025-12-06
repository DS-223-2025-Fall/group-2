import requests
from bs4 import BeautifulSoup
import csv


def init_csv(filename="books.csv"):
    headers = ["name", "author", "price", "genre", "url"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()


def append_to_csv(data, filename="books.csv"):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writerow(data)


def get_books_categories():
    url = "https://www.books.am/am/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    books_menu = soup.find("li", attrs={"data-title": "Գրքեր"})
    if not books_menu:
        raise RuntimeError("Could not find 'Գրքեր' menu")

    categories = []
    for a in books_menu.select(".submenu_list a[href]"):
        href = a.get("href")
        title = a.get_text(strip=True)

        if "/catalog/category/view/id/" in href:
            categories.append({"title": title, "url": href})

    return categories


def extract_books_from_category(url, category_name):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.select(".product_name a.combo_link")

    books = []
    for a in items:
        books.append({
            "title": a.get_text(strip=True),
            "url": a.get("href")
        })

    return books


def scrape_book(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # NAME
    name_el = soup.select_one(".product.attribute.section_title")
    name = name_el.get_text(strip=True) if name_el else ""

    # AUTHOR
    author_el = soup.select_one(".product_brand")
    author = author_el.get_text(strip=True) if author_el else ""

    # PRICE
    price_el = soup.select_one(".price-wrapper .price")
    price = price_el.get_text(strip=True).replace("դր.", "").strip() if price_el else ""

    return {
        "name": name,
        "author": author,
        "price": price
    }

def extract_all_books(category_url, category_name, csv_filename="books.csv"):
    max_pages = 100 if category_url == "https://www.books.am/am/catalog/category/view/id/7464/" else 10

    for i in range(1, max_pages + 1):
        page_url = f"{category_url}?p={i}"
        print("Scanning:", page_url)

        books = extract_books_from_category(page_url, category_name)
        if not books:
            print("No more books. Stopping.")
            break

        for b in books:
            print("Scraping:", b["url"])

            data = scrape_book(b["url"])
            data["genre"] = category_name
            data["url"] = b["url"]

            append_to_csv(data, csv_filename)


init_csv("books.csv")

categories = get_books_categories()

for category in categories:
    print("\nCATEGORY:", category["title"])
    extract_all_books(category["url"], category["title"], "books.csv")

print("\nDONE — All books saved to books.csv")
