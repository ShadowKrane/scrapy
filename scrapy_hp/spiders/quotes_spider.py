import scrapy
from pathlib2 import Path

x = []


class QuotesSpider(scrapy.Spider):
    name = "hp"
    base_url = 'http://store.hp.com/ItalyStore/Merch/List.aspx?sel=NTB&ctrl=f&fc_form_nb=1'
    start_urls = [
        'http://store.hp.com/ItalyStore/Merch/List.aspx?sel=NTB&ctrl=f&fc_form_nb=1',
    ]

    def parse(self, response):
        xpath = '.pb-cta__btn--common::attr(href)'
        links = response.css(xpath).extract()
        for l in links:
            yield response.follow(l, callback=self.parse_product)

    def parse_product(self, response):
        selector = '.pb-product__name::text'
        x = response.css(selector).extract_first()

        page = response.url.split("/")[-2]
        file_check = Path('/home/stage/PycharmProjects/scrapy_hp/hp-Merch.html')
        filename = 'hp-%s.html' % page
        MODE = 'a' if file_check.is_file() else 'w'
        with open(filename, MODE) as F:
            F.write(str((response.css('.specs-table__key::text').extract())))
            F.write("\n")
            F.write(str(response.css('.specs-table__value::text').extract()))
            F.write(str(x))
            F.write("\n")
            F.close()
        self.log('Saved file %s' % filename)
