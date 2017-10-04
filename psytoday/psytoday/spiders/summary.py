# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Request as Req

class SummarySpider(scrapy.Spider):
    name = 'summary'
    allowed_domains = ['psychologytoday.com']
    start_urls = ['https://therapists.psychologytoday.com/rms/prof_results.php?sid=1496611071.9758_12177&city=San+Diego&state=CA&rec_next=1']
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OSX 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome 39.0.2171.95 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        }
    npage = 0
    Npage = 100

    def parse(self, response):
        self.npage += 1
        urllist = response.xpath("//div[@class='hidden-xs result-actions']/a[@class='btn btn-gray btn-small']/@href").extract()
        for personal_url in urllist:
            time.sleep(2)
            yield Req(personal_url, headers = self.header, callback=self.subparse)
            #yield {'url': t}
        
        next_url = response.xpath("//a[@title='More Therapists in San Diego, San Diego County, California']/@href").extract_first()
        if (len(next_url)>0) and (self.npage <= self.Npage):#isinstance(next_url, basestring):
            time.sleep(5)
            yield Req(next_url, headers = self.header, callback=self.parse, dont_filter=True)

    def subparse(self, response):
        idict = {}
        ## personal
        # name
        iname = response.xpath("//h1[@itemprop='name']/text()").extract_first()
        print('=============== ' + iname.strip() + '================')
        idict['name'] = iname.strip()
        
        # title
        ititle = list(set(response.xpath("//div[@class='profile-title']//span/text()").extract()))
        idict['title'] = ititle
        
        # years in practice (may be absent)
        iyears = response.xpath("//strong[text()='Years in Practice:']/following-sibling::text()").extract_first()
        if iyears:
            idict['years_practice'] = iyears.strip()
        
        # school (may be absent)
        ischool = response.xpath("//strong[text()='School:']/following-sibling::text()").extract_first()
        if ischool:
            idict['school'] = ischool.strip()
        
        # graduation year (may be absent)
        igraduate = response.xpath("//strong[text()='Year Graduated:']/following-sibling::text()").extract_first()
        if igraduate:
            idict['graduate_year'] = igraduate.strip()
        
        # insurance
        iinsurance = response.xpath("//strong[text()='Accepted Insurance Plans']/following-sibling::div[@class='spec-list']//li/text()").extract()
        idict['insurance'] = iinsurance
        
        ## Specialties
        ispecialty = response.xpath("//div[@class='spec-list'][1]/div[@class='row']//li[@class='highlight']/text()").extract()
        if ispecialty:
            idict['specialties'] = ispecialty
        
        categories = response.xpath("//div[@class='spec-list']/h2/text()").extract()
        print '================================categories==========================================='
        print categories
        print '==========================================================================='
        for cat in range(len(categories)):
            tmp = response.xpath("//div[@class='spec-list'][cat+1]")
            #subcategories = tmp.xpath(".//h3/text()").extract()
            subcategories = response.xpath("//div[@class='spec-list'][cat+1]//h3/text()").extract()
            print '=============================subcategories of '+ categories[cat]+ '============================================='
            print subcategories
            print '==========================================================================='

            for sub in range(len(subcategories)-1):
                iname = subcategories[sub]
                ivalue = response.xpath("//div[@class='spec-list'][1]/h3[sub+1]/following-sibling::div[count(. | //div[@class='spec-list'][1]/h3[sub+2]/preceding-sibling::div) = count(//div[@class='spec-list'][1]/h3[sub+2]/preceding-sibling::div)]//li").extract()
                idict[iname] = ivalue
            try:
                iname = subcategories[-1]
                ivalue = tmp.xpath("./h3[len(subcategories)]/following-sibling::div//li/text()").extract()
                idict[iname] = ivalue
            except:
                iname = None
        yield idict

