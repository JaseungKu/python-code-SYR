# ADRMagCycle.py

"""
Nov 2019, Jaseung Ku
Python module for ADR mag cycle
"""

import pyvisa, serial
import logging
import time, datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('..\Instrument Driver')
import Lakeshore218, Lakeshore331, Agilent6641A, HeatSwitch, SR830 # ADR1
import Lakeshore340, Lakeshore332, Agilent6641A, HeatSwitch  # ADR2

logging.basicConfig(level=logging.INFO) # set logging level to be INFO.

class Plotter(object):
    """
    Create a plot objecto to plot various parameters vs time during a mag cycle
    """
    def __init__(self, title='title'):

        self.fig, self.axs = plt.subplots(2 ,1, figsize=(10,8))

        self.fig.suptitle(title)
        self.fig.autofmt_xdate()

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
            self.axs[1].set_xlabel(xlabel)
            self.axs[i].set_ylabel(ylabels[i])
            self.axs[i].grid(which='both')

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
    - Base class for mag cycle. Do not use this directly, instead, use a subclass, e.g., ADR1MagCycle.

    - Args:
            - soak_hour: soak duration in hour
            - max_current : current at full field
            - max_volt: final voltage to go during mag up. This voltage should be higher than the voltage
                required to output max current when the magnet inductive voltage is zero.
            - timestep_magup: time step in second during mag up
            - timestep_magdown: time step in second during mag down
            - plot_title : plot title
    """
    _log_folder = None  # logger main folder in labshare
    _log_subfolder = None  # (folder) name given by user that logger creates when it runs.
    _inductive_voltage_limit = 0.25  # in V

    def __init__(self, soak_hour=None, max_current=None, max_volt=None, timestep_magup=None, timestep_magdown=None, plot_title=None):
        self.soak_hour = soak_hour
        self.max_current = max_current  # max set current
        self.max_volt = max_volt     # max set voltage
        self.timestep_magup = timestep_magup # How fast to ramp up voltage in sec during magup.
        self.timestep_magdown = timestep_magdown  # How fast to ramp down voltage in sec during magdown.

        self._initial_setvoltage = None
        self._temperature_3K = None
        self._temperature_GGG  = None

        self.plotter = Plotter(title=plot_title)
        self.data = [np.array([])] * 4  # data : [time,  set voltage, meas.V, Meas.I,]

        self.configure_instrument()

    def configure_instrument(self):
        """
        Configure instruments.
        """
        # connect instruments
        self.power_supply = Agilent6641A.Agilent6641A(self._Agilent6641A_GPIB_ADDR)
        self.heat_switch = HeatSwitch.HeatSwitch(self._HeatSwitch_PORT)

        logging.info(f'Power supply and heat switch were connected')

         # configure power supply to set voltage and current
         # If output was (left) on, read set voltage to use as a starting voltage for magup, and set current=max_current
        if self.power_supply.getOutputStatus():
            self._initial_setvoltage = self.power_supply.getSetVoltage()  # what is the current set voltage?
            self.power_supply.setCurrent(self.max_current)
        else:    # if output is off, set V=0 and I=maxCurr. Then turn on output.
            self.power_supply.setVoltage(0)
            self.power_supply.setCurrent(self.max_current)  # for voltage-bias mode
            self.power_supply.outputOn()

    def cleanup(self):
        """
        Clean-up after magdown
        """
        self.heat_switch.close_port()  # Close port so that we can access heat switch elsewhere.

    @property
    def temperature_3K(self):
        # self._temperature_3K = self.Lakeshore331.getTemperature('A')
        self._temperature_3K = self._read_latest_3K()
        return self._temperature_3K

    @property
    def temperature_GGG(self):
        # self._temperature_GGG = self.Lakeshore332.getTemperature('A')
        self._temperature_GGG = self._read_latest_GGG()
        return self._temperature_GGG

    def _update_data(self):
        """
        Update time, set voltage, measured voltage, and measured current.
        """
        self.data[0] = np.append(self.data[0], datetime.datetime.now())
        self.data[1] = np.append(self.data[1], self.power_supply.getSetVoltage())  # set volt.
        self.data[2] = np.append(self.data[2], self.power_supply.measVoltage())
        self.data[3] = np.append(self.data[3], self.power_supply.measCurrent())

    def is_inductive_voltage_too_high(self):
        """ Check if the inductive voltage is higher than threshold """

        inductive_volt = self._read_latest_inductive_volt()

        if inductive_volt > self._inductive_voltage_limit:
            return True
        else:
            return False

    def _read_latest_inductive_volt(self):
        log_filename = self._find_log_file()
        with h5py.File(log_filename, 'r') as f:
            return np.abs(f['Data'][-1][5])    # f['Data'] is an array with 6 elements. 6th element is inductive voltage.

    def _read_latest_3K(self):
        log_filename = self._find_log_file()
        with h5py.File(log_filename, 'r') as f:
            return f['Data'][-1][2]   # f['Data'] is an array with 6 elements. 6th element is inductive voltage.

    def _read_latest_GGG(self):
        log_filename = self._find_log_file()
        with h5py.File(log_filename, 'r') as f:
            return f['Data'][-1][3]    # f['Data'] is an array with 6 elements. 6th element is inductive voltage.

    def _find_log_file(self):

        month_folder = datetime.date.strftime(datetime.date.today(), '%Y-%m')
        filename = ''.join([self._log_subfolder, '-', datetime.date.strftime(datetime.date.today(), '%Y%m%d'),'.hdf5'])
        full_file_path = os.path.join(self._log_folder, self._log_subfolder, month_folder, filename)

        return full_file_path

    def _magup_voltages(self):
        """
        Generate magup voltages until current reaches maximum set current.
        When power supply switches from CV mode from CC mode, this method stops generating voltages.
        """
        voltages = np.arange(self._initial_setvoltage, self.max_volt, 0.001)  # 1mV step

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

    def _magdown_voltages(self):
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
        # Check if 3K is cold
        if self.temperature_3K > 4.5:
            logging.info(f'3K stage temperature(={self.temperature_3K})is too hot (> 4.5K)! Mag cycle is aborted!')
            raise Exception('3K stage is too hot. Script aborted!')

        logging.info(f'Magup started @{datetime.datetime.now():%X}!')

        heat_switch_status = 'OPEN'

        # Ramp up voltage to the magnet
        for volt in self._magup_voltages():
            self.power_supply.setVoltage(volt)
            self._update_data()
            self.plotter.update(*self.data)

            # if inductive voltage is high threshold, slow down ramping
            if self.is_inductive_voltage_too_high():
                time.sleep(5)   # 1mv/5sec ramp rate should be low enough to keep inductive voltage under 0.25V

            # Close heat switch when GGG temperature gets higher than 3 Kevin
            if heat_switch_status == 'OPEN' and self.temperature_GGG > 3:
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
        for volt in self._magdown_voltages():
            self.power_supply.setVoltage(volt)
            self._update_data()
            self.plotter.update(*self.data)

            # if inductive voltage is high threshold, slow down ramping
            if self.is_inductive_voltage_too_high():
                time.sleep(5)   # 1mv/5sec ramp rate should be low enough to keep inductive voltage under 0.25V

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

    def fast_mag_down(self):
        """
        Quickly ramp down voltage/current to zero. Not sure if this would cause magnet quench.
        """
        self.timestep_magdown = 1  # 1mv/sec

        logging.info(f'Fast magdown started @{datetime.datetime.now():%X}!')

        # Ramp down voltage to zero
        for volt in self._magdown_voltages():
            self.power_supply.setVoltage(volt)
            self._update_data()
            self.plotter.update(*self.data)

        self.power_supply.outputOff()

        logging.info(f'Fast magdown finished @{datetime.datetime.now():%X}!')

    @classmethod
    def run_mag_cycle(cls, **kwargs):
        """
        Run a complete mag cycle.
        Usage: MagCycle.run_mag_cycle(soak_hour=1)
        """

        logging.info(f'Mag cycle started @{datetime.datetime.now():%X}!')

        mag = cls(**kwargs)
        mag.mag_up()
        mag.soak()
        mag.mag_down()
        mag.cleanup()

        logging.info(f'Mag cycle ended @{datetime.datetime.now():%X}! Yeah!')

    @classmethod
    def run_mag_down_only(cls, **kwargs):
        """
        Start magdown immediately from where you are.
        Usage: MagCycle.run_mag_down_only()
        """

        logging.info(f'Magdown started @{datetime.datetime.now():%X}!')

        mag = cls(**kwargs)
        mag.mag_down()
        mag.cleanup()

        logging.info(f'Magdown ended @{datetime.datetime.now():%X}! Yeah!')

    @classmethod
    def schedule_mag_cycle(cls, start_mag_cycle_datetime, **kwargs):
        """
        Run a mag cycle at the scheduled date/time.
        start_mag_cycle_datetime : datetime object
        Usage: To run a mag cycle at 2019/10/11, 09:00 AM,
               MagCycle.schedule_mag_cycle(datetime.datetime(2019,10,11,9,0), soak_hour=4)
        """

        if input('Scheduled date/time are correct? (y/n)') == 'n':
            return logging.info('Aborted!')

        logging.info(f'Mag cycle is scheduled to start @{start_mag_cycle_datetime:%x. %X}')
        logging.info('Waiting to start a mag cycle...')

        while True:
            if datetime.datetime.now() >= start_mag_cycle_datetime:
                cls.run_mag_cycle(**kwargs)
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
        logging.info(f'Heat switch closed @{datetime.datetime.now():%X}.')
        heat_switch.close_port()   # close serial port so that it is available when trying to connect it again.

    @classmethod
    def open_heat_switch(cls):
        """
        Standalone operation for opening heat switch
        """
        heat_switch = HeatSwitch.HeatSwitch(cls._HeatSwitch_PORT)
        heat_switch.open()
        logging.info(f'Heat switch opened @{datetime.datetime.now():%X}.')
        heat_switch.close_port() # close serial port so that it is available when trying to connect it again.

class ADR1MagCycle(MagCycle):
    """ Subclass for ADR1.
    - Usage: To start mag cycle, use either 'run_mag_cycle' or 'schedule_mag_cycle' method. See below for example.

            # To start mag cycle immediately with a given soak hour.
            ADR1MagCycle.run_mag_cycle(soak_hour=1)

            # To schedule a mag cycle starting at 2019/10/11, 09:00 AM
            ADR1MagCycle.schedule_mag_cycle(datetime.datetime(2019,10,11,9,0), soak_hour=1)
    """
    _Agilent6641A_GPIB_ADDR = 12
    _HeatSwitch_PORT = 'COM9'

    _log_folder = 'Z:\Logs\ADR1'
    _log_subfolder = 'ADR1 Log'

    def __init__(self
                , soak_hour=1
                , max_current=9.2
                , max_volt=0.7
                , timestep_magup=3
                , timestep_magdown=5
                , plot_title=f'ADR1 MAG CYCLE V and I MONITORING @{datetime.datetime.now():%x,%X}'
                ):
        super().__init__(soak_hour=soak_hour, max_current=max_current, max_volt=max_volt, timestep_magup=timestep_magup
                        , timestep_magdown=timestep_magdown, plot_title=plot_title)

class ADR2MagCycle(MagCycle):
    """ Subclass for ADR2  """

    _Agilent6641A_GPIB_ADDR = 3
    _HeatSwitch_PORT = 'COM3'

    _log_folder = 'Z:\Logs\ADR2'
    _log_subfolder = 'ADR2 Log'

    def __init__(self
                , soak_hour=1
                , max_current=9.2
                , max_volt=0.6
                , timestep_magup=3
                , timestep_magdown=5
                , plot_title=f'ADR2 MAG CYCLE V and I MONITORING @{datetime.datetime.now():%x,%X}'
                ):
        super().__init__(soak_hour=soak_hour, max_current=max_current, max_volt=max_volt, timestep_magup=timestep_magup
                        , timestep_magdown=timestep_magdown, plot_title=plot_title)

class PID_T_Control(object):
    _Agilent6641A_GPIB_ADDR = 12
    _HeatSwitch_PORT = 'COM9'

    _log_folder = 'Z:\Logs\ADR1'
    _log_subfolder = 'ADR1 Log'


    def __init__(self, P, I, D):
        self.P =P
        self.I = I
        self.D = D

    def configure_instrument(self):
        self.power_supply = Agilent6641A.Agilent6641A(self._Agilent6641A_GPIB_ADDR)

    @property
    def temperature_FAA(self):
        # self._temperature_GGG = self.Lakeshore332.getTemperature('A')
        self._temperature_FAA = self._read_latest_FAA()
        return self._temperature_FAA

    def _read_latest_FAA(self):
        log_filename = self._find_log_file()
        with h5py.File(log_filename, 'r') as f:
            return f['Data'][-1][4]    # f['Data'] is an array with 6 elements. 6th element is inductive voltage.

    def _find_log_file(self):

        month_folder = datetime.date.strftime(datetime.date.today(), '%Y-%m')
        filename = ''.join([self._log_subfolder, '-', datetime.date.strftime(datetime.date.today(), '%Y%m%d'),'.hdf5'])
        full_file_path = os.path.join(self._log_folder, self._log_subfolder, month_folder, filename)

        return full_file_path

    def set_FFA_temperature(self, temperature):
        for volt in self.PID_volt(temperature):
            time.sleep(self.time_interval)
            self.power_supply.setVoltage(volt)

    def PID_volt(self, target_temperature):
        """ generate next voltage"""
        integral = 0
        whiel True:
            e = (target_temperature - self.temperature_FAA)
            integral =  integral + e * self.time_interval
            next_volt = self.P * e +  I * integral
            if next_volt > ?:
                yield self.volt_limit
            else :
                yield next_volt
            
