# Lakeshore331.py

import visa

class Lakeshore331(object):	
    def __init__(self, GPIB_ADDR):
        self.GPIB_ADDR = GPIB_ADDR
        self.rm = visa.ResourceManager()
        self.instr = self.rm.get_instrument('GPIB0::' + str(self.GPIB_ADDR) + '::INSTR')

    def IDN(self):
        return self.instr.query('*IDN?')

    def tempGet(self,channel):
        control = 2
        if control == 0:
            channel = 'A'
        if control == 1:
            channel = 'B'
        return self.instr.query('KRDG? '+channel)

    def getTemperature(self, channel):
        """
        Read temperature in Kevin
        channel: 'A' or 'B'
        """        
        return float(self.instr.query('KRDG? '+ channel))
