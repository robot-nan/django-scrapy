# coding: utf-8

import random
import requests
import json

import time
from bs4 import BeautifulSoup
from django.utils import timezone

from web.doc import LondonGold, LondonSilver
from web.helper import make_aware_timezone
from web.models import Yuncaijing, Guzhang
from django.conf import settings


def get_yuncaijing_insider():
    print u'Start crawl --- www.yuncaijing.com --- Time:%s' % (timezone.localtime(timezone.now()).strftime('%F %R'))
    try:
        yuncaijing_headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        res = requests.get('http://www.yuncaijing.com/insider/main.html', headers=yuncaijing_headers)
        print res.content
        body = BeautifulSoup(res.content, 'html.parser')
        soup = body.find(attrs={'class': 'main'})
        for _row in soup.findAll('li', {'class': 'pr'})[:-1]:
            _tmp = {}
            news_id = _row.find('a')['href'].split('id_')[-1].split('.')[0]
            headers = {
                "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
                "X-Requested-With": 'XMLHttpRequest'
            }
            news_info_url = 'http://www.yuncaijing.com/news/modal/' + news_id
            if u'/insider/page_' in news_info_url:
                break
            res = requests.get(news_info_url, headers=headers)
            res = json.loads(res.content)
            res = res['data']['news']
            _tmp['title'] = res['title']
            _tmp['description'] = res['description']
            _tmp['content_info'] = res['content']
            _tmp['pub_time'] = res['inputtime']
            Yuncaijing.objects.update_or_create(id=res['id'], defaults=_tmp)
    except Exception as e:
        print u'error --- %s --- Time:%s' % (e, timezone.localtime(timezone.now()).strftime('%F %R'))


def get_guzhang():
    print u'Start crawl --- www.guzhang.com --- Time:%s' % (timezone.localtime(timezone.now()).strftime('%F %R'))
    url = u'http://www.guzhang.com/e/extend/info/t.php?random=' + str(random.random())
    try:
        res = requests.get(url)
        for _index in res.json():
            news_id = int(_index[u'titleurl'].split('/')[-1])
            q = {
                'title': _index[u'title'],
                'news_text': _index[u'newstext'].strip(),
                'news_time': _index[u'newstime'],
                'real_time': _index[u'realtime'],
                'news_time_title': _index[u'newstimetitle'],
                'class_name': _index[u'classname'],
                'news_all_text': _index[u'newsalltext'].strip(),
            }
            Guzhang.objects.update_or_create(news_id=news_id, defaults=q)
    except Exception as e:
        print u'error --- %s --- Time:%s' % (e, timezone.localtime(timezone.now()).strftime('%F %R'))


def london_silver():
    """
        "lastclosingprice":"16.98",
        "price":"17.07",
        "updatetime":"2017-01-21 5:49:00",
        "buyprice":"17.08",
        "openingprice":"16.99",
        "changequantity":"0.088",
        "minprice":"16.80",
        "sellprice":"17.07",
        "maxprice":"17.15",
        "type":"白银美元",
        "changepercent":"0.47%",
        "amplitude":"2.10"
    """
    url = 'http://api.chinadatapay.com/financial/commodity/191/5?key={key}'.format(key=settings.SHUJUBAO_SILVER_KEY)
    for _time in xrange(20):
        res = requests.get(url)
        data = res.json()['data'][0]
        LondonSilver(
            type=data['type'],
            price=float(data['price']),
            changepercent=data['changepercent'],
            changequantity=float(data['changequantity']),
            openingprice=float(data['openingprice']),
            maxprice=float(data['maxprice']),
            minprice=float(data.get('minprice', 0.0)),
            lastclosingprice=float(data['lastclosingprice']),
            amplitude=float(data['amplitude']),
            buyprice=float(data['buyprice']),
            sellprice=float(data['sellprice']),
            updatetime=make_aware_timezone(data['updatetime'], '%Y-%m-%d %H:%M:%S'),
        ).save()
        time.sleep(3)


def london_gold():
    """
    {
        "code": "10000",
        "message": "成功",
        "data": [
            {
                "lastclosingprice": "1203.36",
                "price": "1201.91",
                "updatetime": "2017-01-20 22:53:00",
                "buyprice": "1202.09",
                "openingprice": "1203.60",
                "changequantity": "-1.45",
                "sellprice": "1201.91",
                "maxprice": "1209.07",
                "type": "黄金美元",
                "changepercent": "-0.14%",
                "amplitude": ".90"
            }
        ]
    }
    """
    url = 'http://api.chinadatapay.com/financial/commodity/170/5?key={key}'.format(key=settings.SHUJUBAO_GOLD_KEY)
    for _time in xrange(20):
        res = requests.get(url)
        data = res.json()['data'][0]
        LondonGold(
            type=data['type'],
            price=float(data['price']),
            changepercent=data['changepercent'],
            changequantity=float(data['changequantity']),
            openingprice=float(data['openingprice']),
            maxprice=float(data['maxprice']),
            minprice=float(data.get('minprice', 0.0)),
            lastclosingprice=float(data['lastclosingprice']),
            amplitude=float(data['amplitude']),
            buyprice=float(data['buyprice']),
            sellprice=float(data['sellprice']),
            updatetime=make_aware_timezone(data['updatetime'], '%Y-%m-%d %H:%M:%S'),
        ).save()
        time.sleep(3)
