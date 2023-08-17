#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2022-2023 ByQuant.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################



 
from __future__ import (absolute_import, division, print_function,unicode_literals)
import backtrader as bt
#import pandas as pd

class Backtest():

    
    def __init__(self,datasets,strategy='',out='',style='candle',**params):
        print('*** Start ByQuant Backtest Engine ***')
        if 'cash' in params:
            self.cash = params['cash']
        else:
            self.cash = 100000
            
        if 'commission' in params:
            self.commission = params['commission']
        else:
            self.commission = 0.0005
            
        self.datasets = datasets
        #self.params = params
        
        #data.index=pd.to_datetime(data['datetime'])
        #self.data = bt.feeds.PandasData(dataname=data, datetime='datetime')
        
        self.strategy = strategy
        self.style = style
        self.out = out
    
    def feedData(self,data,freq):
        if freq == '1m':
            params = dict(
                #fromdate = datetime.datetime(2011,1,4),
                #todate = datetime.datetime(2021,3,20),
                timeframe = bt.TimeFrame.Minutes, #bt.TimeFrame.Minutes,
                compression = 1,
                #dtformat=('%Y-%m-%d %H:%M:%S'),
                #tmformat=('%H:%M:%S'),
                #datetime=0,
                open=0,
                high=1,
                low=2,
                close=3,
                volume=4
            )
        else:
            params = dict(
                #fromdate = datetime.datetime(2011,1,4),
                #todate = datetime.datetime(2021,3,20),
                timeframe = bt.TimeFrame.Days, #bt.TimeFrame.Minutes,
                compression = 1,
                #dtformat=('%Y-%m-%d %H:%M:%S'),
                #tmformat=('%H:%M:%S'),
                #datetime=0,
                open=0,
                high=1,
                low=2,
                close=3,
                volume=4
            )
        data = data[['open','high','low','close','volume']]
        feed_result = bt.feeds.PandasData(dataname=data,**params)
        
        return feed_result


    def byrun(self):
        cerebro = bt.Cerebro(stdstats=True)
        cerebro.addobserver(bt.observers.BuySell)
        cerebro.addobserver(bt.observers.DrawDown)
        cerebro.addobserver(bt.observers.TimeReturn)
        
        cerebro.addstrategy(self.strategy)
        
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='_Pyfolio')
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')  # 夏普比率
        cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns')  # 用对数法计算总、平均、复合、年化收益率
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')  # 回撤
            
            
        
        cerebro.broker.setcash(self.cash)
        
        cerebro.broker.setcommission(commission=self.commission)
        if type(self.datasets) == list:
            for dataset in self.datasets:
                data = dataset['data']
                symbol = dataset['symbol']
                freq = dataset['freq']
                feed_data = self.feedData(data,freq)
                cerebro.adddata(feed_data, name = symbol)
                
                
        else :
            data = self.datasets
            symbol = 'Symbol'
            freq = '1d'
            feed_data = self.feedData(data,freq)
            cerebro.adddata(feed_data, name = symbol)
            
            
            
        results = cerebro.run()

        if 'plot' == self.out or 'a' == self.out:
            figsize = (12, 6)  # 宽度为10英寸，高度为6英寸
            
            cerebro.plot(style = self.style,figsize=figsize)
            
        elif 'plotly' == self.out or 'c' == self.out:
            # 获取策略的收益率
            import pandas as pd
            import plotly.graph_objects as go
            returns = results[0].analyzers._Returns.get_analysis()
            # 创建收益曲线图
            returns_df = pd.DataFrame.from_dict(returns, orient='index', columns=['Returns'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=returns_df.index, y=returns_df['Returns'], mode='lines', name='Returns'))

            # 设置图表布局
            fig.update_layout(title='Strategy Returns',
                              xaxis_title='Time',
                              yaxis_title='Returns')

            # 显示图表
            fig.show()
            
        elif 'pyfolio' == self.out or 'p' == self.out:
            import pyfolio as pf
            pyfoliozer = results[0].analyzers.getbyname('_Pyfolio')
            returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
            pf.create_full_tear_sheet(returns, positions, transactions)

        elif 'quantstats' == self.out or 'q' == self.out: 
            import quantstats as qs
            pyfoliozer = results[0].analyzers.getbyname('_Pyfolio')
            returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
            returns.index = returns.index.tz_convert(None)
            qs.reports.full(returns, benchmark=returns, mode='full')
            
        
            
        elif 'bokeh' == self.out or 'b' == self.out:
            from backtrader_plotting import Bokeh
            from backtrader_plotting.schemes import Tradimo,Blackly
            b = Bokeh(
                #title='symbol',
                tabs='single',  # single 和 multi
                plot=True,  # 关闭K线
                style='line',  # style='line'
                plot_mode='single',
                scheme=Tradimo(),
                # scheme=Blackly(),
                output_mode='show',  # output_mode “show”,“save”,"memory"
                #filename='filepath',
                show_headline=False
            )
            cerebro.plot(b)
            
        elif 'seaborn' == self.out or 's' == self.out:
            import seaborn as sns
            pyfoliozer = results[0].analyzers.getbyname('_Pyfolio')
            returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
            sns.lineplot(returns)
            #sns.histplot(positions)
            #sns.histplot(transactions)

        else:
            returns = results[0].analyzers._Returns.get_analysis()
            sharpe_ratio = results[0].analyzers._SharpeRatio.get_analysis()
            draw_down = results[0].analyzers._DrawDown.get_analysis()
            #print('Value: %.2f' % cerebro.broker.getvalue())
            print('Returns:%s' % returns)
            print('Sharpe Ratio: %s' % sharpe_ratio)
            print('Draw Down: %s' % draw_down)

