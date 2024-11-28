import scrapy
from scrapy.http import HtmlResponse
from unsplash import spiders
from unsplash.items import UnsplashItem
from scrapy.loader import ItemLoader
import re


class UnsplashcomSpider(scrapy.Spider):
    name = "unsplashcom"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class='zNNw1']")
        for link in links:
            yield response.follow(link, callback=self.parse_photo)
        
   
    def parse_photo(self, response: HtmlResponse):
        loader = ItemLoader(item=UnsplashItem(), response=response)
        try:
            loader.add_xpath('name', "//h1/text()")
        except Exception as e:
            print(f"Error: {e}")
            loader.add_value('name', None)

        try:
            categories = response.xpath("//div[@class='zb0Hu atI7H']/a[@class='m7tXD jhw7y TYpvC']")
            for category in categories:
                loader.add_value('category', category.xpath('./text()').get())
        except Exception as e:
            print(f"Error: {e}")
            loader.add_value('category', None)    
            
        loader.add_value('url', response.url)
        
        # Получение фотографий
        try:
            src = response.xpath('//div[@class="wdUrX"]//img[@class="I7OuT DVW3V L1BOa"]/@src').get()
        except Exception as e:
            print(f"Error: {e}")
            src = None
        # Добавляем фотографии в загруженный элемент
        loader.add_value('photos', src)

        yield loader.load_item()
