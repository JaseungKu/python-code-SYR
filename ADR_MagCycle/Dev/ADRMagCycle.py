# ADRMagCycle.py

"""
Mar 2021, Jaseung Ku
Python module for ADR mag cycle
"""

import pyvisa, serial
import logging
import time, datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import os
import h5py
import sys
sys.path.append('..\Instrument Driver')
import Lakeshore218, Lakeshore331, Agilent6641A, HeatSwitch, SR830

logging.basicConfig(level=logging.INFO) # set logging level to be INFO.

class Plotter(object):
    """
    Create a plot objec to plot various parameters vs time during a mag cycle
    """

    def __init__(self, title='Mag Cycle'):

        self.fig, self.axs = plt.subplots(2 ,1, figsize=(10,8))
        self.fig.autofmt_xdate()
        self.axs[0].set_title(title)
        self.lines = [[]] * 3   # 3 line plots and 6 axes

        xlabel = 'Time'
        ylabels = ['Volt. (V)', 'Meas.Curr (A)']
        line_labels = ['Set Volt.', 'Meas.Volt.', 'Meas.Curr.' ]
        line_plotStyles = ['b-', 'r-',  'b-']
        
        self.line2axis_map = [ 0, 0, 1]

        for i in range(3):  # set line property
            self.lines[i], = self.axs[self.line2axis_map[i]].plot([datetime.datetime.now()], [0], line_plotStyles[i])
            self.lines[i].set_label(line_labels[i])

        for i in range(2):   # set axis property
            self.axs[i].legend(loc=2)
            self.axs[i].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            self.axs[1].set_xlabel(xlabel, fontsize=20)
            self.axs[i].set_ylabel(ylabels[i], fontsize=20)
            self.axs[i].grid(which='both')
            self.axs[i].tick_params('both', labelsize=18)

    def update(self, xdata, *ydata):
        for i in range(3):
            self.lines[i].set_xdata(xdata)
            self.lines[i].set_ydata(ydata[i])

            self.axs[self.line2axis_map[i]].relim()
            self.axs[self.line2axis_map[i]].autoscale()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

class MagCycle(object):
    """
    - Base class for mag cycle
    - Args:
            soak_hour: soak duration in hour
            max_current : current at full field
            max_volt: final voltage to go during mag up. This voltage should be higher than the voltage
            required to output max current when the magnet inductive voltage is zero. Mag up will end before
            reaching max_volt since max_current will reach earlier.
            timestep_magup: time step in second during mag up
            timestep_magdown: time step in second during mag down
    """
    
    def __init__(self
                , soak_hour=1
                , max_current=9.2
                , max_volt=0.7
                , timestep_magup=3
                , timestep_magdown=5
                , inductive_voltage_limit=0.25):

        self.soak_hour = soak_hour
        self.max_current = max_current  # max set current
        self.max_volt = max_volt     # max set voltage
        self.timestep_magup = timestep_magup # How fast to ramp up voltage in sec during magup.
        self.timestep_magdown = timestep_magdown  # How fast to ramp down voltage in sec during magdown.
        self.initial_setvoltage = 0
        self.inductive_voltage_limit = inductive_voltage_limit # in V

        # plot initiialization
        self.plotter = Plotter(title=f'ADR1 MAG CYCLE MONITORING @{datetime.datetime.now():%x,%X}')

        # data : [time, Meas.V, Meas.I, 50K, 3K, GGG , FFA , set voltage, induc.volt]
        self.data = [np.array([])] * 4
        
    def initialize_instrument(self):
        """ Implement this in subclass. This is a placeholder""" 
        pass
    
    def _configure_power_supply(self):
        """ Configure power supply to set voltage and current.
            If output was (left) on, read set voltage to use as a starting voltage for magup, and set current=max_current
        """

        if self.power_supply.getOutputStatus():   # is output on?
            self.initial_setvoltage = self.power_supply.getSetVoltage()
            self.power_supply.setCurrent(self.max_current)
        else:
            self.power_supply.setVoltage(0)
            self.power_supply.setCurrent(self.max_current)  # for voltage-bias mode
            self.power_supply.outputOn()

    def cleanup(self):
        """
        Clean-up after magdown
        """
        self.heat_switch.close_port()  # Close port so that we can access heat switch elsewhere.

    def _update_data(self):
        """
        Update time, set voltage, measured voltage, inductive voltage, and measured current.
        """
        self.data[0] = np.append(self.data[0], datetime.datetime.now())
        self.data[1] = np.append(self.data[1], self.power_supply.getSetVoltage())  # set volt.
        self.data[2] = np.append(self.data[2], self.power_supply.measVoltage())
        self.data[3] = np.append(self.data[3], self.power_supply.measCurrent())

    def is_inductive_voltage_too_high(self):
        """ Check if the inductive voltage is higher than threshold """

        inductive_volt = self._read_latest_inductive_volt()

        if inductive_volt > self.inductive_voltage_limit:
            return True
        else:
            return False

    def _read_latest_inductive_volt(self):
        log_filename = self._find_log_file()
        with h5py.File(log_filename, 'r') as f:
            for i, v in enumerate(f['Log list']):
                if v[0] == 'Pos. Induct. Volt':
                    pos_induct_volt_index = i
                    break
            return np.abs(f['Data'][-1, pos_induct_volt_index+1])    # f['Data'] is 2d dataset. The first column is time. 

    def _find_log_file(self):

        month_folder = datetime.date.strftime(datetime.date.today(), '%Y-%m')
        filename = ''.join([self._log_subfolder, '-', datetime.date.strftime(datetime.date.today(), '%Y%m%d'),'.hdf5'])
        full_file_path = os.path.join(self._log_folder, self._log_subfolder, month_folder, filename)

        return full_file_path

    def _generate_magup_voltages(self):
        """
        Generate magup voltages until current reaches maximum set current.
        When power supply switches from CV mode from CC mode, this method stops generating voltages.
        """
        voltages = np.arange(self.initial_setvoltage, self.max_volt, 0.001)  # 1mV step

        logging.info('Voltage is ramping up...')
        for volt in voltages:
            if self.power_supply.is_CC_mode():
                logging.info(f'Current reached the max current {self.max_current} A...')
                return  # This ends generator.
            else:
                yield volt
                time.sleep(self.timestep_magup)

        logging.info(f'Waiting to reach the max current {self.max_current} A...')
        while True:
            if self.power_supply.is_CC_mode():
                logging.info(f'Current reached the max current {self.max_current} A...')
                break
            else:
                yield self.max_volt
                time.sleep(self.timestep_magup)

    def _generate_magdown_voltages(self):
        """
        Generate magdown voltages until current reaches 0A.
        """
        voltages = np.arange(self.power_supply.measVoltage(), 0, -0.001)  # 1mV step

        logging.info('Voltage is ramping down to zero...')
        for volt in voltages:
            yield volt
            time.sleep(self.timestep_magdown)

        logging.info('Waiting to reach 0 A...')
        while True:
            if self.power_supply.measCurrent() <= 0.05:
                break
            else:
                yield 0
                time.sleep(self.timestep_magdown)

    def mag_up(self):
        """  Do magup. """

        # Check if 3K is cold enough.
        T_3K = self.read_3K()
        if T_3K > 4.5:
            logging.info(f'3K stage temperature(={T_3K})is too hot (> 4.5K)! Mag cycle is aborted!')
            raise Exception('3K stage is too hot. Script aborted!')

        logging.info(f'Magup started @{datetime.datetime.now():%X}!')

        heat_switch_status = 'OPEN'

        # Ramp up voltage to the magnet
        for volt in self._generate_magup_voltages():
            self.power_supply.setVoltage(volt)
            self._update_data()
            self.plotter.update(*self.data)

            # if inductive voltage is too high, slow down ramping
            if self.is_inductive_voltage_too_high():
                time.sleep(5)       # 1mv/5sec ramp rate should be low enough to keep inductive voltage under 0.25V

            # Close heat switch when GGG temperature gets higher than 3 Kevin
            if heat_switch_status == 'OPEN' and self.read_GGG() > 3:
                self.heat_switch.close()
                logging.info(f'Heat switch closed @{datetime.datetime.now():%X}.')
                heat_switch_status = 'CLOSED'

        logging.info(f'Magup finished @{datetime.datetime.now():%X}!!')

    def mag_down(self):
        """
        Do magdown.
        Power supply output is turned off at the end of magdown.
        """
        logging.info(f'Magdown started @{datetime.datetime.now():%X}!')

        # Open heat switch
        self.heat_switch.open()
        logging.info(f'Heat switch opened @{datetime.datetime.now():%X}.')

        # Ramp down voltage to zero
        for volt in self._generate_magdown_voltages():
            self.power_supply.setVoltage(volt)
            self._update_data()
            self.plotter.update(*self.data)

            # if inductive voltage is too high, slow down ramping.
            if self.is_inductive_voltage_too_high():
                time.sleep(5)

        self.power_supply.outputOff()

        logging.info(f'Magdown finished @{datetime.datetime.now():%X}!')

    def soak(self):
        """
        Just wait during soak time. Do nothing other than plotting.
        """
        # cycle heat switch to release stress.
        self.heat_switch.open()
        logging.info(f'Heat switch opened @{datetime.datetime.now():%X}.')
        self.heat_switch.close()
        logging.info(f'Heat switch closed @{datetime.datetime.now():%X}.')

        init_time = datetime.datetime.now()
        logging.info(f'Soak started @{init_time:%X} and will last for {self.soak_hour} hr.')

        while True:
            curr_time = datetime.datetime.now()
            if (curr_time - init_time).seconds < self.soak_hour * 3600:
                self._update_data()
                self.plotter.update(*self.data)
                time.sleep(60)
            else :
                logging.info(f'Soak finished @{datetime.datetime.now():%X}')
                break

    @classmethod
    def run_mag_cycle(cls, **kwargs):
        """
        Run a complete mag cycle.
        Usage: ADR1MagCycle.run_mag_cycle(soak_hour=1)
        """

        logging.info(f'Mag cycle started @{datetime.datetime.now():%X}!')

        mag = cls(**kwargs)
        mag.initialize_instrument()
        mag.mag_up()
        mag.soak()
        mag.mag_down()
        mag.cleanup()

        logging.info(f'Mag cycle ended @{datetime.datetime.now():%X}! Yeah!')

    @classmethod
    def run_mag_down_only(cls, **kwargs):
        """
        Start magdown immediately from where you are.
        Usage: ADR1MagCycle.run_mag_down_only()
        """

        logging.info(f'Magdown started @{datetime.datetime.now():%x, %X}!')

        mag = cls(**kwargs)
        mag.initialize_instrument()
        mag.mag_down()
        mag.cleanup()

        logging.info(f'Magdown ended @{datetime.datetime.now():%x, %X}! Yeah!')

    @classmethod
    def schedule_mag_cycle(cls, start_mag_cycle_datetime, soak_hour=1):
        """
        Run a mag cycle at the scheduled date/time.
        start_mag_cycle_datetime : datetime object
        Usage: To run a mag cycle at 2019/10/11, 09:00 AM,
               ADR1MagCycle.schedule_mag_cycle(datetime.datetime(2019,10,11,9,0), soak_hour=4)
        """

        if input('Scheduled date/time are correct? (y/n)') == 'n':
            return logging.info('Aborted!')

        logging.info(f'Mag cycle is scheduled to start @{start_mag_cycle_datetime:%x. %X}')
        logging.info('Waiting to start a mag cycle...')

        while True:
            if datetime.datetime.now() >= start_mag_cycle_datetime:
                cls.run_mag_cycle(soak_hour=soak_hour)
                break
            else:
                time.sleep(60)

        end_mag_cycle_datetime = datetime.datetime.now()
        logging.info(f'Scheduled mag cycle is complete @{end_mag_cycle_datetime:%x, %X}! Yeah!')

    @classmethod
    def close_heat_switch(cls):
        """
        Standalone operation for closing heat switch
        """
        heat_switch = HeatSwitch.HeatSwitch(cls._HeatSwitch_PORT)
        heat_switch.close()
        logging.info(f'Heat switch closed @{datetime.datetime.now():%x, %X}.')
        heat_switch.close_port()   # close serial port so that it is available when trying to connect it again.

    @classmethod
    def open_heat_switch(cls):
        """
        Standalone operation for opening heat switch
        """
        heat_switch = HeatSwitch.HeatSwitch(cls._HeatSwitch_PORT)
        heat_switch.open()
        logging.info(f'Heat switch opened @{datetime.datetime.now():%x,%X}.')
        heat_switch.close_port() # close serial port so that it is available when trying to connect it again.

class ADR1MagCycle(MagCycle):
    """ 
        - This class needs to implement three methods: initialize_instrument, read_3K, and read_GGG.
        - To start a mag cycle right away, use the class method 'run_mag_cycle'.
        - To schedule a mag cycle, use the class method 'schedule_mag_cycle'  
        - Usage:
            To start mag cycle immediately with a given soak hour.
            >> ADR1MagCycle.run_mag_cycle(soak_hour=1)
            To schedule a mag cycle starting at 2019/10/11, 09:00 AM
            >> ADR1MagCycle.schedule_mag_cycle(datetime.datetime(2019,10,11,9,0), soak_hour=1)
    """
    _Agilent6641A_GPIB_ADDR = 12    # magnet power supply
    _Lakeshore218_GPIB_ADDR = 18    # 50K, 3K, inductive voltage
    _Lakeshore331_GPIB_ADDR = 14    # GGG
    _HeatSwitch_PORT = 'COM9'
    _log_folder = 'Z:\Logs\ADR1'
    _log_subfolder = 'ADR1 Log' # this name is set when to start logger. Don't change.

    def initialize_instrument(self):
        """
        Initialize instruments.
        """
        # connect instruments, create instrument object.
        self.power_supply = Agilent6641A.Agilent6641A(self._Agilent6641A_GPIB_ADDR)
        self.Lakeshore218 = Lakeshore218.Lakeshore218(self._Lakeshore218_GPIB_ADDR) # 50K, 3K, inductive voltage
        self.Lakeshore331 = Lakeshore331.Lakeshore331(self._Lakeshore331_GPIB_ADDR)  # GGG
        self.heat_switch = HeatSwitch.HeatSwitch(self._HeatSwitch_PORT)

        logging.info(f'All instrumient connected')

        self._configure_power_supply()

    def read_3K(self):
        """ Read 3K temperature """
        return self.Lakeshore218.getTemperature('1')

    def read_GGG(self):
        """ Read GGG temperature """
        return self.Lakeshore331.getTemperature('A')

class ADR2MagCycle(MagCycle):

    _Agilent6641A_GPIB_ADDR = 3     # magnet power supply
    _Lakeshore340_GPIB_ADDR = 1     # 50K, 3K, inductive voltage
    _Lakeshore332_GPIB_ADDR = 2     # GGG, FAA
    _HeatSwitch_PORT = 'COM3'
    _log_folder = 'Z:\Logs\ADR2'
    _log_subfolder = 'ADR2 Log'
    
  
    def initialize_instrument(self):
        """
        Initialize instruments.
        """
        # connect instruments
        self.power_supply = Agilent6641A.Agilent6641A(self._Agilent6641A_GPIB_ADDR)
        self.Lakeshore340 = Lakeshore340.Lakeshore340(self._Lakeshore340_GPIB_ADDR) # 50K, 3K
        self.Lakeshore332 = Lakeshore332.Lakeshore332(self._Lakeshore332_GPIB_ADDR)  # GGG, FFA
        self.heat_switch = HeatSwitch.HeatSwitch(self._HeatSwitch_PORT)

        logging.info(f'All instrument connected')

        self._configure_power_supply()

    def read_3K(self):
        """ Read 3K temperature """
        return self.Lakeshore340.getTemperature('A')

    def read_GGG(self):
        """ Read GGG temperature """
        return self.Lakeshore332.getTemperature('A')
