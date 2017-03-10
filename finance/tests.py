#!/usr/bin/env python
# -*- coding: gb2312 -*-
from mongoengine import *
import time
import datetime
# import TradeX
MARKETS = [
    {13: '111081'},
    {13: '111082'},
]
MONGO_HOST = 'dds-m5ea0fc94e106de42.mongodb.rds.aliyuncs.com'
MONGO_PORT = 3717
MONGO_DATABASE = 'finance'
MONGO_USERNAME = 'root'
MONGO_PASSWORD = '1234qwer'


connect(MONGO_DATABASE, host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USERNAME,
        password=MONGO_PASSWORD)


class FuturesTimeSharing(Document):
    market = IntField()
    code = StringField(max_length=32)
    update_time = DateTimeField()
    list_data = ListField()


class FuturesK(Document):
    market = IntField()
    type = IntField()
    code = StringField(max_length=32)
    update_time = DateTimeField()
    list_data = ListField()


class Finance(object):
    def __init__(self, host="59.175.238.38", port=7727, ):
        self.host = host
        self.port = port
        self.conn = TradeX.TdxExHq_Connect(self.host, self.port)

    def item_infomation(self, market_num, item_name):
        res = self.conn.GetInstrumentQuote(market_num, item_name)

        return self.__format_data(res)

    def item_K(self, market, item_name, start=0, count=200, d_type=9):
        """
        type:K线种类
                0 = 5分钟K线
                1 = 15分钟K线
                2 = 30分钟K线
                3 = 1小时K线
                4 = 日K线
                5 = 周K线
                6 = 月K线
                7 = 1分钟
                8 = 1分钟K线
                9 = 日K线
                10 = 季K线
                11 = 年K线
        """
        res = self.conn.GetInstrumentBars(d_type, market, item_name, start, count)
        return self.__format_data(res)

    def time_sharing(self, market, item_name, start=0, count=200):
        # 分时图
        res = self.conn.GetTransactionData(market, item_name, start, count)  # count 为整型
        return self.__format_data(res)

    def __format_data(self, res):
        context = []
        titles = res[1].split('\n')[0]
        values = res[1].split('\n')[1:]
        for _line_value in values:
            tmp = {}
            for _title, _value in zip(titles.split('\t'), _line_value.split('\t')):
                title = _title.decode('gbk')
                tmp[title] = _value
            context.append(tmp)
        return context


if __name__ == '__main__':
    FuturesTimeSharing.objects.all().delete()
    FuturesK.objects.all().delete()

    # f = Finance()
    # for i in xrange(20):
    #     _datetime = datetime.datetime.now()
    #     print _datetime.strftime('%Y-%m-%d %H:%M:%S')
    #     try:
    #         for market in MARKETS:
    #             for _market, name in market.iteritems():
    #                 res = f.time_sharing(_market, name)
    #                 FuturesTimeSharing.objects(market=_market, code=name).update_one(
    #                     list_data=res,
    #                     update_time=_datetime,
    #                     upsert=True
    #                 )
    #                 for i in xrange(12):
    #                     res = f.item_K(_market, name, d_type=i)
    #                     FuturesK.objects(market=_market, code=name, type=i).update_one(
    #                         list_data=res,
    #                         update_time=_datetime,
    #                         upsert=True
    #                     )
    #         time.sleep(2)
    #     except:
    #         pass
