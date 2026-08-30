import requests
from bs4 import BeautifulSoup


def scrape_product(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Get product name
    title = soup.find("h1")

    if title:
        product_name = title.get_text(strip=True)
    else:
        product_name = "Unknown Product"

    # Get product price
    price_tag = soup.find("p", class_="price_color")

    if price_tag:
        price = price_tag.get_text(strip=True)
    else:
        price = None

    return {
        "name": product_name,
        "price": price,
        "url": url
    }


if __name__ == "__main__":
    url = input("Enter product URL: ")

    product = scrape_product(url)

    print("\nProduct Information")
    print("-------------------")
    print("Name:", product["name"])
    print("Price:", product["price"])
    print("URL:", product["url"])