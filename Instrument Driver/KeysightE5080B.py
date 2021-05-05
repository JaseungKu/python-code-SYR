# Feb 2021 Jaseung Ku

import visa
import numpy as np
import matplotlib.pyplot as plt

class KeysightE5080B:
    '''Class for KeysightE5080B Network Analyzer'''
    def __init__(self, resource_name):
        '''Object Constructor.
       
        '''
        
        self.measurements = []
        self.rm = visa.ResourceManager()
        self.instr = self.rm.open_resource(resource_name)
       
        self.instr.write('SYST:PREset')
        
                    
    def IDN(self):
        '''*IDN?
        '''
        return self.instr.query('*IDN?')

    def dataFormat(self,mode='MLINear'):
        '''Setup Data format
            mode - MLINear, MLOGarithmic, PHASe, UPHase, IMAGinary, REAL, POLar'''
        if mode in ['MLINear','MLOGarithmic','phase','uphase','IMAGinary','REAL','POLar']:
            a = "calculate2:format {}".format(mode)
            print(a)
            self.instr.write("calculate2:format {}".format(mode))
        else:
            print("Format should be MLINear, MLOGarithmic, phase, uphase, IMAGinary, REAL, POLar")

#     def setupMeas(self, meas='S21', name="S21Meas"):
    def setupMeas(self, meas='S21'):
#         '''Creates Measurement
#             meas - S11, S12, S21, or S22
#             name - A name to keep track of the measurement'''
#         if meas in ['S11', 'S12', 'S21', 'S22']:
#             self.instr.write("CALCulate:PARameter:DEFine:EXT '{}',{}".format(name, meas))
#             self.instr.write("DISPlay:WINDow1:TRACe1:FEED '{}'".format(name))
#             self.measurements.append(name)
#             print("Initialized {} Measurement '{}'".format(meas, name))
#             return name
#         else:
#             print("Measurement must be S11, S12, S21, or S22")
         self.instr.write(f'CALCulate:MEASure1:PARameter {meas}')

    def setSweepType(self, mode):
        '''Set sweep mode : linear sweep, log sweep, CW sweep, etc 
           mode : LINear | LOGarithmic | POWer | CW | SEGMent | PHASe'''
        self.instr.write("SENSe1:SWEep:TYPE {}".format(mode))
        
    def setCWFreq(self, freq):
        ''' Set CW fixed frequency '''
        self.instr.write("SENSe1:FREQuency {}".format(freq))
        
    def setFreqStartEnd(self, startFreq, endFreq):
        ''' Set start and end frequency '''
        self.instr.write("SENSe1:FREQuency:STARt {}".format(startFreq))
        self.instr.write("SENSe1:FREQuency:STOP {}".format(endFreq))
    
    def setFreqCenterSpan(self, centerFreq, spanFreq):
        ''' Set start and end frequency '''
        self.instr.write("SENSe1:FREQuency:CENTer {}".format(centerFreq))
        self.instr.write("SENSe1:FREQuency:SPAN {}".format(spanFreq))
        
    def setStartFreq(self, freq):
        ''' Start Freq in Hz
        '''
        self.instr.write("SENSe1:FREQuency:STARt {}".format(freq))
        
    def setStopFreq(self, freq):
        ''' Stop Freq in Hz
        '''
        self.instr.write("SENSe1:FREQuency:STOP {}".format(freq))

    def selfCenterFreq(self, freq):
        ''' Center Freq in Hz
        '''
        self.instr.write("SENSe1:FREQuency:CENTer {}".format(freq))

    def setSpanFreq(self,freq):
        ''' span in Hz
        '''
        self.instr.write("SENSe1:FREQuency:SPAN {}".format(freq))    
        
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
        self.instr.write("SOUR:POW {}".format(power))
       
    def setFreq(self, freq):
        '''Frq for measurement
        '''
        self.instr.write("SOUR:FREQ {}".format(freq))
        
    def setStartPwr(self, pwr):
        ''' Start Freq in Hz
        '''
        self.instr.write("SENSe1:POWer:STARt {}".format(pwr))
        
    def setStopPwr(self, pwr):
        ''' Stop Freq in Hz
        '''
        self.instr.write("SENSe1:POWer:STOP {}".format(pwr))
        
    def numPoints(self, points):
        '''Number of points in measurement. 
        '''
        self.instr.write("SENSe1:SWEep:POINts {}".format(points))
        
    def avgClear(self):
        ''' Clears and restarts averaging of the measurement data. Does NOT apply to point averaging.
        '''
        self.instr.write("SENSe1:AVERage:CLEar")
        
    def avgCount(self, count):
        '''Sets the number of measurements to combine for an average. Must also set SENS:AVER[:STATe] ON
        '''
        if count < 65536 and count >= 1:
            self.instr.write("SENSe1:AVERage ON")
            self.instr.write("SENSe1:AVERage:COUNt {}".format(count))
        else:
            self.instr.write("SENSe1:AVERage OFF")
                
    def avgDone(self):
        '''Return true if averaging is complete, false if not.
        '''
        self.instr.timeout = 10000
        return bool(float(self.instr.query('STAT:OPER:AVER1:COND?')) or 0)
        
    def sweepDone(self):
        return bool(self.instr.query('STAT:OPER:DEV:COND?'))
            
#     def getData(self, cplx=False):
#         '''Retrieve Measurement data
#         returns numpy array
#         '''
#         while self.avgDone() is False:
#             pass
        
#         self.instr.write("FORMat ASCII")

#         if cplx:
#             self.instr.read('SYST:FCOR:CHAN:COUP:STAT OFF')
#             ans = self.instr.read("CALC:MEASure:Data? SDATA")
#             #ans = self.instr.read("putDataComplex - naRawData (0)")
#             real = []
#             imag = []
#             y = []
#             ya = [float(f) for f in ans.split(',')]

#             for i, yi in enumerate(ya):
#                 if i % 2 == 0:
#                     real.append(yi)
#                 else:
#                     imag.append(yi)
#                     y.append(real[-1] + 1j*imag[-1])
#             x = np.linspace(float(self.instr.query("SENSe1:FREQuency:START?")), float(self.instr.query("SENSe1:FREQuency:STOP?")), len(y))
#             return x, np.asarray(y, dtype=np.dtype(np.complex128))
#         else:         
#             ans = self.instr.query("CALCulate1:DATA? FDATA")
#             y = [float(f) for f in ans.split(',')]
#             x = np.linspace(float(self.instr.query("SENSe1:FREQuency:START?")), float(self.instr.query("SENSe1:FREQuency:STOP?")), len(y))
#             return x, np.asarray(y)
    
    def getData(self, cplx=True):
        '''Retrieve Measurement data
        returns numpy array
        '''
        while self.avgDone() is False:
            pass
        
        
        if cplx:
            ans = self.instr.query('Calc:meas:data:sdata?')
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
            x = np.linspace(float(self.instr.query("SENSe1:FREQuency:START?")), float(self.instr.query("SENSe1:FREQuency:STOP?")), len(y))
            
        return x, np.asarray(y, dtype=np.dtype(np.complex128))
       
            
    def plot(self):
        '''Simple Matplotlib Plot of Measurement'''
        if not self.measurements:
            self.setupMeas()
        
        x, y=self.getData()
        plt.plot(x, y)
    
    def analyze(self):
        '''Resonator Analysis'''
        y = self.getData()
        x = np.linspace(float(self.instr.query("SENSe1:FREQuency:START?")), float(self.instr.query("SENSe1:FREQuency:STOP?")), len(y))
        analyze('Analysis', x=x, y=y)

    def setIF(self, freq):
        '''Set IF Bandwidth in Hz'''
        self.instr.write("SENS:BWID {}".format(freq))