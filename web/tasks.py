# coding:utf-8
from bs4 import BeautifulSoup
import requests
import json

from django.utils import timezone

from web.models import Yuncaijing


def get_yuncaijing_insider():
    print u'开始抓取 yuncaijing --- 时间:%s' % (timezone.localtime(timezone.now()).strftime('%F %R'))
    try:
        res = requests.get('http://www.yuncaijing.com/insider/main.html')
        body = BeautifulSoup(res.content, 'html.parser')
        soup = body.find(attrs={'class': 'main'})
        for _row in soup.findAll('li', {'class': 'pr'})[:-1]:
            _tmp = {}
            news_id = _row.find('a')['href'].split('id_')[-1].split('.')[0]
            headers = {
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
        print u'error --- %s --- 时间:%s' % (e, timezone.localtime(timezone.now()).strftime('%F %R'))