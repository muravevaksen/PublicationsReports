import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# Добавить парсинг ВСЕХ публикаций, сейчас выводит только первые 100!
# scrapy crawl publ_parse_spider -O spider_app.json

class PublParseSpiderSpider(CrawlSpider):
    name = "publ_parse_spider"
    allowed_domains = ["scholar.google.com"]
    id_author = "9c_OePYAAAAJ"
    start_urls = ["https://scholar.google.com/citations?view_op=list_works&hl=ru&hl=ru&user=9c_OePYAAAAJ&pagesize=100"]
    # добавить параметр для перешагивания по страницам

    rules = (Rule(LinkExtractor(restrict_xpaths="//td[@class='gsc_a_t']/a"), callback="parse_item", follow=True),)

    def parse_item(self, response):

        item = {}

        item["title"] = response.xpath('//a[@class="gsc_oci_title_link"]/text()').get()
        publications = response.xpath('//div[@id="gsc_vcpb"]//div[@class="gsc_oci_value"]')

        titles = ['Authors', 'Year', 'journal', 'Volume', 'Number', 'Pages', 'Publisher', '', '', '']
        i = 0
        for p in publications:
            item[titles[i]] = p.xpath('./text()').get()
            i += 1

        return item
