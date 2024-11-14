#Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию о всех книгах на сайте во всех категориях: 
# название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
# Затем сохранить эту информацию в JSON-файле.

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
import json

ua = UserAgent()

url = "https://books.toscrape.com"

headers = {"User-Agent": ua.random}
params = {"page": 1}

session = requests.session()

all_posts = []

while True:

    response = session.get(url + "/catalogue/page-" + str(params['page']) + ".html", headers=headers, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", class_="product_pod")
    if not products:
        break      

    for product in products:
            products_info = {}

            name_info = product.find("h3").find("a")

            subresponse = session.get("https://books.toscrape.com/catalogue/" + name_info.get('href'), headers=headers, params=params)
            book_soup = BeautifulSoup(subresponse.text, "html.parser")

            name = book_soup.find("div", {"class":"col-sm-6 product_main"}).find("h1").getText()
            products_info['name'] = name

            price = book_soup.find("div", {"class":"col-sm-6 product_main"}).find("p", {"class":"price_color"}).getText()
            products_info['price'] = float(price.split('£')[1].split()[0])

            stock = book_soup.find("div", {"class":"col-sm-6 product_main"}).find("p", {"class":"instock availability"}).getText()
            products_info['stock'] = int(stock.split('(')[1].split()[0])

            description_section = book_soup.find("div", id="product_description")
            if description_section:
                description_paragraph = description_section.find_next_sibling("p")
                if description_paragraph:
                    products_info['description'] = description_paragraph.getText()
                else:
                    products_info['description'] = "Нет описания"
            else:
                products_info['description'] = "Нет описания"

            all_posts.append(products_info)
    print(f"Обработана {params['page']} страница")
    params['page'] += 1

with open('books.json', 'w', encoding='utf-8') as f:
    json.dump(all_posts, f, ensure_ascii=False, indent=4)

pprint(all_posts)
pprint(len(all_posts))