# coding:utf-8
import datetime
import json

import pandas
import tushare as ts
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from pandas.tseries.offsets import BDay

from finance.helper import TushareStock
from django.views.decorators.clickjacking import xframe_options_exempt
from datetime import datetime, timedelta
from finance.models import StockPoint


@xframe_options_exempt
def ticks(request, code):
    ts = TushareStock(code)
    context = ts.code_base_info()
    context['code'] = code
    context['show'] = int(request.GET.get('show', 1))
    context['height'] = request.GET.get('height','414')
    context['show_point'] = request.GET.get('show_point', '0')
    return render(request, 'k_line.html', context)

@xframe_options_exempt
def get_k_ticks_data(request, code):
    try:
        df = ts.get_today_ticks(code)
    except:
        today = pandas.datetime.today()
        df = ts.get_tick_data(code, date=(today - BDay(1)).strftime('%Y-%m-%d'))
    context = {}
    context['point'] = []
    context['time'] = df.to_dict().get('time').values()
    context['price'] = df.to_dict().get('price').values()
    context['pchange'] = df.to_dict().get('pchange',{}).values()
    context['change'] = df.to_dict().get('change').values()
    context['volume'] = df.to_dict().get('volume').values()
    context['amount'] = df.to_dict().get('amount').values()
    context['type'] = df.to_dict().get('type').values()
    for _index in StockPoint.objects.filter(code=code, date=timezone.now().strftime('%Y-%m-%d')):
        _type = _index.type
        context['point'].append(
            {
                'name': u'卖' if _type == 'sell' else u'买',
                'coord': [_index.time, _index.price],
                'itemStyle': {
                    'normal': {'color': 'red' if _type == 'sell' else 'green'}
                }
            }
        )
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
    context = ts.code_base_info()
    context['code'] = code
    context['type'] = type
    context['show'] = int(request.GET.get('show', 1))
    context['data'] = json.dumps(ts.history_data[::-1].to_dict(orient='split')['data'][::-1])
    context['height'] = request.GET.get('height','414')
    return render(request, 'day_k_line.html', context)


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
