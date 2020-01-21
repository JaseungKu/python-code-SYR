
import visa

class Agilent33250A:
    def __init__(self, GPIB_ADDR, channel=1):
        '''Object Constructor.
        Inputs - GPIB Address
        '''
        self.GPIB_ADDR = GPIB_ADDR
        self.channel = channel
        self.rm = visa.ResourceManager()
        self.instr = self.rm.get_instrument('GPIB0::' + str(self.GPIB_ADDR) + '::INSTR')

    def setVoltage(self,volt):
        '''Applies DC voltage. Also turns output on.'''
        self.instr.write("APPL:DC DEF, DEF, {} V".format(volt))
