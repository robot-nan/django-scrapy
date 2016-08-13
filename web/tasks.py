from bs4 import BeautifulSoup
import requests
import json
from web.models import Yuncaijing


def get_yuncaijing_insider():
    res = requests.get('http://www.yuncaijing.com/insider/main.html')
    body = BeautifulSoup(res.content, 'html.parser')
    soup = body.find(attrs={'class': 'main'})
    for _row in soup.findAll('li', {'class': 'pr'})[:-1]:
        _tmp={}
        news_id = _row.find('a')['href'].split('id_')[-1].split('.')[0]
        headers = {
            "X-Requested-With": 'XMLHttpRequest'
        }
        news_info_url = 'http://www.yuncaijing.com/news/modal/' + news_id
        _res = requests.get(news_info_url, headers=headers)
        _res = json.loads(_res.content)
        _res = _res['data']['news']
        _tmp['title'] = _res['title']
        _tmp['description'] = _res['description']
        _tmp['content_info'] = _res['content']
        _tmp['pub_time'] = _res['inputtime']
        Yuncaijing.objects.update_or_create(id=_res['id'], defaults=_tmp)
