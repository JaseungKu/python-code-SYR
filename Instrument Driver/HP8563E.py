# Aug 2016, Jaseung Ku
# Original script by Caleb
# Modified for my taste.

import visa
import numpy as np
import matplotlib.pyplot as plt

class HP8563E:
    '''Class for HP 8563E Spectrum Analyzer'''
    def __init__(self, GPIB_ADDR):
        '''Object Constructor.
        Inputs - GPIB Address
        example: pna = AgilentN5230A(16)
        '''
        self.GPIB_ADDR = GPIB_ADDR
        self.measurements = []
        self.rm = visa.ResourceManager()
        self.instr = self.rm.get_instrument('GPIB0::' + str(GPIB_ADDR) + '::INSTR')
        self.instr.write('FORM REAL,64')
            
    def IDN(self):
        '''*IDN?
        '''
        return self.instr.ask('*IDN?')
     
    def setFreqStart(self, Freq):
        ''' Set start and end frequency '''
        self.instr.write("FA {} Hz;".format(Freq))
            
    def setFreqEnd(self, Freq):
        ''' Set start and end frequency '''
        self.instr.write("FB {} Hz".format(Freq))
                
    def getData(self, channel):
        '''Retrieve Measurement data. 
        returns numpy array
        '''
        if channel =='A':
            return self.instr.ask("TRA?;")
        elif channel =='B':
            return self.instr.ask("TRB?;")
    
    def clear(self):
        ''' clear buffer '''
        self.instr.write("CLEAR")
    