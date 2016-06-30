from __future__ import absolute_import

import json


from urllib import urlencode
from urlparse import parse_qs, urlparse, urlunparse

from scrapy.exceptions import CloseSpider
from django.db.models import Q
from scrapy import Request

from scrapy.spiders import Spider
from scrapy.utils import engine

import django;django.setup()

GOLD_TOU_TIAO_URL = "http://www.goldtoutiao.com/techanalysis/USOil"


class GoldTouTiaoSpider(Spider):
    name = "get_tudou_user"
    allowed_domains = ["tudou.com"]
    categorys = VideoCategory.objects.filter(~Q(tudou=-1)).values_list('tudou', flat=True)
    start_urls = [CATEGORY_URL.format(category=_category, page=1) for _category in categorys]

    # start_urls = ["http://www.tudou.com/list/itemData.action?tagType=1&firstTagId=7&page=1&sort=1"]
    content
    def parse(self, response):
        try:
            res = json.loads(response.body.replace('jQuery172007327694002318719_1466997755915(', '')[:-2])
            u = urlparse(response.url)
            query = parse_qs(u.query)
            query['pageNo'] = [int(query['pageNo'][0]) + 1]
            category = query['tagId'][0]
            item = TudouUserItem()

            if not res['list']:
                print 'exit %s' % response.url
                raise CloseSpider(reason='no more data')

            for _block in res['list']:
                item["uid"] = _block['userId']
                item["uidCode"] = _block['userCode']
                item["candidate"] = 1
                item['v_category'] = category
                yield item

            next_page_url = urlunparse(u._replace(query=urlencode(query, True)))
            yield Request(next_page_url, dont_filter=True, callback=self.parse)
        except CloseSpider:
            pass
