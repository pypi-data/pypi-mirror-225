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
from ..bystrategy import Strategy as byStrategy
from .. import techanaly as byta

class MACDStrategy(byStrategy):
    params = (
        ('fastperiod', 12),
        ('slowperiod', 26),
        ('signalperiod', 9)
    )
    def __init__(self):
        self.macd = byta.MACD(
            self.datas[0],
            fastperiod=self.p.fastperiod,
            slowperiod=self.p.slowperiod,
            signalperiod=self.p.signalperiod,
        )
        
        
    def next(self):
        try:
            
            if self.macd.macd[0] > self.macd.signal[0] and self.macd.macd[-1] < self.macd.signal[-1]:  # MACD线上穿信号线
                self.order = self.buy()
            if self.macd.macd[0] < self.macd.signal[0] and self.macd.macd[-1] > self.macd.signal[-1]:  # MACD线下穿信号线
                self.order = self.sell()
                
        except Exception as e:
            print(e.args)
            pass
        