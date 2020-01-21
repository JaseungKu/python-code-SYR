# Nov 2019, Jaseung Ku

import serial
import time

class HeatSwitch(object):
    '''
    Class for Heat Switch control. This controls Ardino, which controls heat switch.
    '''
    
    def __init__(self, COM_ADDR):
        '''
        Object Constructor.
        EX) COM_ADDR : 'COM3'
        '''     
        self.instr = serial.Serial(COM_ADDR)    
        time.sleep(3)
        
    def open(self):
        self.instr.write(b'O')
        time.sleep(5)
#         self.write(b'O')
    
    def close(self):
        self.instr.write(b'C')
        time.sleep(5)
#         self.write(b'C')

    def close_port(self):
        self.instr.close()