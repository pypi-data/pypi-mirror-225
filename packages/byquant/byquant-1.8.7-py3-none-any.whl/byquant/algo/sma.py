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

class SMAStrategy(byStrategy):
    params = (
        ('sma_period', 20),  # 移动均线周期
    )
    def __init__(self):
        #self.sma = by.indicators.SMA(self.data.close, period=self.p.sma_period)
        self.sma = byta.sma(self.data, period=self.p.sma_period)

    def next(self):
        #self.log(f"short_ma:{self.short_ma[0]}")
        if self.data.close[0] > self.sma[0] and self.data.close[-1] < self.sma[-1]:
            # 执行买入操作
            self.buy()
        elif self.data.close[0] < self.sma[0] and self.data.close[-1] > self.sma[-1]:
            # 执行卖出操作
            self.sell()
            