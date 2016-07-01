# coding:utf-8
import urllib2


from django.http import JsonResponse, HttpResponse
from lxml import etree

def glod_advice(request):
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

    return JsonResponse({'data': item})
