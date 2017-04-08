# coding:utf-8
import json
import random
import re

import urllib2
import requests
import tushare as ts
from collections import OrderedDict
from django.http import JsonResponse
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.utils import timezone
from lxml import etree
from user_agents import USER_AGENTS
from web.doc import FinanceInfo

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"


def gold_advice(request):
    url = 'http://www.goldtoutiao.com/techanalysis/USOil'
    response = urllib2.urlopen(url)
    item = []
    htmlparser = etree.HTMLParser()
    response = etree.parse(response, htmlparser)
    advice = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[1]/td[2]/span/text')
    move_1 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[2]/td[2]/text')
    move_2 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[2]/td[3]/text')
    move_3 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[2]/td[4]/text')
    technology_1 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[3]/td[2]/text')
    technology_2 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[3]/td[3]/text')
    technology_3 = response.xpath('//*[@id="tech-analysis"]/div[3]/ul/li/table[1]/tbody/tr[3]/td[4]/text')
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


def get_investing(request, code):
    res = FinanceInfo.objects.filter(code=code).first().data
    return JsonResponse(res)


def wezone(request, code):
    data = {}
    res = requests.get('http://wx.wezone.wang/stock/detail?code=' + code)
    code = re.findall('"http://hq.sinajs.cn/list=(?P<date>.*)"', res.content)[0]
    url = 'http://hq.sinajs.cn/list=' + code
    _res = requests.get(url)

    now_price = _res.content.split(',')[3]
    last_price = _res.content.split(',')[2]
    # 现价
    data['xj'] = now_price
    # 涨跌幅
    last_price = float(last_price)
    now_price = float(now_price)
    data['zd'] = now_price - last_price
    # 涨跌
    data['zdf'] = (now_price - last_price) / last_price * 100
    soup = BeautifulSoup(res.content, 'html.parser')
    data['name'] = soup.title.text
    # 机构评级
    data['jgpj'] = soup.select('.am-panel-default.doc-content table tr .am-text-default')[0].text
    _soup = soup.select('.am-panel-default.doc-content table tr')[1]
    # 综合评分
    data['scores'] = _soup.select('td span')[0].text
    # 打败多少人
    data['pk'] = _soup.select('td div')[2].text
    # 诊断说明
    data['des'] = _soup.select('.mydiv')[0].text.strip()

    for _block_soup in soup.select('.am-g.am-g-fixed section'):
        _main_key = _block_soup.select('div h3')[0].text
        data[_main_key] = {}
        for _row in _block_soup.find_all('tr'):
            try:
                _key = _row.find_all('td')[0].text
                _value = _row.find_all('td')[1].text
                data[_main_key][_key] = _value
            except:
                pass
    return JsonResponse({'data': data, 'now_time': timezone.now()})


def stock_finance_sina(request, code):
    url = 'http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/singleqgqp/index.phtml?num=60&symbol=' + code
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    trs = soup.select('table tr')
    res = {}
    for _row in trs[1:]:
        _code = _row.find_all('td')[0].text
        _name = _row.find_all('td')[1].text
        _data = _row.find_all('td')[2].text
        _comment = _row.find_all('td')[3].text
        res[_data] = [_code, _name, _comment]
    return JsonResponse(res, safe=False)


def caiku(request, code):
    url = 'http://www.caiku.com/stock/' + code + '/pick.html'
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }
    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.content, 'html.parser')
    prediction_price = soup.select('.st_dt_ri_btm table .tal')[1].text.replace(u'元', '')
    up = soup.select('.yl')[0].text.split()[-1]
    down = soup.select('.yr')[0].text.split()[-1]
    content = {
        'prediction_price': prediction_price,
        'up': up,
        'down': down
    }
    return JsonResponse(content)


def jqka(request, code):
    url = 'http://doctor.10jqka.com.cn/' + code
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    score = soup.select_one('.bignum').text + '.' + soup.select_one('.smallnum').text
    # print '分数', score
    score_description = soup.select_one('.stocktotal').text
    # print '分数 评论', score_description
    short = soup.select_one('.short').text
    mid = soup.select_one('.mid').text
    long = soup.select_one('.long').text
    # print '短期', short
    # print '中期', mid
    # print '长期', long
    title = soup.select_one('.title').text.replace(u'更多连续上涨股票>>', '')
    # print '标题', title
    title_info = soup.select_one('.cnt').text
    # print '标题内容', title_info
    yingyun = soup.select_one('.bd.indexStat .hd2').text.strip()
    pressure = soup.select_one('#nav_technical > div > div.nx_items > div.box3.indexStat > div.hd2').text
    muti = soup.select_one('#nav_technical > div > div.nx_items > div:nth-of-type(4) > div.hd2').text
    # print '标题内容', pressure
    # print '标题内容', muti

    content = {
        'score': score,
        'score_description': score_description,
        'short': short,
        'mid': mid,
        'long': long,
        'title': title,
        'title_info': title_info,
        'pressure': pressure,
        'muti': muti,
        'yingyun': yingyun
    }

    return JsonResponse(content)


def stock_price(request, code):
    return JsonResponse({'data': ts.get_realtime_quotes(code).iloc[0].price})


def stock_open_height_amount(request, code):
    context = {}
    df = ts.get_realtime_quotes(code)  # Single stock symbol
    context['name'] = df[['name']].iloc[0]['name']
    context['price'] = df[['price']].iloc[0]['price']
    # context['stock_zd'] = 0
    context['open'] = df[['open']].iloc[0]['open']
    # context['stock_yestoday_close'] =0
    context['height'] = df[['high']].iloc[0]['high']
    context['low'] = df[['low']].iloc[0]['low']
    context['amount'] = df[['amount']].iloc[0]['amount']
    context['time'] = df[['date']].iloc[0]['date'] + '  ' + df[['time']].iloc[0]['time']
    return JsonResponse(context)


def stock_today_ditail(request, code):
    """
    name，股票名字
    open，今日开盘价
    pre_close，昨日收盘价
    price，当前价格
    high，今日最高价
    low，今日最低价，竞买价，即“买一”报价
    ask，竞卖价，即“卖一”报价
    volume，成交量 maybe you need do volume/100
    amount，成交金额（元 CNY）
    date，日期；
    time，时间；
    """
    context = {}
    df = ts.get_realtime_quotes(code)
    context['name'] = df.iloc[0]['name']
    context['open'] = df.iloc[0]['open']
    context['pre_close'] = df.iloc[0]['pre_close']
    context['price'] = df.iloc[0]['price']
    context['high'] = df.iloc[0]['high']
    context['low'] = df.iloc[0]['low']
    context['ask'] = df.iloc[0]['ask']
    context['volume'] = df.iloc[0]['volume']
    context['amount'] = df.iloc[0]['amount']
    context['time'] = df.iloc[0]['amount']
    context['date'] = df.iloc[0]['amount']
    return JsonResponse(context)


def piano(request):
    context={}
    values = ['bEm', '#G', 'bBm', '#FM', 'Dm', '#Gm', 'Bm', 'Fm', 'A', 'C', 'B', 'E', 'D', 'G', 'F', '#Cm', 'GM', 'fm', 'Em', 'bE', '#Fm', 'Cm', 'bB', '#C', 'Am', '#F', '#CM', 'Gm']
    random.shuffle(values)
    context['data_list'] = values
    return render(request, 'piano.html', context)


