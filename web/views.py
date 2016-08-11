# coding:utf-8
import json
import urllib2

import requests
from django.http import JsonResponse
from bs4 import BeautifulSoup
from django.utils import timezone
from lxml import etree


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
    res = requests.get('http://www.kxt.com/cjrl/ajax?date={date}'.format(date=date),headers=headers)
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


def get_yuncaijing(request):
    item = []

    res = requests.get('http://www.yuncaijing.com/neican')
    body = BeautifulSoup(res.content, 'html.parser')
    soup = body.find(attrs={'class': 'neican-list'})
    for _row in soup.find_all('li'):
        tmp = {}
        try:
            tmp['time'] = _row.find('time').text
            tmp['title'] = _row.find(attrs={'class': 'tit'}).text
            tmp['content'] = _row.find(attrs={'class': 'normal-text'}).text
            item.append(tmp)
        except:
            pass
            # modal_id = _row.find(attrs={'class': 'url'})['data-target'].replace('#','')
            # modal = body.find(attrs={'id':modal_id})
            # print modal.find(attrs={'class':'uglify-arcticle'})

    return JsonResponse({'data': item, 'now_time': timezone.now()})


def get_yuncaijing_insider(request):
    item = []
    url = request.GET.get('url', '')
    if url:
        res = requests.get(url)
    else:
        res = requests.get('http://www.yuncaijing.com/insider/main.html')
        body = BeautifulSoup(res.content, 'html.parser')
        soup = body.find(attrs={'class': 'main'})
        for _row in soup.findAll('li', {'class': 'pr'}):
            tmp = {}
            try:
                tmp['time'] = _row.find('kbd').text.strip()
                tmp['title'] = _row.find('a').text.strip()
                tmp['content'] = _row.find(attrs={'class', 'nc-con'}).text.strip()
                tmp['content_info_url'] = 'http://www.yuncaijing.com' + _row.find('a')['href']

                item.append(tmp)
            except:
                pass
    return JsonResponse({'data': item, 'content_info': res.content, 'now_time': timezone.now()})
#
#
# #
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
