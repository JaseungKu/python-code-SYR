# module : PNA_Exp.py, Plotter.py

###########################################################################################
# Goal: Make it easy and fast (1) to build a type of experiemnt and (2) to run Measurement
# Idea is to define each function that corresponds to a type of measurement, rather than making
# a generic experiment class like Qlab. The reason is by giving up some abstraction, we want
# to have more flexibility and intuition. Once we make one type of measurement, we rarely change it.
###########################################################################################

# Plotter.py
class Plot1D_1sub(object):
    pass

class Plot1D_2sub(object):
    pass

class Plot2D_1sub(object):
    pass

class Plot2D_4sub(object):


import numpy as np
import visa
import os
import re

class PNA_Factory(AgilentN5230A.AgilentN5230A):
    '''
    This object peforms what we want PNA to do, including basic individual operations provided by instrument driver and
    compositions of operatioins, for example, configure method.
    This class Inherites PNA instrument driver class.
    '''

    def __init__(self, address=address))
        super().__init__(address)

    def configure(self, sweepType=sweepType, IF=IF, avg=avg, numPoints=numPoints, **kwargs):
        self.setupMeas()
        self.setSweepType(sweepType)
        if sweepType == 'linear':
            self.setFreqStartEnd(kwargs['startFreq'],kwargs['endFreq'])
        elif sweepType == 'CW':
            self.setCWFreq(kwargs['CWFreq'])
        self.IFBandwith(IF)
        self.avgCount(avg)
        self.numPoints(numPoints)

class FileHandler(object):
    """
        To create a log file which contains parameters from Setting instance
        , and to create data file.
    """
    def __init__(self, exp_name, setting, dataobj):
        self.setting = setting

        # create a sample_ID folder followed by date folder with yyyy-mm-dd format
        self.sample_ID_folder = os.path.join(self.setting.save_base_path, self.setting.sample_ID)
        self.date_folder = datatime.datetime.today().strftime('%Y-%m-%d')
        self.full_file_path = os.path.join(self.setting.save_base_path, self.setting.sample_ID, self.date_folder)

        try:
            os.mkdir(self.sample_ID_folder)
        except FileExistsError:
            pass

        try:
            os.mkdir(sel.full_file_path)
        except FileExistsError:
            pass

        self.file_ID_num = self.get_file_ID_num() # start from 1
        self.base_file_name = '_'.join([self.file_ID_num, setting.sample_ID, self.exp_name])
        self.log_file_name = self.base_file_name + '.json'
        self.data_file_name = self.base_file_name + '.dat'

    def get_file_ID_num(self):
        IDs = []
        for (root,dirs,files) in os.walk(self.sample_ID_folder, topdown=true):
            matchobj = re.match(r'^\d+', files)
            IDs.append(int(matchobj.group()))

        return str(np.max(IDs) + 1)

    def create_log_file(self):
        # file_name = FileNameFormatter(setting)
        full_log_file_path =  os.path.join(self.setting.save_base_path
                                        , self.setting.sample_ID
                                        , self.folder_date
                                        , self.log_file_name )

        with open(full_log_file_path, 'w') as f:
            json.dump(self.to_dict(self.setting), f, indent=4, sort_keys=True)

    def to_dict(self, c):
        d = dict( (key, value)
                for (key, value)
                in c.__class__.__dict__.items()
                if not key.startswith('__')
                )
        return d

    def update_data_file(self):
        with  open(self.data_file_name 'wb') as f:
            np.savetxt(f, self.dataobj.data, fmt='%.9g', delimiter=',') # comma seperated

class DataContainer(object):
    """
        'data' attribute stores S21 data during sweep.
        New data is vertically stacked.
    """
    def __init__(self):
        self.data = None   # 1D or 2D array of S21
        self._data_dB = None
        self._data_real = None
        self._data_imag = None
        self._data_angle = None
        for i in range(num_data):
            self.

    @property
    def data_dB(self):
        self._data_dB = 20 * np.log10(np.absolute(self.data))
        return _data_dB

    @property
    def data_real(self):
        self._data_real = np.real(self.data)
        return _data_real

    @property
    def data_imag(self):
        self._data_imag = np.image(self.data)
        return _data_imag

    @property
    def data_angle(self):
        self._data_angle = np.angle(self.data, degrer=True)  # in degree
        return _data_angle

    def update(self, S21, *args):
        # args can be any numbers that can go with S21, for example, spec_freq or voltages
        # even though they can be noramlly scaled based on sweep parameters.
        # If self.data is 2D like 2D power scan, no args.
        # If self.data is 1D like 1D spectroscopy, args can have spec_freq or no args at all.
        data = np.append(S21, [*args])  # concatenate S21 and arguments
        if self.data is None:
            self.data = data
        else:
            self.data = np.vstack(self.data, data)  # append to axis=0 direction

class Setting(object):
    allowed_attributes = {
    'pna_pna_start_freq', 'pna_pna_end_freq', 'pna_CW_freq', 'pna_power' 'num_points','avg', 'IF'
    ,'flux_volt'
    , 'sweep1_start', 'sweep1_end', 'sweep1_step'
    , 'sweep2_start', 'sweep2_end', 'sweep2_step'
    , 'sweep3_start', 'sweep3_end', 'sweep3_step'
    , 'save_path', 'sample_ID', 'suffix'
    }

def cav_power_2D(exp_name, setting):

    # instrument setting
    pna = AgilentN5230A.AgilentN5230A(setting.PNA_GPIB_ADDR)
    pna = setting.pna
    
    if  hasattr(setting, 'flux_volt'):
        flux_instr = []
        for i in setting.flux_volt):
            flux_instr.append( SIM.SIM(setting.SIM_GPIB_ADDR, channel=setting.SIM_channels[i]) )

    ## data DataContainer
    dataobj = DataContainer()  # measured data stores in dataobj
    # log and data file
    fileobj = FileHandler(exp_name, setting, dataobj)  # pass setting parameters and data.
    # plot setup
    plotobj= Plotter.Plot2D_1sub(xlabel='Power (dBm)', ylabel = 'Frequency(Hz)', title = fileobj.base_file_name)

    # initialize instruments
    pna.configure(sweepTyep='linear', startFreq=setting.pna_start_freq, endFreq=setting.pna_end_freq
                , avg=setting.avg, numPoints=setting.num_points)
    pna.pwrOn()
    if not num_flux is 0:
        for volt, instr in zip(setting.flux_volt, flux_instr):
            instr.setVolage(volt)

    # sweep
    sweep1_values = np.arange(setting.sweep1_start, setting.sweep1_end + setting.sweep1_step, setting.sweep1_step): # traverse in [pmin, pmax].
    IF_bandwiths = np.linspace(setting.IF_start, setting.IF_end, len(sweep1_values)) # IFbandwidth scales up linearly

    for pwr, IFBW in zip(sweep1_values, IF_bandwiths):

        # clear_output()
        print(f'startPwr={setting.sweep1_start:.3g} dBm, endPwr={setting.sweep1_end:.3g} dBm, current power={pwr:.3g} dBm')

        # configure
        pna.setIF(IFBW)
        pna.setPwr(pwr)
        pna.avgClear()

        # fetch data from PNA
        freq, S21 = pna.getData(cplx=True) # S21 in linear scale

        # data update
        dataobj.update(S21) # For 2D data
        # dataobj.update(S21, spec_freq) # For 1D data like 1D spec.

        # plot update
        extent = [setting.sweep1_start, pwr, setting.pna_start_freq, setting.pna_end_freq]
        plotobj.update(dataobj.data_dB, extent)

        # save data in each iteration
        fileobj.update_data_file()

    # Post measurement
    pna.setPwr(-60)
    pna.pwrOff()
    plotobj.fig.savefig(os.path.join(fileobj.full_file_path, fileobj.base_file_name + '.png'))
    print('Measurement complete!!!')

def cav_flux_2D(setting):

    # instrument setting
    pna = AgilentN5230A.AgilentN5230A(setting.PNA_GPIB_ADDR)
    if  hasattr(setting, 'flux_volt'):
        flux_instr = []
        for i in setting.flux_volt:
            flux_instr.append( SIM.SIM(setting.SIM_GPIB_ADDR, channel=setting.SIM_channels[i]) )

    ## data DataContainer
    dataobj = DataContainer()  # measured data stores in dataobj
    # log and data file
    fileobj = FileHandler(exp_name, setting, dataobj)  # pass setting parameters and data.
    # plot setup
    plotobj= Plotter.Plot2D_1sub(xlabel='Flux (V)', ylabel = 'Frequency (Hz)', title = fileobj.base_file_name)

    # initialize instruments
    pna.configure(sweepTyep='linear', startFreq=setting.pna_start_freq, endFreq=setting.pna_end_freq
                , avg=setting.avg, numPoints=setting.num_points, IF=setting.IF)
    pna.pwrOn()

    # sweep
    sweep1_values = np.arange(setting.sweep1_start, setting.sweep1_end + setting.sweep1_step, setting.sweep1_step): # traverse in [pmin, pmax].

    for val in sweep1_values:

        # configure
        flux_instr[0].setVolage(val)
        pna.avgClear()

        # fetch data from PNA
        freq, S21 = pna.getData(cplx=True) # S21 in linear scale

        # data update
        dataobj.update(S21) # For 2D data
        # dataobj.update(S21, spec_freq) # For 1D data like 1D spec.

        # plot update
        extent = [setting.sweep1_start, pwr, setting.pna_start_freq, setting.pna_end_freq]
        plotobj.update(dataobj.data_dB, extent)

        # save data in each iteration
        fileobj.update_data_file()

    # Post measurement
    pna.pwrOff()
    plotobj.fig.savefig(os.path.join(fileobj.full_file_path, fileobj.base_file_name + '.png'))
    print('Measurement complete!!!')

def cav_flux1_flux2_2D()
def spec_1D
def spec_power_2D
def spec_flux_2D

##################################################################################
#### usage in jupyter notebook ###################################################
import Plotter  # Classes for different types of plot styles are defined.
import PNA_Exp  # Classes used to build each measurement, e.g., cav_power_2D, cav_flux_2D, cav_flux1_flux2_2D, spec_1D, spec_2D,


# Global setting for instruments
setting.PNA_GPIB_ADDR = 0
setting.SIM_GPIB_ADDR = 0
setting.SIM_SERIAL_PORT = 'COM6'
setting.SIM_channels = (2,3,4)  # each element corresponds to channel number
setting.Hittite_GPIB_ADDR = 0

# Define instruments to be used
setting.pna = AgilentN5230A.AgilentN5230A(setting.PNA_GPIB_ADDR)

############################ Set parameters which are directly used in instruments ############
#### cav_power_2D ############33333
setting = PNA_Exp.Setting()

# PNA setting
setting.pna_start_freq, setting.pna_end_freq = 4.5e9, 5.1e9
setting.num_points = 801
setting.avg = 1
setting.IF = 500

# Flux Setting
# Each element corresponds to each SIM value. Also, this tells how many SIMs are used.
# comment out if no SIM is used,i.e., remove flux_volt parameter.
setting.flux_instr_list = [SIM.SIM(setting.SIM_GPIB_ADDR, ch) for ch in setting.SIM_channels]
setting.flux_volt_list = [0, 0] # in volt
assert len(flux_instr_list) == len(flux_volt_list), 'The number of SIMs and values should be equal.'

# Sweep Setting
setting.IF_start, setting.IF_end = 100, 2000  # linearly scaled
setting.sweep1_start, setting.sweep1_end, setting.sweep1_step =  -80, -20, 1
# setting.sweep_start_2, setting.sweep_end_2, setting.sweep_step_2 =  3e9, 10e9, 10e6

# File Setting
# file name = ID num + sampleID + exp_name
setting.save_base_path = 'z:\User\Jaseung'
setting.sample_ID = 'WisCST'  # Folder with sample_ID is created under save_path
setting.exp_name = 'cav_power_2D' # All file name will be prepended with sample_ID.
###########################################################3#################################

cav_power_2D(setting, expName)

############################ Set parameters which are directly used in instruments ############
#### cav_flux_2D ############33333

# PNA setting
setting.pna_start_freq, setting.pna_end_freq = 4.5e9, 5.1e9
setting.num_points = 801
setting.avg = 1
setting.IF = 500

# Flux Setting
# Each element corresponds to each SIM value. Also, this tells how many SIMs are used.
# Comment out if no SIM is used.
setting.flux_volt = None # in volt

# Sweep Setting
setting.sweep1_start, setting.sweep1_end, setting.sweep1_step =  -2, 2, 0.005
# setting.sweep_start_2, setting.sweep_end_2, setting.sweep_step_2 =  3e9, 10e9, 10e6

# File Setting
setting.save_base_path = 'z:\User\Jaseung'
setting.sample_ID = 'WisCST'  # Folder with sample_ID is created under save_path
setting.exp_name = 'cav_flux_2D' # All file name will be prepended with sample_ID.
###########################################################3#################################

cav_flux_2D(setting, expName)
