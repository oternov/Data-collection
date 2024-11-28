# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import os
import csv


class UnsplashPipeline:
    # def process_item(self, item, spider):
    #     return item
    
    def open_spider(self, spider):
        # Создаем директорию для CSV-файла, если она не существует
        os.makedirs('output', exist_ok=True)
        
        # Открываем CSV-файл для записи
        self.file = open('output/images_info.csv', 'w', newline='', encoding='utf-8')
        
        self.writer = csv.writer(self.file)
        
        self.writer.writerow(['name', 'category', 'url', 'photos'])

    def close_spider(self, spider):
        # Закрываем файл
        self.file.close()

    def process_item(self, item, spider):
        # Записываем каждый элемент в CSV
        try:
            self.writer.writerow([
                item.get('name', [''])[0].strip('[]'),
                #item.get('category', [''])[0].strip('[]'),
                ' '.join(item.get('category', [])),
                item.get('url', [''])[0].strip('[]'),
                item.get('photos', [{}])[0].get('url', '')
            ])
        except Exception as e:
            spider.logger.error(f'Error writing to CSV: {e}')
        
        return item

    
class  UnsplashPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

        if item['photos']:
            for img_url in item['photos']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    print(f'Error: {e}')

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item