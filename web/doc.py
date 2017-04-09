# coding:utf-8
from django.conf import settings
from mongoengine import *

connect(settings.MONGO_DATABASE, host=settings.MONGO_HOST, port=settings.MONGO_PORT, username=settings.MONGO_USERNAME,
        password=settings.MONGO_PASSWORD)


class LondonGold(Document):
    """
    伦敦黄金
    :接口返回值
    名称	                类型	        必填	    说明
    type	            string	    否	    品种代号
    price	            string	    否	    最新价
    changepercent	    string	    否	    涨跌幅
    changequantity	    string	    否	    涨跌量
    openingprice	    string	    否	    开盘价
    maxprice	        string	    否	    最高价
    minprice	        string	    否	    最低价
    lastclosingprice	string	    否	    昨收盘价
    amplitude	        string	    否	    振幅
    buyprice	        string	    否	    买入价
    sellprice	        string	    否	    卖出价
    updatetime	        string	    否	    更新时间
    """

    name = StringField(max_length=32)
    price = FloatField()
    changepercent = StringField(max_length=32)
    changequantity = FloatField()
    openingprice = FloatField()
    maxprice = FloatField()
    minprice = FloatField()
    lastclosingprice = FloatField()
    amplitude = FloatField()
    buyprice = FloatField()
    sellprice = FloatField()
    updatetime = DateTimeField()


class LondonSilver(Document):
    """
    {
        "code":"10000",
        "message":"成功",
        "data":[
            {
                "lastclosingprice":"16.98",
                "price":"17.07",
                "updatetime":"2017-01-21 5:49:00",
                "buyprice":"17.08",
                "openingprice":"16.99",
                "changequantity":"0.088",
                "minprice":"16.80",
                "sellprice":"17.07",
                "maxprice":"17.15",
                "type":"白银美元",
                "changepercent":"0.47%",
                "amplitude":"2.10"
            }
        ]
    }
    """
    name = StringField(max_length=32)
    price = FloatField()
    changepercent = StringField(max_length=32)
    changequantity = FloatField()
    openingprice = FloatField()
    maxprice = FloatField()
    minprice = FloatField()
    lastclosingprice = FloatField()
    amplitude = FloatField()
    buyprice = FloatField()
    sellprice = FloatField()
    updatetime = DateTimeField()


class FinanceInfo(Document):
    code = StringField(max_length=32)
    name = StringField(max_length=32)
    web_site = StringField(max_length=256)
    updatetime = DateTimeField()
    data = DictField()


class StackDatas(Document):
    code = IntField()
    time = StringField(max_length=8)
    updatetime = DateTimeField()
    data = DictField()


class StackSettings(Document):
    name = StringField(max_length=32)
    updatetime = DateTimeField()
    list_data = ListField()


class FuturesTimeSharing(Document):
    market = IntField()
    code = StringField(max_length=32)
    list_data = ListField()


class FuturesK(Document):
    market = IntField()
    type = IntField()
    code = StringField(max_length=32)
    update_time = DateTimeField()
    list_data = ListField()
