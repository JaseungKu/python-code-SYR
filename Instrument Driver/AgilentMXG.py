# Aug 2016, Jaseung Ku
# Original script by Caleb
# Modified for my taste.

import visa
import numpy as np
import matplotlib.pyplot as plt

class AgilentMXG:
    '''Class for Agilent N5230 Network Analyzer'''
    def __init__(self, GPIB_ADDR):
        '''Object Constructor.
        Inputs - GPIB Address
        example: pna = AgilentN5230A(16)
        '''
        self.GPIB_ADDR = GPIB_ADDR
        self.measurements = []
        self.rm = visa.ResourceManager()
        self.instr = self.rm.get_instrument('GPIB0::' + str(self.GPIB_ADDR) + '::INSTR')
    
    def IDN(self):
        '''*IDN?
        '''
        return self.instr.ask('*IDN?')
        
    def setFreq(self, freq):
        ''' Freq in Hz
        '''
        self.instr.write(":freq:fixed {};".format(freq))
        
    def pwrOn(self):
        '''Power On
        '''
        self.instr.write(':output 1;')
    
    def pwrOff(self):
        '''Power Off'''
        self.instr.write(":output 0;")
        
    def setPwr(self, power):
        '''Power for measurement in dbm
        '''
        self.instr.write(":power {}dbm".format(power))
    