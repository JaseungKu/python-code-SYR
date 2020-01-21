import visa

class LSCI332S:	
	def __init__(self, GPIB_ADDR):
		self.GPIB_ADDR = GPIB_ADDR
		self.measurements = []
		self.rm = visa.ResourceManager()
		self.instr = self.rm.get_instrument('GPIB0::' + str(self.GPIB_ADDR) + '::INSTR')
		
	def IDN(self):
		return self.instr.ask('*IDN?')
		
	def tempGet(self,channel):
		control = 2
		if control == 0:
			channel = 'A'
		if control == 1:
			channel = 'B'
		return self.instr.ask('KRDG? '+channel)
			