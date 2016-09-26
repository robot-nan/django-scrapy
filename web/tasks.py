# coding: utf-8

import random
import requests
import json
from bs4 import BeautifulSoup
from django.utils import timezone
from web.models import Yuncaijing, Guzhang

def get_yuncaijing_insider():
    print u'Start crawl --- www.yuncaijing.com --- Time:%s' % (timezone.localtime(timezone.now()).strftime('%F %R'))
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
