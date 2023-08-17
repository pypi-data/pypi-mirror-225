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
        
 #       
        
def EMV(data,low=pd.Series(dtype=float),volume=pd.Series(dtype=float)):
    if isinstance(data, pd.DataFrame):
        return False
    elif isinstance(data, pd.Series):
        return False
    elif 'backtrader.' in str(type(data)):
        return byEMV(data)
    else:
        return None



emv = EMV
#AROON_NP = AROON


