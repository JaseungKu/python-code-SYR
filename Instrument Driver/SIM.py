# Modified by Jaseung Ku, Aug 2016
# Original script by Caleb

import visa
from time import sleep

class SIM:
    def __init__(self, GPIB_ADDR, channel=1):
        '''Object Constructor.
        Inputs - GPIB Address or com
        example: sim = SIM928(16), sim = SIM928('COM7')
        Connect to SIM
        '''
        self.GPIB_ADDR = GPIB_ADDR
        self.channel = channel
        self.rm = visa.ResourceManager()
        if type(GPIB_ADDR) == str:
        	self.instr = self.rm.get_instrument('ASRL' + GPIB_ADDR[3:] + '::INSTR')
        else:
	        self.instr = self.rm.get_instrument('GPIB0::' + str(self.GPIB_ADDR) + '::INSTR')

    def IDN(self):
        '''*IDN?
        '''
        return self.instr.ask("*IDN?")

    def setVoltage(self, value):
        '''Set the voltage of a module on a defined channel.
        '''
        self.instr.write('SNDT {}, "VOLT {}"'.format(self.channel, round(value, 3))) # round doesn't help

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
        return float(self.instr.read()[5:])
        # return self.instr.read()

    def askVoltage(self):
        '''Query set voltage.
        '''
        self.instr.write('SNDT {}, "VOLT?"'.format(self.channel))
        sleep(0.05)
        self.instr.write('GETN? {}, 12'.format(self.channel))
        return float(self.instr.read()[5:])

    def readVoltage(self,sim970channel, port):
        #self.instr.write('CONN '+str(sim970channel)+',"SIM900"')
        self.instr.write('FLOQ')
        self.instr.write('*RST')
        self.instr.write('CONN {}, "SIM900"'.format(sim970channel))
        self.instr.write('SIM900')
        self.instr.write('CONN {}, "SIM900"'.format(sim970channel))
        self.instr.write('*RST')
        self.instr.write('TMOD 2')
        self.instr.write('*TRG')
        volt_out1 = self.instr.ask('VOLT? {}'.format(port))
        print(volt_out1)
        # volt_out1 gives wrong number and vol_out2 gives right number. It is
        volt_out2 = self.instr.ask('VOLT? {}'.format(port))
        print(volt_out2)
        volt_out3 = self.instr.ask('VOLT? {}'.format(port))
        print(volt_out3)
        self.instr.write('SIM900')
        return float(volt_out1),float(volt_out2),float(volt_out3)
