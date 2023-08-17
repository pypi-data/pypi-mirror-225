import backtrader as bt
import pandas as pd
#from backtrader.comminfo import ComminfoFuturesPercent, ComminfoFuturesFixed  # 期货交易的手续费用，按照比例或者按照金额
from backtrader.comminfo import CommInfoBase


#期货百分比佣金收取方式
class ComminfoFuturesPercent(CommInfoBase):
    '''write by myself,using in the future backtest,it means we should give a percent comminfo to broker'''
    params = (
        ('stocklike', False),
        ('commtype', CommInfoBase.COMM_PERC),
        ('percabs', True)
    )

    def _getcommission(self, size, price, pseudoexec):
        return abs(size) * price * self.p.mult * self.p.commission

    def get_margin(self, price):
        return price * self.p.mult * self.p.margin

# comm_rb = CommInfoFutures(commission=1e-4, margin=0.09, mult=10.0)
# cerebro = bt.Cerebro()
# cerebro.broker.addcommissioninfo(comm_rb, name='RB')
#期货固定佣金收取方式
class ComminfoFuturesFixed(CommInfoBase):
    '''write by myself,using in the future backtest,it means we should give a fixed comminfo evey lot to broker'''
    params = (
        ('stocklike', False),
        ('commtype', CommInfoBase.COMM_FIXED),
        ('percabs', True)
        )
    def _getcommission(self, size, price, pseudoexec):
        return abs(size) *  self.p.commission

    def get_margin(self, price):
        return price * self.p.mult * self.p.margin

#股票百分比佣金收取方式
class CommInfo_Stocks_PercAbs(CommInfoBase):
    params = (
        ('stocklike', True),
        ('commtype', CommInfoBase.COMM_PERC),
        ('percabs', True),
    )
#comm = CommInfo_Stocks_PercAbs(commission=0.001)
#cerebro = bt.Cerebro()
#cerebro.broker.addcommissioninfo(comm, name='xxx')
# commission=0.001 代表按照成交金额的千分之一收取佣金

# 超过5000手，佣金打折50% 。需要核对这个用法有没有效果，我自己没有用过。
#超过一定的手数之后佣金打折的方法
class CommInfo_Fut_Discount(bt.CommInfoBase):
    params = (
      ('stocklike', False),  # Futures
      ('commtype', bt.CommInfoBase.COMM_FIXED),  # Apply Commission

      # Custom params for the discount
      ('discount_volume', 5000),  # minimum contracts to achieve discount
      ('discount_perc', 50.0),  # 50.0% discount
    )

    negotiated_volume = 0  # attribute to keep track of the actual volume

    def _getcommission(self, size, price, pseudoexec):
        if self.negotiated_volume > self.p.discount_volume:
           actual_discount = self.p.discount_perc / 100.0
        else:
           actual_discount = 0.0

        commission = self.p.commission * (1.0 - actual_discount)
        commvalue = size * price * commission

        if not pseudoexec:
           # keep track of actual real executed size for future discounts
           self.negotiated_volume += size

        return commvalue


def load_hist_ticks(histfile):
    # 读取回填用的历史tick数据，文件格式见样本文件。
    # 用户可修改从数据库读取到df
    df = pd.read_csv(histfile,parse_dates=[0])
    return df

def load_hist_bars(histfile):
    # 读取回填用的历史1分钟bar数据（即1分钟k线数据），文件格式见样本文件。
    # 用户可修改从数据库读取到df
    df = pd.read_csv(histfile, parse_dates=[0])
    return df


