import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_dushu.items import ScrapyDushuItem

class ReadSpider(CrawlSpider):
    name = "read"
    allowed_domains = ["www.dushu.com"]
    start_urls = ["https://www.dushu.com/book/1188_1.html"]

    rules = (Rule(LinkExtractor(allow=r"/book/1188_\d+\.html"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        # item = {}
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        img_list = response.xpath('//div[@class="bookslist"]//img')
        for img in img_list:
            name = img.xpath('./@alt').extract_first()
            url = img.xpath('./@data-original').extract_first()
            book = ScrapyDushuItem(name=name, src=url)
            yield book