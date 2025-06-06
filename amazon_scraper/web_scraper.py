import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.amazon.in/s?k=laptops'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5"
}

response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    for item in soup.find_all('div', {'data-component-type': 's-search-result'}):
        title = item.h2.text.strip() if item.h2 else 'N/A'
        price_whole = item.find('span', {'class': 'a-price-whole'})
        price_fraction = item.find('span', {'class': 'a-price-fraction'})

        if price_whole and price_fraction:
            price = f"₹{price_whole.text.strip()}.{price_fraction.text.strip()}"
        else:
            price = 'N/A'

        products.append({'Title': title, 'Price': price})

    df = pd.DataFrame(products)
    df.to_csv('amazon_products.csv', index=False, encoding='utf-8')
    print("Scraping complete! Data saved to 'amazon_products.csv'.")
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
