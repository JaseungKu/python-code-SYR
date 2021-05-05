# Apr 2021
# Jaseung Ku

import pyvisa

class Agilent33250A:
    def __init__(self, GPIB_ADDR):
        '''Object Constructor.
        Inputs - GPIB Address
        '''
        self.GPIB_ADDR = GPIB_ADDR     
        self.rm = pyvisa.ResourceManager()
        self.instr = self.rm.get_instrument('GPIB0::' + str(self.GPIB_ADDR) + '::INSTR')

    def set_offset(self, offset):
        ''' Set offset voltage in V'''
        self.instr.write(f'Voltage:offset {offset}')
       
    def set_amplitude(self, amp):
        ''' Set amplitude voltage in V'''
        self.instr.write(f'Voltage {amp}')
    
    def set_frequency(self, freq):
        ''' Set frequency in Hz'''
        self.instr.write(f'Frequency {freq}')
     
    def output_on(self):
        ''' Turn on output'''
        self.instr.write(f'Output ON')
    
    def output_off(self):
        ''' Turn off output'''
        self.instr.write(f'Output OFF')