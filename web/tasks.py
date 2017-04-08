# coding: utf-8

import random
import tushare as ts
import traceback
import requests
import json
from bs4 import BeautifulSoup
from django.utils import timezone
from web.doc import FinanceInfo, StackSettings, StackDatas
from web.models import Yuncaijing, Guzhang
from django.conf import settings
from web.user_agents import USER_AGENTS


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


def get_finance_brief():
    url = "https://hk.investing.com/common/technical_studies/technical_studies_data.php?action=get_studies&pair_ID={id}&time_frame=900"

    finance = {
        u"白银": 8836,
        u"黄金": 8830,
        u"铜": 8831,
        u"原油": 8849,
        u"天然气": 8862,
        u"小麦": 8917,
        u"大豆": 8916
    }
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
    }
    for _name in finance:
        while 1:
            try:
                res = requests.get(url.format(id=finance[_name]), headers=headers)

                if res.status_code == 200:
                    all_info = res.content.split('</style>')[-1].split('<dl class="splitbar">')[0].strip().split('*;*')
                    datas = {}
                    for i in all_info:
                        _key = i.split('=')[0]
                        _value = i.split('=')[1]
                        datas[_key] = _value.decode('utf8')

                    FinanceInfo.objects(name=_name, code=str(finance[_name])).update_one(
                        updatetime=timezone.now(),
                        data=datas,
                        upsert=True
                    )

                    break
            except:
                print traceback.format_exc()


def get_stack_code():
    res = ts.get_stock_basics()
    codes = res['name'].to_dict().keys()
    StackSettings.objects(name='stack_list').update_one(
        updatetime=timezone.now(),
        list_data=codes,
        upsert=True
    )


def get_k_datas():
    headers = {
        'Authorization': 'APPCODE ' + settings.ALIYUN_STOCK_APP_CODE
    }
    times = [u'5', u'30', u'60', u'day', u'week', u'month']
    url = "http://ali-stock.showapi.com/realtime-k?code={code}&time={time}"
    codes = StackSettings.objects.filter(name='stack_list').first().list_data
    for _code in codes:
        for _time in times:
            _url = url.format(code=_code, time=_time)
            res = requests.get(_url, headers=headers)
            res = res.json()
            if not res['showapi_res_error']:
                StackDatas.objects(code=_code, time=_time).update_one(
                    updatetime=timezone.now(),
                    data=res,
                    upsert=True
                )
            else:
                print timezone.now(), '===', _code, '===', _time, '===', res, '\n'


def finanace_base_info():
    '''
    https://apimarkets.wallstreetcn.com/v1/quote/XAUUSD
    XAUUSD 黄金
    XAGUSD 白银
    USOil 原油
    Copper 铜
    AUTD 黄金TD
    AGTD 白银TD
    :return: 
    '''
    finance_list = {
        "XAUUSD": u'黄金',
        "XAGUSD": u'白银',
        "USOil": u'原油',
        "Copper": u'铜',
        "AUTD": u'黄金T+D',
        "AGTD": u'白银',
    }
    price_base_url = 'https://apimarkets.wallstreetcn.com/v1/price'
    info_base_url = r'https://apimarkets.wallstreetcn.com/v1/quote/'

    for _code, _name in finance_list.iteritems():
        datas = {}
        params = {
            "symbol": _name
        }
        res = requests.get(price_base_url, params=params)
        data = res.json()['results'][0]
        datas['price'] = data['price']
        datas['change'] = data['change']
        datas['changePercent'] = data['changePercent']
        url = info_base_url + _code
        res = requests.get(url)
        data = res.json()['results']
        datas['open'] = data['open']
        datas['close'] = data['prevClose']
        datas = dict((("set__data__%s" % k, v) for k, v in datas.iteritems()))
        FinanceInfo.objects(name=_name, code=_code).update(**datas)
