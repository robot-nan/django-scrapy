# coding:utf-8
import json
import urllib2
import requests
from collections import OrderedDict

from django.http import JsonResponse
from bs4 import BeautifulSoup
from django.utils import timezone
from lxml import etree

from web.models import Yuncaijing


def gold_advice(request):
    url = 'http://www.goldtoutiao.com/techanalysis/USOil'
    response = urllib2.urlopen(url)
    item = []
    htmlparser = etree.HTMLParser()
    response = etree.parse(response, htmlparser)
    advice = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[1]/td[2]/span/text()')
    move_1 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[2]/td[2]/text()')
    move_2 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[2]/td[3]/text()')
    move_3 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[2]/td[4]/text()')
    technology_1 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[3]/td[2]/text()')
    technology_2 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[3]/td[3]/text()')
    technology_3 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[3]/td[4]/text()')
    for _index in range(8):
        tmp = {}
        tmp['composite_advice'] = advice[_index].strip()
        tmp['average_advice'] = move_1[_index].strip()
        tmp['average_buy'] = move_2[_index].strip()
        tmp['average_sell'] = move_3[_index].strip()
        tmp['technology_advice'] = technology_1[_index].strip()
        tmp['technology_buy'] = technology_2[_index].strip()
        tmp['technology_sell'] = technology_3[_index].strip()
        tmp['show_data'] = _index
        item.append(tmp)

    return JsonResponse({'data': item, 'now_time': timezone.now()})


def get_kxt(request, date=None):
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
    }
    res = requests.get('http://www.kxt.com/cjrl/ajax?date={date}'.format(date=date), headers=headers)
    res = json.loads(res.content)
    soup = BeautifulSoup(res['data']['pc']['cjDataHtml'], 'html.parser')
    soup = soup.find_all(attrs={'class': 'rlDateItem'})
    item = []
    for _row in soup:
        tmp = {}
        line = _row.find_all('td')
        tmp['time'] = line[0].text
        tmp['region'] = {'name': line[1].find('img').get('alt'), 'src': line[1].find('img').get('src')}
        tmp['title'] = line[2].text
        tmp['important'] = line[3].text
        tmp['previous_value'] = line[4].text
        tmp['predict_value'] = line[5].text
        tmp['publish'] = line[6].text
        tmp['judge'] = line[7].text
        item.append(tmp)
    return JsonResponse({'data': item, 'now_time': timezone.now()})


def get_investing(request):
    url = "http://cn.investing.com/technical/%E5%95%86%E5%93%81-%E6%8C%87%E6%A0%87"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    data = OrderedDict((
        ('gold', []),
        ('silver', []),
        ('copper', []),
        ('oil', []),
        ('gas', []),
        ('wheat', []),
    ))
    for _num in xrange(0, 11 + 1):
        info_soup = soup.find_all(attrs={'id': 'pair_{num}'.format(num=_num)})
        res_soup = soup.find_all(attrs={'class': 'movingAveragesTbl'})
        for _value, _res, _key in zip(info_soup, res_soup, data):
            _tmp = _res.find_all('td')[:-1]
            _buy = _tmp[0].text
            _sale = _tmp[1].text
            _mid = _tmp[2].text
            _summary = _res.find('span').text

            data[_key].append({'name': _value.find(attrs={'id': 'pair_name_{num}'.format(num=_num)}).text,
                               'value': _value.find(attrs={'id': 'open_{num}'.format(num=_num)}).text,
                               'res':
                                   {
                                       'buy': _buy,
                                       'sale': _sale,
                                       'mid': _mid,
                                       'summary': _summary
                                   },
                               'action': _value.find('span').text
                               }
                              )




    return JsonResponse({'data': data, 'now_time': timezone.now()})

# import grequests
#
#
# def exception_handler(request, exception):
#     print "Request failed"
#
#
# urls = [
#     'http://www.baidu.com',
#     'http://www.hao123.com',
#     'http://www.163.com',
#     'http://www.taobao.com', 'http://www.baidu.com',
#     'http://www.hao123.com',
#     'http://www.163.com',
#     'http://www.taobao.com', 'http://www.baidu.com',
#     'http://www.hao123.com',
#     'http://www.163.com',
#     'http://www.taobao.com', 'http://www.baidu.com',
#     'http://www.hao123.com',
#     'http://www.163.com',
#     'http://www.taobao.com', 'http://www.baidu.com',
#     'http://www.hao123.com',
#     'http://www.163.com',
#     'http://www.taobao.com', 'http://www.baidu.com',
#     'http://www.hao123.com',
#     'http://www.163.com',
#     'http://www.taobao.com', 'http://www.baidu.com',
#     'http://www.hao123.com',
#     'http://www.163.com',
#     'http://www.taobao.com',
# ]
# rs = (grequests.get(u) for u in urls)
# grequests.map(rs)
