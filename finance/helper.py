# coding:utf-8
import datetime
import pytz
import tushare

TZ = pytz.timezone('Asia/Shanghai')


class TushareStock(object):
    def __init__(self, code='600848'):
        self.code = code
        self.history_data = tushare.get_hist_data(code=code)

    def yesterday_formart(self):
        # 要判断是否过了3点
        now_day = datetime.datetime.now(TZ)
        if now_day.hour > 15:
            # 大于15点就拿当日的记录
            return now_day.strftime('%Y-%m-%d')

        yesterday = now_day - datetime.timedelta(days=1)
        return yesterday.strftime('%Y-%m-%d')

    def day_formart(self, days):
        time = datetime.datetime.now(TZ) - datetime.timedelta(days=days)
        return time.strftime('%Y-%m-%d')

    def yesterday_open_price(self):
        # 昨日开盘价
        return self.history_data.head(1).iloc[0]['open']

    def yesterday_high_price(self):
        # 昨日最高价
        return self.history_data.head(1).iloc[0]['high']

    def yesterday_low_price(self):
        # 昨日最低价
        return self.history_data.head(1).iloc[0]['low']

    def today_buy_point(self):
        # 今日买点 :昨日 ((开盘价 + 最高价 + 最低价) / 3 * 2 * (3 - 1)) / (3 + 1)
        open = self.yesterday_open_price()
        high = self.yesterday_high_price()
        low = self.yesterday_low_price()
        return (sum([open, high, low]) / 3 * 2 * (3 - 1)) / (3 + 1)

    def stop_loss(self):
        # 止损价：不包括当天   5日内收盘价的最高值*0.95
        return tushare.get_hist_data(code=self.code).head(5).close.max() * 0.95

    def stop_make_money(self):
        # 止盈价：昨天的最高价*0.95
        return self.history_data.head(1).high.values[0]

    def drag(self):
        # 阻力价：不包括当天 有开盘的 交易日的  19日内最高价的最高值
        return tushare.get_hist_data(code=self.code).head(19).high.max()

    def tomorrow_buy_point(self):
        # 明日买点：算今天的 在收盘后 计算
        # ((开盘价+最高价+最低价)/3*2*(4-1))/(4+1)+((最高价+最低价)/2-3日前的(开盘价+最高价+最低价)/3）/4
        open = self.yesterday_open_price()
        high = self.yesterday_high_price()
        low = self.yesterday_low_price()
        before_3days_data = tushare.get_hist_data(code=self.code).head(4)[1:]
        open_before_3days = before_3days_data.iloc[[-1]].open.iat[0]
        high_before_3days = before_3days_data.iloc[[-1]].high.iat[0]
        low_before_3days = before_3days_data.iloc[[-1]].low.iat[0]
        return ((open + high + low) / 3 * 2 * (4 - 1)) / (4 + 1) + ((high + low) / 2 - (open_before_3days + high_before_3days + low_before_3days) / 3) / 4

    def yesterday_prediction_point(self):
        # 昨测今日买点：1日前的((开盘价+最高价+最低价)/3*2*(4-1))/(4+1)+((最高价+最低价)/2-3日前的(开盘价+最高价+最低价)/3）/4
        return ''


if __name__ == '__main__':
    ts = TushareStock()
    # print ts.yesterday_open_price()
    # print ts.yesterday_high_price()
    # print ts.yesterday_low_price()
    # print ts.today_buy_point()
    # print ts.stop_loss()
    # print ts.stop_make_money()
    # print ts.drag()
    print ts.tomorrow_buy_point()












