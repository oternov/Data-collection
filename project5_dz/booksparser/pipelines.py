# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class BooksparserPipeline:
    def __init__(self):
        self.file = open('books.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['name', 'price_old', 'price_discount', 'author', 'rating', 'url'])  # заголовки

    def process_item(self, item, spider):
        self.writer.writerow([
            item.get('name', ''), 
            item.get('price_old', ''), 
            item.get('price_discount', ''), 
            item.get('author', ''), 
            item.get('rating', ''), 
            item.get('url', '')
        ])
        return item

    def close_spider(self, spider):
        self.file.close()