# Nov 2019, Jaseung Ku

import pyvisa

class Agilent6641A(object):
    '''Class for Agilent6331A power supply'''
    def __init__(self, GPIB_ADDR):
        '''Object Constructor.
        Inputs - GPIB Address
        example: pna = AgilentN5230A(16)
        '''
        self.GPIB_ADDR = GPIB_ADDR
        self.rm = pyvisa.ResourceManager()
        self.instr = self.rm.get_instrument('GPIB0::' + str(self.GPIB_ADDR) + '::INSTR')
        self.instr.timeout = 10000 # in milisecond. To avoid timeout error during mag cycle with logger running.
    
    def IDN(self):
        '''*IDN?
        '''
        return self.instr.query('*IDN?')
        
    def setVoltage(self, volt):
        ''' Set voltage in V
        '''
        self.instr.write('VOLT {}'.format(volt))
    
    def getSetVoltage(self):
        ''' Read set voltage in V
        '''
        return float(self.instr.query('VOLT?'))
        
    def setCurrent(self, curr):
        ''' Set current in A
        '''
        self.instr.write('CURR {}'.format(curr))
    
    def getSetCurrent(self):
        ''' Read set current in A
        '''
        return float(self.instr.query('CURR?'))
        
    def measVoltage(self):
        ''' Sense voltage in V (not nominal voltage setting)
        '''
        return float(self.instr.query('MEAS:VOLT?'))
        
    def measCurrent(self):
        ''' Sense current in A (not nominal current setting)
        '''
        return float(self.instr.query('MEAS:CURR?'))
                
    def outputOn(self):
        ''' Output on
        '''
        self.instr.write('OUTP 1')
        
    def outputOff(self):
        ''' Output off
        '''
        self.instr.write('OUTP 0 ')
    
    def getOutputStatus(self):
        ''' Read output status: 0(off) or 1(on)
        '''
        return float(self.instr.query('OUTP?'))
   
    def is_CV_mode(self):
        """
        Check if power supply is in CV mode.
        """
        if int(self.instr.query('STAT:OPER:COND?')) == 256:
            return True
        else:
            return False
        
    def is_CC_mode(self):
        """
        Check if power supply is in CC mode.
        """
        if int(self.instr.query('STAT:OPER:COND?')) == 1024:
            return True
        else:
            return False
        