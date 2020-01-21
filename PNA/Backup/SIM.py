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
    
    def setVoltage(self, value):
        '''Set the voltage of a module on a defined channel.
        '''
        self.instr.write('SNDT {}, "VOLT {}"'.format(self.channel, value))
        
    def setOutput(self, value):
        '''Set the output of a module on a defined chanenl.
        '''
        if value:
            self.instr.write('SNDT {}, "OPON"'.format(self.channel))
        else:
            self.instr.write('SNDT {}, "OPOF"'.format(self.channel))

    def getVoltage(self, port):
        '''Measure voltage of port on a defined channel.
        '''
        self.instr.write('SNDT {}, "VOLT? {}"'.format(self.channel, port))
        sleep(0.05)
        self.instr.write('GETN? {}, 12'.format(self.channel))
        return float(self.instr.read()[6:])