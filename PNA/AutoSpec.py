# Modified by Jaseung Ku, Aug 2016
# Original script by Caleb

import visa
from time import sleep

class SIM:
    def __init__(self, GPIB_ADDR, channel=1):
        '''Object Constructor.
        Inputs - GPIB Address
        example: sim = SIM928(16)
        Connect to SIM
        '''
        self.GPIB_ADDR = GPIB_ADDR
        self.channel = channel
        self.rm = visa.ResourceManager()
        self.instr = self.rm.get_instrument('GPIB0::' + str(self.GPIB_ADDR) + '::INSTR')

    def IDN(self):
        '''*IDN?
        '''
        return self.instr.ask("*IDN?")

    def Define_Res()
        