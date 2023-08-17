import backtrader as bt

def isCross(line1,line2):
    if line1[0] > line2[0] and line1[-1] < line2[-1]:
        return True
    else:
        return False
        
def crossUp(line1,line2):
    return line1[0] > line2[0] and line1[-1] < line2[-1]

def crossDown(line1,line2):
    return line1[0] < line2[0] and line1[-1] > line2[-1]
    
        
def num2date(datetime):
    return bt.num2date(datetime)