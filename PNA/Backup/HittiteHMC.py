# Aug 2016, Jaseung Ku
# Original script by Caleb
# Modified for my taste.

import visa
import numpy as np

class HittiteHMC:
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
        self.instr.write("freq:cw {};".format(freq))

    def readFreq(self):
        return self.instr.ask('freq?;') 
        
    def pwrOn(self):
        '''Power On
        '''
        self.instr.write('output 1;')
    
    def pwrOff(self):
        '''Power Off'''
        self.instr.write("output 0;")
        
    def setPwr(self, power):
        '''Power for measurement in dbm
        '''
        self.instr.write("POWer:LEVel:IMMediate {}dbm".format(power))

        # function val = get.frequency(obj)
        #     val = str2double(obj.query('freq?;'))*1e-9; % convert to GHz
        # end
        # function val = get.power(obj)
        #     val = str2double(obj.query('power?'));
        # end
        # function val = get.output(obj)
        #     val = obj.query('output?');
        # end
        
        # % property setters
        # function obj = set.frequency(obj, value)
        #     assert(isnumeric(value), 'Requires numeric input');
        #     obj.write(sprintf('freq:cw %20.10fGHz', value));
        #     %Wait for frequency to settle
        #     pause(0.005);
        # end
        # function obj = set.power(obj, value)
        #     assert(isnumeric(value), 'Requires numeric input');
        #     obj.write(sprintf('POWer:LEVel:IMMediate %ddbm', value));
        # end
        # function obj = set.output(obj, value)
        #     obj.write(['output ' obj.cast_boolean(value)]);
        # end