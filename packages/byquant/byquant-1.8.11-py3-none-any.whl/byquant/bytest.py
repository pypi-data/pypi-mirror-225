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
from . import algo as byalgo
from . import data as bydata
from .bybacktest import *
from .bystrategy import Strategy as byStrategy

class Test():
    def __init__(self,symbol,strategy='sma',freq='1d',out='a',**params):
        if 'start' in params:
            self.start = params['start']
        else:
            self.start = ''
            
        if 'end' in params:
            self.end = params['end']
        else:
            self.end = ''
            
        data = bydata.quote(symbol=symbol,freq=freq,start=self.start, end=self.end,cachetime=0)
        if strategy == 'sma':
            Backtest(data,strategy=byalgo.SMAStrategy,out=out).byrun()
        elif strategy == 'macd':
            Backtest(data,strategy=byalgo.MACDStrategy,out=out).byrun()
        else:
            Backtest(data,strategy=byalgo.SMAStrategy,out=out).byrun()
            
            