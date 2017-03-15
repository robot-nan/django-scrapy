# coding:utf-8
import json
import requests
import time

from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from finance.helper import TushareStock, stock_info
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings
from finance.models import StockPoint
from web.doc import FuturesK


@xframe_options_exempt
def ticks(request, code):
    context = stock_info(code)
    context['code'] = code
    context['show'] = int(request.GET.get('show', 1))
    context['height'] = request.GET.get('height', '414')
    context['show_point'] = request.GET.get('show_point', '0')
    context['start'] = request.GET.get('start', 50)
    context['end'] = request.GET.get('end', 100)

    return render(request, 'k_line.html', context)


@xframe_options_exempt
def get_k_ticks_data(request, code, days=1):
    headers = {
        'Authorization': 'APPCODE ' + settings.ALIYUN_STOCK_APP_CODE
    }
    url = 'http://ali-stock.showapi.com/timeline?code={code}&day={days}'.format(code=code, days=days)
    res = requests.get(url, headers=headers)
    context = {}
    context['data'] = res.json()
    return JsonResponse(context)


@xframe_options_exempt
def get_day_k_line(request, code):
    """
    D=日k线 W=周 M=月
    5=5分钟 15=15分钟
    30=30分钟 60=60分钟
    """
    type = request.GET.get('type', 'D')
    ts = TushareStock(code, type)
    context = stock_info(code)
    context['code'] = code
    context['type'] = type
    context['start'] = request.GET.get('start', 50)
    context['end'] = request.GET.get('end', 100)
    context['show'] = int(request.GET.get('show', 1))
    context['data'] = json.dumps(ts.history_data[::-1].to_dict(orient='split')['data'][::-1])
    context['height'] = request.GET.get('height', '414')
    return render(request, 'day_k_line.html', context)


def today_buy_point(request, code):
    ts = TushareStock(code)
    return JsonResponse(ts.today_buy_point(), safe=False)


def stop_loss(request, code):
    ts = TushareStock(code)
    return JsonResponse(ts.stop_loss(), safe=False)


def stop_make_money(request, code):
    ts = TushareStock(code)
    return JsonResponse(ts.stop_make_money(), safe=False)


def drag(request, code):
    ts = TushareStock(code)
    return JsonResponse(ts.drag(), safe=False)


def tomorrow_buy_point(request, code):
    ts = TushareStock(code)
    return JsonResponse(ts.tomorrow_buy_point(), safe=False)


def set_point(request):
    if request.method == 'POST':
        date = timezone.now().strftime('%Y-%m-%d')
        code = request.POST.get('code')
        price = request.POST.get('price')
        time = request.POST.get('date')
        type = request.POST.get('type')
        StockPoint.objects.create(
            date=date,
            code=code,
            price=price,
            time=time,
            type=type
        )
        return JsonResponse({'successful': 1})
    else:
        return render(request, 'k_line_manager.html')


def tradingview(request):
    return render(request, 'tradingview.html')


def tradingview_config(request):
    q = {"supports_search": True, "supports_group_request": False, "exchanges": [{"value": "", "name": "All Exchanges", "desc": ""}], "symbolsTypes": [{"name": "All types", "value": ""}, {"name": "CFD", "value": "cfdindice"}, {"name": "Bond", "value": "bond"}, {"name": "Index", "value": "index"}, {"name": "Commodity", "value": "commodity"}, {"name": "Forex", "value": "forex"}, {"name": "Stock", "value": "stock"}], "supportedResolutions": [1, 5, 15, 30, 60, 240, "1D", "1W", "1M"]}
    return JsonResponse(q)


def search(request):
    pass


def symbol_info(request):
    q = {"description": u"纽约黄金",
         "has_no_volume": True,
         "session": "24x7",
         "has_intraday": True,
         "timezone": "UTC",
         "ticker": {},
         "minmov2": 0,
         # "name": "111081",
         "type": "stock",
         "intraday_multipliers": ["1", "5", "15", "30", "60", "240"],
         "minmov": 1,
         "exchange-traded": "",
         "pricescale": 100,
         "exchange-listed": ""}
    return JsonResponse(q)


def markets(request):
    datas = FuturesK.objects.filter(market=13, code='111081', type=9).first()
    datas.list_data['t'] = map(lambda x: int(time.mktime(time.strptime(x, '%Y%m%d'))), datas.list_data['t'])
    print datas.list_data['t']
    return JsonResponse(datas.list_data)
