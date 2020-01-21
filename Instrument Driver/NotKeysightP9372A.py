
import visa
import numpy as np
import matplotlib.pyplot as plt

class KeysightP9372A:
    '''Class for Keysight P9372A Network Analyzer'''
    def __init__(self, USB_ADDR):
        '''Object Constructor.
        Inputs - USB Address
        example: pna = Keysight9372A(10)
        '''
        self.USB_ADDR = USB_ADDR
        self.measurements = []
        self.rm = visa.ResourceManager()
        # self.instr = self.rm.get_instrument('ASRL' + str(USB_ADDR) + '::INSTR')
        self.instr = self.rm.get_instrument('PXI10::0-0.0::INSTR')
        # self.instr.write('FORM REAL,64')

    # def IDN(self):
    #     '''*IDN?
    #     '''
    #     return self.instr.ask('*IDN?')

    # def dataFormat(self,mode='MLINear'):
    #     '''Setup Data format
    #         mode - MLINear, MLOGarithmic, PHASe, UPHase, IMAGinary, REAL, POLar'''
    #     if mode in ['MLINear','MLOGarithmic','phase','uphase','IMAGinary','REAL','POLar']:
    #         a = "calculate2:format {}".format(mode)
    #         print(a)
    #         self.instr.write("calculate2:format {}".format(mode))
    #     else:
    #         print("Format should be MLINear, MLOGarithmic, phase, uphase, IMAGinary, REAL, POLar")

    def setupMeas(self, meas='S21', name="S21Meas"):
        '''Creates Measurement
            meas - S11, S12, S21, or S22
            name - A name to keep track of the measurement'''
        if meas in ['S11', 'S12', 'S21', 'S22']:
            self.instr.write("CALC1:PAR:MOD {}".format(meas))
            # self.instr.write("DISPlay:WINDow1:TRACe1:FEED '{}'".format(name))
            self.measurements.append(name)
            print("Initialized {} Measurement '{}'".format(meas, name))
            return name
        else:
            print("Measurement must be S11, S12, S21, or S22")

    def setSweepType(self, mode='linear'):
        '''Set sweep mode : linear sweep, log sweep, CW sweep, etc
           mode : LINear | LOGarithmic | POWer | CW | SEGMent | PHASe'''
        self.instr.write("SENS1:SWE:TYPE {}".format(mode))

    # def setCWFreq(self, freq):
    #     ''' Set CW fixed frequency '''
    #     self.instr.write("SENSe1:FREQuency {}".format(freq))
    #
    def setFreqStartEnd(self, startFreq, endFreq):
        ''' Set start and end frequency '''
        self.instr.write("SOUR1:POW:STAR {}".format(startFreq))
        self.instr.write("SOUR1:POW:STOP {}".format(endFreq))

    def setFreqCenterSpan(self, centerFreq, spanFreq):
        ''' Set start and end frequency '''
        self.instr.write("SOUR1:POW:CENT {}".format(centerFreq))
        self.instr.write("SOUR1:POW:SPAN {}".format(spanFreq))

    def setStartFreq(self, freq):
        ''' Start Freq in Hz
        '''
        self.instr.write("SOUR1:POW:STAR {}".format(freq))

    def setStopFreq(self, freq):
        ''' Stop Freq in Hz
        '''
        self.instr.write("SOUR1:POW:STOP {}".format(freq))

    def selfCenterFreq(self, freq):
        ''' Center Freq in Hz
        '''
        self.instr.write("SOUR1:POW:CENT {}".format(freq))

    def setSpanFreq(self,freq):
        ''' span in Hz
        '''
        self.instr.write("SOUR1:POW:SPAN {}".format(freq))

    def pwrOn(self):
        '''Power On
        '''
        self.instr.write("OUTP 1")

    def pwrOff(self):
        '''Power Off'''
        self.instr.write("OUTP 0")

    def setPwr(self, power):
        '''Power for measurement
        '''
        self.instr.write("SOUR:POW1:LEV {}".format(power))

    def numPoints(self, points):
        '''Number of points in measurement.
        '''
        self.instr.write("SENS1:SWE:POIN {}".format(points))

    def avgClear(self):
        ''' Clears and restarts averaging of the measurement data. Does NOT apply to point averaging.
        '''
        self.instr.write("SENS1:AVER:CLE")

    def avgCount(self, count):
        '''Sets the number of measurements to combine for an average. Must also set SENS:AVER[:STATe] ON
        '''
        if count < 65536 and count >= 1:
            self.instr.write("SENS1:AVER:STAT 1")
            self.instr.write("SENS1:AVER:COUN {}".format(count))
        else:
            self.instr.write("SENS1:AVER:STAT 0")

    def avgDone(self):
        '''Return true if averaging is complete, false if not.
        '''
        return bool(float(self.instr.ask('*ESR?')) or 0)
    #
    # def sweepDone(self):
    #     return bool(self.instr.ask('STAT:OPER:DEV:COND?'))

    def getData(self, cplx=False):
        '''Retrieve Measurement data
        returns numpy array
        '''
        while self.avgDone() is False:
            pass

        self.instr.write("FORMat ASCII")

        if cplx:
            ans = self.instr.ask("Calculate:Data? SDATA")
            real = []
            imag = []
            y = []
            ya = [float(f) for f in ans.split(',')]

            for i, yi in enumerate(ya):
                if i % 2 == 0:
                    real.append(yi)
                else:
                    imag.append(yi)
                    y.append(real[-1] + 1j*imag[-1])
            x = np.linspace(float(self.instr.ask("SOUR1:POW:STAR?")), float(self.instr.ask("SOUR1:POW:STOP?")), len(y))
            return x, np.asarray(y, dtype=np.dtype(np.complex128))
        else:
            ans = self.instr.ask("CALCulate1:DATA? FDATA")
            y = [float(f) for f in ans.split(',')]
            x = np.linspace(float(self.instr.ask("SENSe1:FREQuency:START?")), float(self.instr.ask("SENSe1:FREQuency:STOP?")), len(y))
            return x, np.asarray(y)

    #
    # def plot(self):
    #     '''Simple Matplotlib Plot of Measurement'''
    #     if not self.measurements:
    #         self.setupMeas()
    #
    #     x, y=self.getData()
    #     plt.plot(x, y)
    #
    # def analyze(self):
    #     '''Resonator Analysis'''
    #     y = self.getData()
    #     x = np.linspace(float(self.instr.ask("SENSe1:FREQuency:START?")), float(self.instr.ask("SENSe1:FREQuency:STOP?")), len(y))
    #     analyze('Analysis', x=x, y=y)

    def setIF(self, freq):
        '''Set IF Bandwidth in Hz'''
        self.instr.write("SENS1:BAND {}".format(freq))
