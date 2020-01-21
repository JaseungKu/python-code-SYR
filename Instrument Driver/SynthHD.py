#Oct 2017, Yebin Liu
import visa
import numpy as py

class SynthHD:
    def __init__(self, USB_ADDR):
        self.USB_ADDR = USB_ADDR
        self.measurements = []
        self.rm = visa.ResourceManager()
        self.instr = self.rm.get_instrument('ASRL' + str(self.USB_ADDR) +'::INSTR')

    def setChannel(self,channel = 0):
        #Cx where x=0=channel0=RFoutA and where x=1=channel1=RFoutB
        #C? queries which channel is currently under control
        self.instr.write('C'+str(channel))

    def setFreq(self, freq):
        '''
        fxxxxx.xxxxxxx sets frequency to x MHz in 0.1Hz resolution
        f? queries frequency setting for current channel in 0.1Hz resolution
        '''
        self.instr.write('f' + str(freq/1e6))

    def setPwr(self, pwr):
        '''
        Wxx.xxx sets RF power to x dBm in 0.001dB resolution
        W? queries the RF output power setting for current channel in 0.001dB resolution
        '''
        self.instr.write('W' + str(pwr))

    def calibrate(self):
        '''
        V queries if there was successful calibration. 1=success, 0=failure
        '''
        cal = self.instr.ask('V')
        if cal == 1:
            return 'Calibration success'
        elif cal == 0:
            return 'Calibration fail'

    def tempCompe(self,mode=3):
        '''
        Zx sets the method for temperature compensation (x=0=none, 1=on set, 2=1sec, 3=10sec).
        Z? queries the setting for Temperature Compensation
        '''
        self.instr.write('Z'+str(mode))

    def pwrOn(self):
        self.instr.write('E1')

    def pwrOff(self):
        self.instr.write('E0')

    def setRef(self,mode=0):
        '''
        xy sets the reference where y=0=external, y=1=internal 27MHz, y=2=internal 10MHz
        x? queries the setting
        '''
        self.instr.write('x'+str(mode))
