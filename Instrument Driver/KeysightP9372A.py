#!/usr/bin/env python
import sys
import os
from comtypes.client import GetModule
from comtypes.client import CreateObject
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

class KeysightP9372A:
    '''Class for Keysight P9372A Network Analyzer'''
    def __init__(self, ADDR):
        '''Object Constructor.
        Inputs - GPIB Address
        example: pna = KeysightP9372A('PXI10::0-0.0::INSTR')
        '''

        self.address = ADDR
        self.measurements = []

        GetModule("C:\Program Files\IVI Foundation\IVI\Bin\AgNA_64.dll")

        from comtypes.gen import AgNALib

        self.VNAObj = CreateObject('AgNA.AgNA')

    def write(self, command):
        """Write commands to Instrument"""
        self.VNAObj.System.ScpiPassThrough.WriteString(command)

    def read(self):
        """Read from Instrument"""
        val = self.VNAObj.System.ScpiPassThrough.ReadString()

        try:
            return float(val)
        except ValueError:
            return val

    def ask(self, command):
        self.write(command)
        return self.read()

    def connect(self, display=False):

        '''Connect to PNA and initialize S21 Measurement'''
        if not self.VNAObj.Initialized:
            self.VNAObj.Initialize(self.address, False, False, '')

        if display:
            self.VNAObj.Display.Enabled = True
            self.VNAObj.Windows.Add(1)

        self.write('FORM REAL,32;')

    def IDN(self):
        '''*IDN?
        '''
        return self.ask('*IDN?')

    def setupMeas(self, meas='S21', name="S21Meas"):
        '''Creates Measurement
            meas - S11, S12, S21, or S22
            name - A name to keep track of the measurement
        '''
        if meas in ['S11', 'S12', 'S21', 'S22']:
            self.write("CALCulate:PARameter:DEFine:EXT '{}',{}".format(name, meas))
            self.write("DISPlay:WINDow1:TRACe1:FEED '{}'".format(name))
            self.measurements.append(name)
            # print("Initialized {} Measurement '{}'".format(meas, name))
            return name
        else:
            print("Measurement must be S11, S12, S21, or S22")

    def startF(self, freq):
        ''' Start Freq in GHz
        '''
        self.write("SENSe1:FREQuency:STARt {}GHz".format(freq))

    def stopF(self, freq):
        ''' Stop Freq in GHz
        '''
        self.write("SENSe1:FREQuency:STOP {}GHz".format(freq))

    def centerF(self, freq):
        ''' Center Freq in GHz
        '''
        self.write("SENSe1:FREQuency:CENTer {}GHz".format(freq))

    def spanf(self,freq):
        ''' span in MHz
        '''
        self.write("sENSe1:frequency:SPAN {}MHz".format(freq))

    def pwrOn(self):
        '''Power On
        '''
        self.write('OUTP 1')

    def pwrOff(self):
        '''Power Off'''
        self.write("OUTP 0")

    def setPwr(self, power):
        '''Power for measurement
        '''
        self.write("SOUR:POW {:.2f}".format(power))

    def numPoints(self, points):
        '''Number of points in measurement.
        '''
        self.write("SENSe1:SWEep:POINts {}".format(points))

    def avgClear(self):
        ''' Clears and restarts averaging of the measurement data. Does NOT apply to point averaging.
        '''
        self.write("SENSe1:AVERage:CLEar")

    def avgCount(self, count):
        '''Sets the number of measurements to combine for an average. Must also set SENS:AVER[:STATe] ON
        '''
        if count < 65536 and count > 1:
            self.write("SENSe1:AVERage ON")
            self.write("SENSe1:AVERage:COUNt {}".format(count))
        else:
            print("Count must be between 1 and 65536.")

    def avgDone(self):
        '''Return true if averaging is complete, false if not.
        '''
        return bool(float(self.ask('STAT:OPER:AVER1:COND?')) or 0)

    def sweepDone(self):
        return bool(self.ask('STAT:OPER:DEV:COND?'))

    def getData(self, cplx=False):
        '''Retrieve Measurement data
        returns numpy array
        '''
        while self.avgDone() is False:
            pass

        self.write(':FORM REAL,32;CALC:DATA? SDATA')
        data = self.VNAObj.System.ScpiPassThrough.ReadIEEEBlockR4()

        i = np.array(data[0::2])
        q = np.array(data[1::2])
        vec = i + 1j*q

        x = np.linspace(float(self.ask("SENSe1:FREQuency:START?")),
        float(self.ask("SENSe1:FREQuency:STOP?")),
        len(vec))

        if cplx:
            return x, vec
        else:
            return x, np.abs(vec)

    def plot(self):
        '''Simple Matplotlib Plot of Measurement'''
        if not self.measurements:
            self.setupMeas()

        x, y=self.getData()
        plt.plot(x, y)

    def analyze(self):
        '''Resonator Analysis'''
        y = self.getData()
        x = np.linspace(float(self.instr.ask("SENSe1:FREQuency:START?")), float(self.instr.ask("SENSe1:FREQuency:STOP?")), len(y))
        analyze('Analysis', x=x, y=y)

    def setIF(self,count):
	    '''Set IF Bandwidth in KHZ'''
	    self.write("SENS:BWID {}KHZ".format(count/1000.))

    def setSweepType(self, mode='linear'):
        '''Set sweep mode : linear sweep, log sweep, CW sweep, etc
           mode : LINear | LOGarithmic | POWer | CW | SEGMent | PHASe'''
        self.write("SENSe1:SWEep:TYPE {}".format(mode))

    def setCWFreq(self, freq):
        ''' Set CW fixed frequency '''
        self.write("SENSe1:FREQuency {}".format(freq))

    def setFreqStartEnd(self, startFreq, endFreq):
        ''' Set start and end frequency '''
        self.write("SENSe1:FREQuency:STARt {}".format(startFreq))
        self.write("SENSe1:FREQuency:STOP {}".format(endFreq))

    def setFreqCenterSpan(self, centerFreq, spanFreq):
        ''' Set start and end frequency '''
        self.write("SENSe1:FREQuency:CENTer {}".format(centerFreq))
        self.write("sENSe1:frequency:SPAN {}".format(spanFreq))

    def autoscale(self):
    	'''Performs an autoscale on trace 1'''
    	sleep(0.2)
    	self.write("DISP:WIND1:TRAC1:Y:AUTO")
