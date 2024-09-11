import re

from scrapy.exceptions import DontCloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

# scrapy crawl publ_parse_spider -O publications_list.json

class PublParseSpiderSpider(CrawlSpider):

    name = "publparsespiderspider"
    custom_settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        "FEEDS": {r"PublicationReports/parse_app/publications_list.json": {"format": "json",
                                                                           "overwrite": True,
                                                                           "encoding": "utf-8"}
                  }
    }

    def __init__(self, domain=None, *args, **kwargs):
        super(PublParseSpiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            f"{domain}&sortby=pubdate&cstart=0&pagesize=10",
 #           f"{domain}&sortby=pubdate&cstart=101&pagesize=200",
 #           f"{domain}&sortby=pubdate&cstart=201&pagesize=300",
 #           f"{domain}&sortby=pubdate&cstart=301&pagesize=400",
 #           f"{domain}&sortby=pubdate&cstart=401&pagesize=500"
        ]

    rules = (Rule(LinkExtractor(restrict_xpaths="//td[@class='gsc_a_t']/a"), callback="parse_item"),)
    def parse_item(self, response):

        item = {}
        item["Название"] = response.xpath('//a[@class="gsc_oci_title_link"]/text()').get()
        # вытаскиваем количество публикаций (очень сложно)
        citation = response.xpath('//div[@id="gsc_vcpb"]//div[@class="gsc_oci_value"]/div/a').getall()
        if len(str(citation)) > 2:
            cit = citation[0]
            cit = cit[-9:-1:1]
            item["Цитирования"] = ''.join(c if c.isdigit() else ' ' for c in cit).split()[0]
        else:
            item["Цитирования"] = "0"
        publications_field = response.xpath('//div[@id="gsc_vcpb"]//div[@class="gsc_oci_field"]')
        publications_value = response.xpath('//div[@id="gsc_vcpb"]//div[@class="gsc_oci_value"]')
        titles = list()

        i = 0
        for p in publications_field:
            titles.append(p.xpath('./text()').get())
            i += 1

        i = 0
        for p in publications_value:
            item[titles[i]] = p.xpath('./text()').get()
            i += 1

        return item