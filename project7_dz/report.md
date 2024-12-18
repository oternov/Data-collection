## Отчет о парсинге сайта April Group

### URL сайта: https://shop.april-group.ru/catalog/novinki/

```
Описание проекта:
```
Цель проекта - автоматизированный сбор информации о товарах из раздела "Новинки" интернет-магазина April Group. Задача включала извлечение следующих данных о каждом товаре:

1. Название товара
2. Цена
3. URL-адрес товара

```
Технический подход:
```
_Инструментарий:_
- Selenium WebDriver
- BeautifulSoup
- Python 3.8+

_Ключевые методы парсинга:_
- Динамическая прокрутка страницы
- Принудительная загрузка lazy-load элементов
- Обработка JavaScript-контента
- Поиск элементов с использованием множественных CSS-селекторов

```
Трудности и решения:
```

1. Проблема: Неполная загрузка товаров.
   
   Решение: Реализация динамической прокрутки с принудительным отображением элементов

2. Проблема: Исчезновение стрелки пагинации.

   Решение: Отказ от поиска стрелки, использование JavaScript-скроллинга для полной загрузки контента

3. Проблема: Частичная загрузка страницы.

   Решение: Увеличение таймаутов. Принудительная задержка. Многократная прокрутка

4. Проблема: Нестабильность селекторов.
   Решение: Использование множественных вариантов поиска элементов

```
Результаты:
```
Успешно спарсено 49 товаров.

Сохранение в CSV с уникальным именем.

Кодировка UTF-8 для корректного отображения кириллицы.
