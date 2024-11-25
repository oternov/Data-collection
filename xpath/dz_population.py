import requests
from lxml import html
import csv
import re

# URL веб-сайта с табличными данными
url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'

# Заголовки запроса, включая строку агента пользователя
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Отправка GET-запроса с заголовками
response = requests.get(url, headers=headers)

# Проверка успешности запроса
if response.status_code == 200:
    # Парсинг HTML-содержимого
    tree = html.fromstring(response.content)
    
    # Извлечение данных из таблицы с использованием XPath
    rows = tree.xpath('//table[contains(@class, "wikitable")]/tbody/tr')

    data = []

    # Начинаем с 1, чтобы пропустить заголовок
    for row in rows[1:]:
        try:
            # Извлечение названия страны
            country_link = row.xpath('.//a[@title]')
            
            # Извлечение населения
            population_cell = row.xpath('.//td[contains(@style, "text-align:right")]')
            
            # Извлечение % от населения мира
            percent_world_cell = row.xpath('.//td[contains(@style, "text-align:right;font-size:inherit")]')
            
            # Извлечение даты
            date_cell = row.xpath('.//td/span[contains(@style, "white-space:nowrap")]')
            
            # Проверка наличия необходимых данных
            if country_link and population_cell and percent_world_cell and date_cell:
                # Извлекаем название страны
                country_name = country_link[0].text_content().strip()
                
                # Извлекаем население и очищаем от лишних символов
                population_text = population_cell[0].text_content().strip()
                population_value = re.sub(r'[^\d]', '', population_text)
                
                # Извлекаем % от населения мира
                percent_world_value = percent_world_cell[0].text_content().strip() if percent_world_cell else 'N/A'
                
                # Извлекаем дату
                date_value = date_cell[0].text_content().strip() if date_cell else 'N/A'
                
                # Добавляем данные в список, если это не "World" и население в числовом виде
                if country_name and population_value and country_name != "World":
                    data.append([country_name, population_value, percent_world_value, date_value])
        
        except Exception as e:
            # Обработка ошибок в случае, если данные не имеют ожидаемого формата
            print(f"Ошибка при обработке строки: {e}")

    # Сохранение данных в CSV-файл
    with open('countries_population.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Country', 'Population', '% of World', 'Date'])  # Записываем заголовки
        writer.writerows(data)  # Записываем данные

    print(f"Данные успешно сохранены в countries_population.csv. Всего записей: {len(data)}")
    
    # Вывод собранных данных в консоль
    for country, population, percent_world, date in data:
        print(f"{country}: {population}, % of World: {percent_world}, Date: {date}")

else:
    # Обработка ошибок при запросе
    print(f"Ошибка при запросе: {response.status_code}")