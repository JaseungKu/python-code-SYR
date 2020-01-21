# Nov 2016, Yebin Liu
# Add some line in Aug 2016, Jaseung Ku
# Original script by Caleb

# Gunnar did this
# Jaseung refined/fixed code 11/8/2019

import visa
import pyvisa
import numpy as np

class SR830:
    '''Class for SR830 Lock-In Amplifier'''
    def __init__(self, GPIB_ADDR):
        '''Object Constructor.
        Inputs - GPIB Address
        example: pna = AgilentN5230A(16)
        '''
        self.GPIB_ADDR = GPIB_ADDR     
        self.rm = pyvisa.ResourceManager()
        self.instr = self.rm.get_instrument('GPIB0::' + str(GPIB_ADDR) + '::INSTR')
        self.instr.write('FORM REAL,64')
            
    def IDN(self):
        '''*IDN?
        '''
        return self.instr.query('*IDN?')
    
       
    def setFreq(self, freq): # freq between 0.001 and 102000
        ''' Set frequency '''
        if freq <= 102000 and freq >= 0.001:
            self.instr.write("FREQ {}".format(freq))                              
        else:
            print('Frequency must be between 0.001 and 102000!')
                        
        # If harm > 1, freq limited to (harm)(phase)(freq) <= 102 kHz
        # Source must be internal
        
    def setAmpl(self, ampl): # ampl between 0.004 and 5
        ''' Set amplitude in V'''        
        if 0.004 <= ampl <= 5:
            self.instr.write("SLVL {}".format(ampl))          
        else:
            print ('Amplitude must be between 0.004 and 5!')       
        
    def setPhase(self, phase): # phase shift between -360 and 729.99, wrapped at +-180
        ''' Set phase shift '''        
        if -360 <= phase <= 729.99:
            self.instr.write("PHAS {}".format(phase))            
        else:
            print ('Phase shift must be between -360 and 729.99!')     
        
    def setSource(self, source): # external = 0, internal = 1
        ''' Set reference source '''
        if source == 'ext':
            self.instr.write("FMOD 0")
        elif source == 'int':
            self.instr.write("FMOD 1")
        else:
            print ('invalid entry')            
        
    def setHarm(self, harm): # harm between 1 and 19999
        ''' Set detection harmonic '''         
        if 1 <= harm <= 19999:
            self.instr.write("HARM {}".format(harm))
        else:
            print ('Detection harmonic must be between 1 and 19999!')
            
         # Value limited by (harm)(phase)(freq) <= 102kHz 
        # If harm requires a freq > 102 kHz, harm set to greatest value that fulfills ^^^

    def setTrig(self, trig): # sine 0 crossing = 0, TTL rising edge = 1, falling edge = 2
        ''' Set reference trigger '''        
        if trig == 'sine':
            self.instr.write("RSLP 0")
        elif trig == 'pos':
            self.instr.write("RSLP 1")
        elif trig == 'neg':
            self.instr.write("RSLP 2")
                    
    def setInputConfig(self, config): # A = 0, A-B = 1, 1megaOhm = 2, 100 megaOhm = 3
        ''' Set input configuration (current gain) '''
        if config == 'A':
            self.instr.write("ISRC 0")
        elif config == 'A-B':
            self.instr.write("ISRC 1")
        elif config == '1 megaOhm':
            self.instr.write("ISRC 2")
        elif config == '100 megaOhms':
            self.instr.write("ISRC 3")
        else:
            print ('invalid entry')
            
    
    def setShield(self, shield): # float = 0, ground = 1
        ''' Set input shield grounding '''
        if shield == 'float':
            self.instr.write("IGND 0")
        elif shield == 'ground':
            self.instr.write("IGND 1")
        else:
            print ('invalid entry')
            
    def setCoupling(self, coupling): # AC = 0, DC = 1
        ''' Set input coupling '''
        if coupling == 'AC':
            self.instr.write("ICPL 0")
        elif coupling == 'DC':
            self.instr.write("ICPL 1")
        else:
            print ('invalid entry')          
        
    def setFilter(self, filt):
        ''' Set input line notch filter '''
  #      self.instr.write("ILIN {}".format(filter_))
        # 0 = no filters in, 1 = line notch, 2 = 2xline notch, 3 = both
        if filt == 'none':
            self.instr.write("ILIN 0")          
        if filt == 'line':
            self.instr.write("ILIN 1")          
        if filt == '2xline':
            self.instr.write("ILIN 2")            
        if filt == 'both':
            self.instr.write("ILIN 3")            
        else:
            print ('invalid entry')            
    
    def setReserve(self, res): # High Reserve = 0, Normal = 1, Low Noise(minimum) = 2
        ''' Set reserve mode '''
        if res == 'high':
            self.instr.write("RMOD 0")
        elif res == 'normal':
            self.instr.write("RMOD 1")
        elif res == 'low':
            self.instr.write("RMOD 2")
        else:
            print ('invalid entry')           
            
    def setSlope(self, slope): # 6dB/oct = 0, 12dB/oct = 1, 18dB/oct = 2, 24dB/oct = 3
        ''' Set low pass filter slope '''
        if slope == 6:
            self.instr.write("OFSL 0")
        elif slope ==  12:
            self.instr.write("OFSL 1")
        elif slope ==  18:
            self.instr.write("OFSL 2")
        elif slope ==  24:
            self.instr.write("OFSL 3")
        else:
            print('invalid entry')            
    
    def setSync(self, sync): # off = 0, filtering below 200 Hz = 1
        ''' Set synchronous filter status '''
        if sync == 'off':
            self.instr.write("SYNC 0")     
        elif sync == 'on':
            self.instr.write("SYNC 1")    
        else:
            print ('invalid entry')            
        
    def readValue(self, var):
        if var == 'x':
            value = 1
        elif var == 'y':
            value = 2
        elif var == 'r':
            value = 3
        elif var == 'theta':
            value = 4
        else:
            print ('invaild entry')
            
        return float(self.instr.query("OUTP? {}".format(value)))
    
    def readX(self):
        s = str(self.instr.query("OUTP? 1"))
        new = s[:-1]
        a = float(new)
        return a 
    
    def readY(self):
        s = str(self.instr.query("OUTP? 2"))
        new = s[:-1]
        a = float(new)
        return a 
    
    def readR(self):
        s = str(self.instr.query("OUTP? 3"))
        new = s[:-1]
        a = float(new)
        return a 
    
    def readT(self):
        s = str(self.instr.query("OUTP? 4"))
        new = s[:]
        a = float(new)
        return a 
    
    def readXY(self):
        print (self.instr.query("SNAP? 1,2"))
        return
    
    def readRT(self):
        print (self.instr.query("SNAP? 3,4"))
        return
    
    def readAmpl(self):
        s = (self.instr.query("SLVL?"))
        new = s[:-1]
        a = float(new)
        return a      
    
    def askSource(self):
        return (self.instr.query("FMOD?"))        
  
    def setTimeConst(self, time):        
        ''' Set time constant '''        
        if time == '10 us':
            return self.instr.write("OFLT 0")
        elif time == '30 us':
            return self.instr.write("OFLT 1")
        elif time == '100 us':
            return self.instr.write("OFLT 2")
        elif time == '300 us':
            return self.instr.write("OFLT 3")
        elif time == '1 ms':
            return self.instr.write("OFLT 4")
        elif time == '3 ms':
            return self.instr.write("OFLT 5")
        elif time == '10 ms':
            return self.instr.write("OFLT 6")
        elif time == '30 ms':
            return self.instr.write("OFLT 7")
        elif time == '100 ms':
            return self.instr.write("OFLT 8")
        elif time == '300 ms':
            return self.instr.write("OFLT 9")
        elif time == '1 s':
            return self.instr.write("OFLT 10")
        elif time == '3 s':
            return self.instr.write("OFLT 11")
        elif time == '10 s':
            return self.instr.write("OFLT 12")
        elif time == '30 s':
            return self.instr.write("OFLT 13")
        elif time == '100 s':
            return self.instr.write("OFLT 14")
        elif time == '300 s':
            return self.instr.write("OFLT 15")
        elif time == '1 ks':
            return self.instr.write("OFLT 16")
        elif time == '3 ks':
            return self.instr.write("OFLT 17")
        elif time == '10 ks':
            return self.instr.write("OFLT 18")
        elif time == '30 ks':
            return self.instr.write("OFLT 19")
        else:
            print ('invalid entry')            
        
    def setSens(self, sens):        
        ''' Set sensitivity '''        
        if sens == '2 nV/fA':
            return self.instr.write("SENS 0")
        elif sens == '5 nV/fA':
            return self.instr.write("SENS 1")
        elif sens == '10 nV/fA':
            return self.instr.write("SENS 2")
        elif sens == '20 nV/fA':
            return self.instr.write("SENS 3")
        elif sens == '50 nV/fA':
            return self.instr.write("SENS 4")
        elif sens == '100 nV/fA':
            return self.instr.write("SENS 5")
        elif sens == '200 nV/fA':
            return self.instr.write("SENS 6")
        elif sens == '500 nV/fA':
            return self.instr.write("SENS 7")
        elif sens == '1 uV/pA':
            return self.instr.write("SENS 8")
        elif sens == '2 uV/pA':
            return self.instr.write("SENS 9")
        elif sens == '5 uV/pA':
            return self.instr.write("SENS 10")
        elif sens == '10 uV/pA':
            return self.instr.write("SENS 11")
        elif sens == '20 uV/pA':
            return self.instr.write("SENS 12")
        elif sens == '50 uV/pA':
            return self.instr.write("SENS 13")
        elif sens == '100 uV/pA':
            return self.instr.write("SENS 14")
        elif sens == '200 uV/pA':
            return self.instr.write("SENS 15")
        elif sens == '500 uV/pA':
            return self.instr.write("SENS 16")
        elif sens == '1 mV/nA':
            return self.instr.write("SENS 17")
        elif sens == '2 mV/nA':
            return self.instr.write("SENS 18")
        elif sens == '5 mV/nA':
            return self.instr.write("SENS 19")
        elif sens == '10 mV/nA':
            return self.instr.write("SENS 20")
        elif sens == '20 mV/nA':
            return self.instr.write("SENS 21")
        elif sens == '50 mV/nA':
            return self.instr.write("SENS 22")
        elif sens == '100 mV/nA':
            return self.instr.write("SENS 23")
        elif sens == '200 mV/nA':
            return self.instr.write("SENS 24")
        elif sens == '500 mV/nA':
            return self.instr.write("SENS 25")
        elif sens == '1 V/uA':
            return self.instr.write("SENS 26")
        else:
            print ("invalid entry")
            
            
        
        
        
        
        
        
        
        