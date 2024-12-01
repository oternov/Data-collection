from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime

options = Options()
options.add_argument('start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

driver.get('https://shop.april-group.ru/catalog/novinki/')

# Увеличим тайм-аут для загрузки
wait = WebDriverWait(driver, 60)

# Список для хранения уникальных товаров
goods = set()

def advanced_scroll_and_load():
    # Получаем первоначальную высоту страницы
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Прокручиваем до самого низа
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Небольшая пауза для загрузки контента
        time.sleep(2)
        
        # Принудительная загрузка lazy-load элементов
        driver.execute_script("""
            var elements = document.getElementsByClassName('bx_catalog_item');
            for(var i = 0; i < elements.length; i++) {
                elements[i].style.opacity = '1';
            }
        """)
        
        # Проверяем новую высоту
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        
        last_height = new_height

def parse_all_items():
    # Полная прокрутка и загрузка
    advanced_scroll_and_load()
    
    # Получаем HTML страницы
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Находим все карточки
    cards = soup.find_all(['div', 'li'], class_=['bx_catalog_item', 'product-item'])
    
    print(f"Найдено карточек: {len(cards)}")
    
    for card in cards:
        try:
            name_elem = (card.find('div', class_='bx_catalog_item_title') or 
                         card.find('a', class_='title'))
            name = name_elem.get_text(strip=True) if name_elem else ''
            
            price_elem = (card.find('small') or 
                          card.find('div', class_='price'))
            price = price_elem.get_text(strip=True) if price_elem else ''
            
            url_elem = (card.find('a', class_='bx_catalog_item_images') or 
                        card.find('a', title=True))
            url = 'https://shop.april-group.ru' + url_elem['href'] if url_elem and 'href' in url_elem.attrs else ''
            
            # Создание и добавление товара
            good_item = (name, price, url)
            
            if good_item not in goods and name and price and url:
                goods.add(good_item)
                print(f"Название: {name}, Цена: {price}, URL: {url}")
        
        except Exception as card_error:
            print(f"Ошибка при парсинге карточки: {card_error}")

# Функция для сохранения в CSV
def save_to_csv(goods):
    # Генерируем имя файла с текущей датой
    filename = f"april_group_parsing_{datetime.now().strftime('%Y%m%d')}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Название', 'Цена', 'URL'])
            for item in goods:
                csvwriter.writerow(item)
        
        print(f"Данные сохранены в файл: {filename}")
    
    except Exception as e:
        print(f"Ошибка при сохранении в CSV: {e}")

# Основной парсинг
try:
    # Принудительная загрузка всех товаров
    parse_all_items()
    
    print(f"Всего уникальных товаров: {len(goods)}")
    
    # Сохраняем в CSV
    save_to_csv(goods)

except Exception as global_e:
    print("Глобальная ошибка:", global_e)

finally:
    driver.quit()