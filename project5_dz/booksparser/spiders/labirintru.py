import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class LabirintruSpider(scrapy.Spider):
    name = "labirintru"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/books/"]


    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//div[@class='pagination-next']/a[@class='pagination-next__text']/@href").get() # get() возвращает первый элемент 
        if next_page: # если есть следующая страница
            yield response.follow(next_page, callback=self.parse)
        
        links = response.xpath("//div[@class='genres-catalog']//a[@class='product-title-link']/@href").getall() # getall() возвращает все элементы внутри объякта
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        

    def vacancy_parse(self, response: HtmlResponse):
        #id = response.xpath("//div[@class='articul'][contains(text(), 'ID товара:')]/text()").get()
        name = response.xpath("//h1/text()").get() # название книги
        price_old = response.xpath("//span[@class='buying-priceold-val-number']/text()").get() # цена без скидки
        price_discount = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get() # цена со скидкой
        author = response.xpath("//div[contains(text(), 'Автор:')]/a/text()").get() # автор
        rating = response.xpath("//div[@id='product-voting-body']/meta[@itemprop='ratingValue']/@content").get()
        url = response.url
        yield BooksparserItem(name=name, price_old=price_old, price_discount=price_discount, url=url, author=author, rating=rating)

# scrapy crawl hhru - запуск паука
