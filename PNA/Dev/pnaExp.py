# pnaExp.py
# Goal: Make it easy and fast to build a type of experiemnt and to run it.
# The idea is to define each function that corresponds to a type of measurement, rather than making
# a generic experiment class like Qlab. The reason is by giving up some abstraction, we want
# to have more flexibility and intuition. Once we make one type of measurement, we rarely change it.
#
import matplotlib.pyplot as plt
import numpy as np
import visa
import os
import re

def list_exp_type():
    """ list all experiment types, i.e., function list """
    pass

def select_params_template(num):
    params = Params()

    return params

def instrument_communication_check():
    pass

class PNA_Factory(AgilentN5230A.AgilentN5230A):
    '''
    This object peforms what we want PNA to do, including basic individual operations provided by instrument driver and
    compositions of operatioins, for example, configure method.
    This class Inherites PNA instrument driver class.
    '''

    def __init__(self, address=address):
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
        Handle 1) a log file which contains parameters from params instance, and 2) a data file.
    """
    def __init__(self, exp_name, params, dataobj):
        self.params = params

        # create a sample_ID folder followed by date folder with yyyy-mm-dd format
        self.sample_ID_folder = os.path.join(self.params.save_base_path, self.params.sample_ID)
        self.date_folder = datatime.datetime.today().strftime('%Y-%m-%d')
        self.full_file_path = os.path.join(self.params.save_base_path, self.params.sample_ID, self.date_folder)

        try:
            os.mkdir(self.sample_ID_folder)
        except FileExistsError:
            pass

        try:
            os.mkdir(sel.full_file_path)
        except FileExistsError:
            pass

        self.file_ID_num = self.get_file_ID_num() # start from 1
        self.base_file_name = '_'.join([self.file_ID_num, params.sample_ID, self.exp_name])
        self.log_file_name = self.base_file_name + '.json'
        self.data_file_name = self.base_file_name + '.dat'

    def get_file_ID_num(self):
        IDs = []
        for (root,dirs,files) in os.walk(self.sample_ID_folder, topdown=true):
            matchobj = re.match(r'^\d+', files)
            IDs.append(int(matchobj.group()))

        return str(np.max(IDs) + 1)

    def create_log_file(self):
        # file_name = FileNameFormatter(params)
        full_log_file_path =  os.path.join(self.params.save_base_path
                                        , self.params.sample_ID
                                        , self.folder_date
                                        , self.log_file_name )

        with open(full_log_file_path, 'w') as f:
            json.dump(self.to_dict(self.params), f, indent=4, sort_keys=True)

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

class DataHandler(object):
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

class Params(object):
    """
    A container for parameters. Data structure..
    """

    allowed_attributes = {
    'CW_freq', 'power' 'num_points','avg', 'IF'
    ,'flux_volt'
    , 'sweep1_start', 'sweep1_end', 'sweep1_step'
    , 'sweep2_start', 'sweep2_end', 'sweep2_step'
    , 'sweep3_start', 'sweep3_end', 'sweep3_step'
    , 'save_path', 'sample_ID', 'suffix'
    }
    def __init__(self, instr_params, sweep_params):
        self.instr_params = instr_params
        self.sweep_params = sweep_params

class InstrumentParams(object):
    """
    Args:
    instr: instrument driver object
    setter_value : a dictionary of set method and value
    """
    def __init__(self, instr, setter_value ):
        self.instr = instr
        self.setter_value = setter_value

class SweepParams:
    def __init__(self, instr_obj, start=None, end=None, step=None, num_points=None, order=1):
        self.instr_obj = instr_obj
        self.start = start
        self.end = end
        self.step = step
        self.num_points = num_points
        self.order = order


class ExpManager:
    def add_sweep(self, sweep_list):
        for sweep in sweep_list:
            self.sweep.append(sweep)
    def run(self):
        
def initialize_instrument(params):
    for p in params:
        if isinstance(p, InstrumentParams):
            p.initialize()

def cav_1D(params):
    pass

def expScripter(params, exp_name):

    ## data DataHandler
    dataobj = DataHandler()  # store data in dataobj

    # log and data file
    fileobj = FileHandler(exp_name, params, dataobj)  # pass params parameters and data.

    # plot setup
    title = fileobj.base_file_name
    plotobj= Plotter.Plot2D_1sub(xlabel='Power (dBm)', ylabel='Frequency(Hz)', title=title)

    # initialize instruments
    initialize_instrument(params)

    # define sweep
    sweep1_values = np.arange(params.sweep1_start, params.sweep1_end + params.sweep1_step, params.sweep1_step) # traverse in [pmin, pmax].
    IF_bandwidths = np.linspace(params.IF_start, params.IF_end, len(sweep1_values)) # IFbandwidth scales up linearly

    for pwr, IFBW in zip(sweep1_values, IF_bandwidths):
        clear_output()
        print(f'startPwr={params.sweep1_start:.3g} dBm, endPwr={params.sweep1_end:.3g} dBm, current power={pwr:.3g} dBm')

        # configure
        params.pna.setIF(IFBW)
        params.pna.setPwr(pwr)
        params.pna.avgClear()

        # fetch data from PNA
        freq, S21 = params.pna.getData(cplx=True) # S21 in linear scale

        # data update
        dataobj.update(S21) # For 2D data

        # plot update
        extent = [params.sweep1_start, pwr, params.pna_start_freq, params.pna_end_freq]
        plotobj.update(dataobj.data_dB, extent)

        # save data in each iteration
        fileobj.update_data_file()

    # Post measurement
    params.pna.setPwr(-90)
    params.pna.pwrOff()

    plotobj.savefig()
    # fig.savefig(os.path.join(fileobj.full_file_path, fileobj.base_file_name + '.png'))
    print('Measurement complete!!!')

def cav_power_2D(params):

    ## data DataHandler
    dataobj = DataHandler()  # store data in dataobj

    # log and data file
    fileobj = FileHandler(exp_name, params, dataobj)  # pass params parameters and data.

    # plot setup
    title = fileobj.base_file_name
    plotobj= Plotter.Plot2D_1sub(xlabel='Power (dBm)', ylabel='Frequency(Hz)'
                                , title=title)

    # initialize instruments
    params.pna.configure(sweepTyep='linear'
                , startFreq=params.pna_start_freq
                , endFreq=params.pna_end_freq
                , avg=params.avg
                , numPoints=params.num_points)
    params.pna.pwrOn()

    for param in dir(params):
        if isinstance(param, InstrumentParams):
            params.flux1.setVolage(params.flux1.voltage)

    # define sweep
    sweep1_values = np.arange(params.sweep1_start, params.sweep1_end + params.sweep1_step, params.sweep1_step) # traverse in [pmin, pmax].
    IF_bandwidths = np.linspace(params.IF_start, params.IF_end, len(sweep1_values)) # IFbandwidth scales up linearly

    for pwr, IFBW in zip(sweep1_values, IF_bandwidths):
        clear_output()
        print(f'startPwr={params.sweep1_start:.3g} dBm, endPwr={params.sweep1_end:.3g} dBm, current power={pwr:.3g} dBm')

        # configure
        params.pna.setIF(IFBW)
        params.pna.setPwr(pwr)
        params.pna.avgClear()

        # fetch data from PNA
        freq, S21 = params.pna.getData(cplx=True) # S21 in linear scale

        # data update
        dataobj.update(S21) # For 2D data
        # dataobj.update(S21, spec_freq) # For 1D data like 1D spec.

        # plot update
        extent = [params.sweep1_start, pwr, params.pna_start_freq, params.pna_end_freq]
        plotobj.update(dataobj.data_dB, extent)

        # save data in each iteration
        fileobj.update_data_file()

    # Post measurement
    params.pna.setPwr(-90)
    params.pna.pwrOff()

    plotobj.savefig()
    # fig.savefig(os.path.join(fileobj.full_file_path, fileobj.base_file_name + '.png'))
    print('Measurement complete!!!')

    return dataobj

def cav_flux_2D(params):

    # instrument params
    pna = AgilentN5230A.AgilentN5230A(params.PNA_GPIB_ADDR)
    if  hasattr(params, 'flux_volt'):
        flux_instr = []
        for i in params.flux_volt:
            flux_instr.append( SIM.SIM(params.SIM_GPIB_ADDR, channel=params.SIM_channels[i]) )

    ## data DataHandler
    dataobj = DataHandler()  # measured data stores in dataobj
    # log and data file
    fileobj = FileHandler(exp_name, params, dataobj)  # pass params parameters and data.
    # plot setup
    plotobj= Plotter.Plot2D_1sub(xlabel='Flux (V)', ylabel = 'Frequency (Hz)', title = fileobj.base_file_name)

    # initialize instruments
    params.pna.configure(sweepTyep='linear', startFreq=params.pna_start_freq, endFreq=params.pna_end_freq
                , avg=params.avg, numPoints=params.num_points, IF=params.IF)
    params.pna.pwrOn()

    # sweep
    sweep1_values = np.arange(params.sweep1_start, params.sweep1_end + params.sweep1_step, params.sweep1_step): # traverse in [pmin, pmax].

    for val in sweep1_values:

        # configure
        params.flux.setVolage(val)
        params.pna.avgClear()

        # fetch data from PNA
        freq, S21 = pna.getData(cplx=True) # S21 in linear scale

        # data update
        dataobj.update(S21) # For 2D data
        # dataobj.update(S21, spec_freq) # For 1D data like 1D spec.

        # plot update
        extent = [params.sweep1_start, pwr, params.pna_start_freq, params.pna_end_freq]
        plotobj.update(dataobj.data_dB, extent)

        # save data in each iteration
        fileobj.update_data_file()

    # Post measurement
    params.pna.pwrOff()
    plotobj.fig.savefig(os.path.join(fileobj.full_file_path, fileobj.base_file_name + '.png'))
    print('Measurement complete!!!')

def cav_flux1_flux2_2D():
    """ Cavity scan with two flux axis."""
    pass

def spec_1D():
    """ Qubit spectroscopy 1D """
    pass

def spec_power_2D():
    """ Spectrosocpy vs power, 2D """
    pass

def spec_flux_2D():
    """ Spectroscopy vs flux, 2D. Cavity frequency is retuned per flux point. """
    pass

def cav_flux_1D():
    pass


def cav_scan(pna, start_freq, end_freq, num_points, avg, IF):
    """ Run 1D cavity scan to find a new resonant frequency.
        Args:
        Return: freq, S21
    """
    pna.configure(sweepTyep='linear'
                , start_freq=start_freq
                , end_freq=end_freq
                , avg=avg
                , num_points=num_points)

    freq, S21 = pna.getData(cplx=True)

    return freq, S21
