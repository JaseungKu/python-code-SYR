# Nov 2019
# Jaseung Ku

import visa

class Lakeshore340(object):
    def __init__(self, GPIB_ADDR):
        self.GPIB_ADDR = GPIB_ADDR
        self.rm = visa.ResourceManager()
        self.instr = self.rm.get_instrument('GPIB0::' + str(self.GPIB_ADDR) + '::INSTR')

    def IDN(self):
        return self.instr.query('*IDN?')

    def getTemperature(self, channel):
        """
        Read temperature in Kevin
        channel: A or B
        """        
        return float(self.instr.query('KRDG? '+ channel))
        
    def getInductiveVolt(self, channel):
        """
        Read inductive voltage.        
        """        
        return float(self.instr.query('SRDG? '+ channel))    
