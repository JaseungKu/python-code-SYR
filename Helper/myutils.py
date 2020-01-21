# Jaseung Ku, Aug 2016
# Utility classes and functions

import math
import visa
                      
class Sweeper1D(object):
    """
    description: Calcuate next point during 1D sweep. 
    attributes: start, end, step, loop, curr_val, curr_sweepNum
    method: __init__, update, stop
    """
    def __init__(self, start, end, step, sweepNum):
        self.start = start
        self.end = end
        if self.start < self.end:
            self.step = math.fabs(step)
        else:
            self.step = math.fabs(step) * (-1)
        self.curr_val = start
        self.sweepNum = sweepNum
        self.curr_sweep = 1
            
    def update(self): # update next value and set value
        if self.inrange(self.curr_val+self.step, self.start, self.end):
            self.curr_val = self.curr_val + self.step
        else:
            self.step = self.step * (-1)
            self.curr_val = self.curr_val + self.step # turn around
            self.curr_sweep += 1
    
    def inrange(self, var, start, end):
        if (var >= start and end >= var) or (var>=end and start>=var):
            return True
        else:
            return False
        
    def stop(self):
        if self.curr_sweep > self.sweepNum:
            return True
        else:
            return False 
###### usage        
# spec = Sweeper1D(starFreq, endFreq, stepFreq, num)
# specdev.setfreq(spec.curr_val)


#def ramp(start, end, method)
#    """
#    description: ramp up or down from start to end
#    """
#    pass

