import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """Собирает ссылки на Пипы"""
        lines = response.css('a.pep.reference.internal')
        for line in lines:
            # follow автоматически убирает дубликаты
            yield response.follow(
                line.css('::attr(href)').get(),
                callback=self.parse_pep
            )

    def parse_pep(self, response):
        """Формирует объектр Items для Пип"""
        status_tag = response.xpath('//dt[contains(text(), "Status")]')
        status = status_tag.xpath('./following-sibling::dd[1]//text()').get()
        name = response.css('h1.page-title::text').get()
        number = re.search(r'\d+', name)
        data = {
            'name': name.strip(),
            'status': status.strip() if status else '',
            'number': int(number.group(0))
        }
        yield PepParseItem(data)
