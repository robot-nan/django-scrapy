# coding:utf-8
import datetime
import tushare as ts
from django.http import JsonResponse
from django.shortcuts import render

from finance.helper import TushareStock


def get_k_day_data(request, code):
    now_day = datetime.datetime.now()
    last_day = now_day + datetime.timedelta(days=-1)
    last_day = last_day.strftime('%Y-%m-%d')
    context = {}
    code = str(code)
    res_day = ts.get_hist_data(code)
    res_5 = ts.get_hist_data(code, ktype='5')
    res_15 = ts.get_hist_data(code, ktype='15')
    res_30 = ts.get_hist_data(code, ktype='30')
    res_60 = ts.get_hist_data(code, ktype='60')
    context = {
        'day': res_day.to_json(orient='split'),
        'min5': res_5.to_json(orient='split'),
        'min15': res_15.to_json(orient='split'),
        'min30': res_30.to_json(orient='split'),
        'min60': res_60.to_json(orient='split'),
    }
    return render(request, 'k_line.html', context)


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
