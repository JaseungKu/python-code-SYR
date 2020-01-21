# Jaseung Ku
# Nov 2019

import visa

class Lakeshore218:	
    def __init__(self, GPIB_ADDR):
        self.GPIB_ADDR = GPIB_ADDR		
        self.rm = visa.ResourceManager()
        self.instr = self.rm.get_instrument('GPIB0::' + str(self.GPIB_ADDR) + '::INSTR')

    def IDN(self):
        return self.instr.query('*IDN?')

    def getTemperature(self, channel):
        """
        Read temperature in Kevin
        channel: channel number in string
        """

        return float(self.instr.query('KRDG? '+ channel))
            
    def getInductiveVolt(self, channel):
        """
        Read inductive voltage.  
        channel: channel number in string
        return : inductive voltage in float
        """        
        return float(self.instr.query('SRDG? '+ channel))
        