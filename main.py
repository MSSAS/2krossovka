from bs4 import BeautifulSoup
import requests
import json

def extract_product_info(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'lxml')

    product_name = soup.find('div', class_="flixer-header").find('h1', class_='product-titl').text.strip()
    product_price = soup.find('div', class_='stock-status-block-0').find('div', class_='pull-left').text.strip()

    # Return information about the product
    return {'name': product_name, 'price': product_price, 'url': product_url}

url = 'https://2krossovka.ru/krossovki-muzhskie/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
items = soup.find_all('div', class_="product-layout")

all_categories_dict = {}

for item in items:
    item_url = item.find('a', itemprop="url").get('href')
    product_info = extract_product_info(item_url)
    all_categories_dict[item_url] = product_info

pagination = soup.find('div', class_="col-sm-6 text-left").find('ul',class_='pagination')
pagination_links = pagination.find_all('a')
for link in pagination_links:
    page_url = link['href']
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_="product-layout")
    for item in items:
        item_url = item.find('a', itemprop="url").get('href')
        product_info = extract_product_info(item_url)
        all_categories_dict[item_url] = product_info 

# with open("products.json", 'w', encoding="utf-8") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open("products.txt", 'w', encoding="utf-8") as file:
    for product_info in all_categories_dict.values():
        file.write(f"Name: {product_info['name']}\n")
        file.write(f"Price: {product_info['price']}\n")
        file.write(f"URL: {product_info['url']}\n\n")
