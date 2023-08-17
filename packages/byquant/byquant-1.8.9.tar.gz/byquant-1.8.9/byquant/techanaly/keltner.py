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

import talib
import pandas as pd
import backtrader as bt

class byKeltner(bt.Indicator):
    lines = ('top','mid','bot',)
    #plotinfo = dict(subplot=True, plotlinelabels=True)
    params = (
        ('period', 14),
        ('deviation', 1.6)
    )
    def __init__(self):
        self.addminperiod(2)
        self.sma = bt.indicators.SMA(self.data,period=self.p.period)
        self.atr = bt.indicators.ATR(self.data,period=self.p.period)


    def next(self):
        self.lines.top[0] = self.sma[0] + self.p.deviation * self.atr[0]
        self.lines.mid[0] = self.sma[0]
        self.lines.bot[0] = self.sma[0] - self.p.deviation * self.atr[0]
        
def Keltner(data,period=14,deviation=1.6):
    if isinstance(data, pd.DataFrame):
        return None
    elif isinstance(data, pd.Series):
        return None
    elif 'backtrader.' in str(type(data)):
        return byKeltner(data,period=period,deviation=deviation)
    else:
        return None



keltner = Keltner


