# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst,MapCompose,Compose

# def process_name(value):
#     value = value[0].strip()
#     return value

# def process_price(value):
#     value = value[0].strip().replace('\xa0',' ').split()
#     if value[0].isdigit():
#         value[0] = int(value[0])
#     return value

# def process_photos(value):
#     if value[0].startswith('//'):
#         value = 'https:' + value.split()[0]
#     else:
#         value = value.split()[0][1]
#     return value


class UnsplashItem(scrapy.Item):
    name = scrapy.Field(input_processor=TakeFirst())
    url = scrapy.Field(input_processor=TakeFirst())
    category = scrapy.Field(input_processor=TakeFirst())
    photos = scrapy.Field(input_processor=TakeFirst())
