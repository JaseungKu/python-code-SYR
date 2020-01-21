# Mar 2017, Jaseung Ku

import visa
import numpy as np
import matplotlib.pyplot as plt

class AFG3252:
    '''Class for Tektronix AFG3252'''
#    def __init__(self, GPIB_ADDR):
#        '''Object Constructor.
#        Inputs - GPIB Address
#        example: pna = AgilentN5230A(16)
#        '''
#        self.GPIB_ADDR = GPIB_ADDR
#        self.measurements = []
#        self.rm = visa.ResourceManager()
#        self.instr = self.rm.get_instrument('GPIB0::' + str(self.GPIB_ADDR) + '::INSTR')
    
    def __init__(self, ADDR):
        '''Object Constructor.
        Inputs - Address. Copy and paste address from the output of visa.ResourceManager().list_resources()
        example: pna = AgilentN5230A('ASRL1::INSTR')
        '''
        self.ADDR = ADDR
        self.measurements = []
        self.rm = visa.ResourceManager()
        self.instr = self.rm.get_instrument(ADDR)

    def IDN(self):
        '''*IDN?
        '''
        return self.instr.ask('*IDN?')
             
    def setPulsePeriod(self, channel, period):
        '''Set the period of pulse. The unit of period is us here
        '''
        self.instr.write('SOURce{}:PULSe:PERiod {}us'.format(channel, period))
        
    def setClkRef(self, source):
        '''Set the clock REF either internal or external.
            source :  INT, EXT
        '''
        if source=='INT':
            self.instr.write('SOURce:ROSCillator:SOURce INTernal') 
        elif source=='EXT':
            self.instr.write('SOURce:ROSCillator:SOURce EXTernal') 
        else:
            print('Argument Error! Proper argument is either INT or EXT')
      
    def setPulseWidth(self, channel, width):
        '''Set the width of pulse. The unit of period is us here
        '''
        self.instr.write('SOURce{}:PULSe:WIDTh {}us'.format(channel, width))
    
    def setPulseDealy(self,channel, delay):
        '''Set the width of delay. The unit of period is us here
        '''
        self.instr.write('SOURce{}:PULSe:DELay {}us'.format(channel, delay))
    
    def setAmpHighLow(self, channel, high, low):
        '''Set the high and low voltage level. The unit of period is V.
        '''
        self.instr.write('SOURce{}:VOLTage:LEVel:IMMediate:HIGH {}V'.format(channel, high))
        self.instr.write('SOURce{}:VOLTage:LEVel:IMMediate:LOW {}V'.format(channel, low))
       
    def setFreqConCurrent(self, channel, width):
        '''Set the frequency concurrent. The unit of period is V.
        '''
        self.instr.write('SOURce{}:VOLTage:LEVel:IMMediate:HIGH {}V'.format(channel, high)) 