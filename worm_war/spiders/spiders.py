from __future__ import absolute_import

import json



from scrapy.exceptions import CloseSpider
from scrapy.spiders import Spider
from bs4 import BeautifulSoup

from worm_war.items import GlodItem
import django
django.setup()

# GOLD_TOU_TIAO_URL = "http://www.goldtoutiao.com/techanalysis/USOil"


class GoldGlodInfoSpider(Spider):
    name = "get_glod_info"
    allowed_domains = ["goldtoutiao.com"]
    start_urls = ['http://www.goldtoutiao.com/techanalysis/USOil']

    # start_urls = ["http://www.tudou.com/list/itemData.action?tagType=1&firstTagId=7&page=1&sort=1"]
    def parse(self, response):
        tmp ={}
        item = GlodItem()
        try:
            advice = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[1]/td[2]/span/text()')
            move_1 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[2]/td[2]/text()')
            move_2 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[2]/td[3]/text()')
            move_3 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[2]/td[4]/text()')
            technology_1 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[3]/td[2]/text()')
            technology_2 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[3]/td[3]/text()')
            technology_3 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[3]/td[4]/text()')
            for _index in range(8):
                item['composite_advice'] = advice[_index].extract().strip()
                item['average_advice'] = move_1[_index].extract().strip()
                item['average_buy'] = move_2[_index].extract().strip()
                item['average_sell'] = move_3[_index].extract().strip()
                item['technology_advice'] = technology_1[_index].extract().strip()
                item['technology_buy'] = technology_2[_index].extract().strip()
                item['technology_sell'] = technology_3[_index].extract().strip()
                item['show_data'] = _index
                yield item
            # for a,x,c,s,d,we,r in zip(advice,move_1,move_2,move_3,technology_1,technology_2,technology_3):


            # show_data = models.CharField

            # move_1 = response.xpath(# for _ele in  response.css('.content'):
            #     print _ele.xpath('')
            # res = json.loads(response.body.replace('jQuery172007327694002318719_1466997755915(', '')[:-2])
            # u = urlparse(response.url)
            # query = parse_qs(u.query)
            # query['pageNo'] = [int(query['pageNo'][0]) + 1]
            # category = query['tagId'][0]
            # item = TudouUserItem()
            #
            # if not res['list']:
            #     print 'exit %s' % response.url
            #     raise CloseSpider(reason='no more data')
            #
            # for _block in res['list']:
            #     item["uid"] = _block['userId']
            #     item["uidCode"] = _block['userCode']
            #     item["candidate"] = 1
            #     item['v_category'] = category
            #     yield item
            #
            # next_page_url = urlunparse(u._replace(query=urlencode(query, True)))
            # yield Request(next_page_url, dont_filter=True, callback=self.parse)
        except CloseSpider:
            pass
