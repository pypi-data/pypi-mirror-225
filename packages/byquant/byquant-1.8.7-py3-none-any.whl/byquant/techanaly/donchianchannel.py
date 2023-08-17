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
import numpy as np

class byEMV(bt.Indicator):
    lines = ('emv',)

    def __init__(self):
        self.addminperiod(2)

    def next(self):
        self.lines.emv[0] = ((self.data.high + self.data.low) / 2 - (self.data.high[-1] + self.data.low[-1]) / 2) * (self.data.high - self.data.low) / self.data.volume
        
class byDonchianChannel(bt.Indicator):
    lines = ('top', 'mid', 'bot')
    params = (('period', 20),)

    def __init__(self):
        self.addminperiod(self.params.period)

    def next(self):
        highest = max(self.data.high.get(-self.p.period, 0))
        lowest = min(self.data.low.get(-self.p.period, 0))
        self.lines.top[0] = highest
        self.lines.bot[0] = lowest
        self.lines.mid[0] = (highest + lowest) / 2
        
def DonchianChannel(data,low=pd.Series(dtype=float),period=14):
    if isinstance(data, pd.DataFrame):
        top = talib.MAX(data.high, timeperiod=period)
        bot = talib.MIN(data.low, timeperiod=period)
        mid = (top + bot) / 2
        return top,mid,bot
    elif isinstance(data, pd.Series):
        top = talib.MAX(data, timeperiod=period)
        bot = talib.MIN(low, timeperiod=period)
        mid = (top + bot) / 2
        return top,mid,bot
    elif 'backtrader.' in str(type(data)):
        return byDonchianChannel(data,period=period)
    else:
        return None



donchianchannel = DonchianChannel
donchian = DonchianChannel
Donchian = DonchianChannel
#AROON_NP = AROON


