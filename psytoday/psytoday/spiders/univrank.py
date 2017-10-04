# -*- coding: utf-8 -*-
import scrapy
import re

class UnivrankSpider(scrapy.Spider):
    name = 'univrank'
    allowed_domains = ['usnews.com']
    start_urls = ['https://www.usnews.com/best-graduate-schools/search?sort=college_name&sortdir=asc&program_rank=ranked&program=top-psychology-schools']
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OSX 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome 39.0.2171.95 Saf    ari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        }

    def parse(self, response):
        univlist = response.xpath("//div[@id='search-results']//a[@class='schoolname']/text()").extract()
        ranklist = response.xpath("//div[@id='search-results']//td[@class='col-program_rank']//sup/following-sibling::text()[1]").extract()
        for u, r in zip(univlist, ranklist):
            match = re.match('(.+) - .+',u)
            yield {match.group(1) : r}

        next_url = response.xpath("//div[@class='pagination']/a[text()='>']/@href").extract()
        if isinstance(next_url, basestring):
            time.sleep(5)
            yield Req('https://www.usnews.com' + next_url, headers = self.header, callback=self.parse, dont_filter=True)
