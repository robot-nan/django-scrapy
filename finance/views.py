# coding:utf-8
import datetime
import tushare as ts
from django.shortcuts import render


def get_k_day_data(request, code):
    now_day = datetime.datetime.now()
    last_day = now_day + datetime.timedelta(days=-1)
    last_day = last_day.strftime('%Y-%m-%d')
    context = {}
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
    return render(request,'k_line.html',context)