<<<<<<< HEAD
%%time
import logger as log
from plotter import quad_plot # singleton
import copy
import json

def create_log_file(params):
    """  Create a log file in json using parameters"""
    
    full_file_name = get_full_file_name(params)
    params.full_file_path = os.path.join(params.base_path,full_file_name)    
    
    with open(logFileName, 'w') as f:
        json.dump(vars(params),f,indent=4, sort_keys=True)
    log.info(f'{params.full_file_path} created')
 
def get_full_file_name(params):
    """ Create a full file name with file extension 'dat'.
        File name structure: ID number_Sample ID_Exp name.dat. 
        ex) 1_NbTi_VI.dat
    """
    full_file_name = get_file_ID_number(params) + '_' + params.sample_ID + '_' + params.exp_name + '.dat'
    
    return full_file_name

def get_file_ID_number(params):
    """ Find ID number used to create a full file name. 
        Under base path, search for all ID numbers of files and decide
        what ID to be used next
        Args: 
            params: instance of Params class
        Return: next ID number in str to be used
        """
    ID_numbers = []
    for (root,dirs,files) in os.walk(params.base_path, topdown=True):
        
        for file in files:
            matchobj = re.match(r'^\d+', file)
            if matchobj:
                ID_numbers.append(int(matchobj.group()))    
    if ID_numbers:
        return str(np.max(ID_numbers) + 1)
    else:
        return str(1)

       json.dump(para,f,indent=4, sort_keys=True)
    
class Parameters:
    """ Placehoder for parameters """

def PNA_configure(**kwargs):
    for k,v in kwargs:
        try:
            setattr(self, k, v)
        except AttributeError:
            print(f'method named '{k}' does not exist. Check instrument driver')
            continue
 
def linear_to_dB(S21_linear):
    dB = 20 * np.log10(np.absolute(S21_linear))
    return dB

def find_res_freq(freqs, S21):
    '''
    Fit with lorentzian 
    Args:
        freqs: numpy array of frequencies
        S21: numpy arrary of S21 in complex
    Return:  resonance frequency
    '''
    pass

def plot_data(quad_plotter, plot_type):
    fig, ax = plt.subplots(1,1)
    if plot_type = 'amp':
        ax = copy.deepcopy(quad_plotter.axes_amp)
    elif plot_type = 'phase':
        ax = copy.deepcopy(quad_plotter.axes_phase)
    elif plot_type = 'real':
        ax = copy.deepcopy(quad_plotter.axes_real)
    elif plot_type = 'imag':
        ax = copy.deepcopy(quad_plotter.axes_imag)
        

############################ Set parameters ################################################
PNA_GPIB = 2
SIM_GPIB = 5

params = Parameters()

# PNA
params.pna = Agilent.Agilent(PNA_GPIB)
params.freq_start, params.freq_end = 4.5e9, 5.1e9
params.num_points = 801
params.avg = 1
params.IF_start = 100
params.IF_end = 2000

# flux params
params.flux = SIM.SIM(SIM_GPIB, ch=1) # or put None if SIM is not used.
params.flux_init = 0
params.flux_final = 0

# sweep params
params.power_start = -80
params.power_end = -20
params.power_step = 1

# file params
params.base_path = ''
params.sample_ID = 'WiscCST'
params.exp_name = 'Cav_vs_P_2D'

# plot
params.plot_type = 'amp' # 'amp', 'phase', 'real', 'imag'
###########################################################3#################################

create_log_file(params)

# plotobj= plotter.PNAplot(xlabel='Power (dBm)'
#                           , ylabel = 'Frequency(Hz)'
#                           , title = params.full_file_path.replace('.dat',''))
quad_plotter.initialze(plot_dim=2
                        , xlabel='Power (dBm)'
                        , ylabel='Frequency (Hz)'
                        , title=get_full_file_name(params))

# initialize instruments
pna.setupMeas()
pna.setSweepType('linear')
pna.setFreqStartEnd(params.freq_start, params.freq_end)
pna.avgCount(params.avg)
pna.numPoints(params.num_points)
pna.setIF(params.IF)

if params.flux is not None:
    params.flux.setVoltage(parama.flux.flux_init)

# sweep
powers = np.arange(params.power_start, params.power_end + params.power_step, params.power_step): # traverse in [pmin, pmax].
IFBandwiths = np.linspace(params.IF_start, params.IF_end, len(params.powers)) # IFbandwidth scales up linearly

data = None

for pwr, IF in zip(powers, IFBandwiths):
    # configure
    pna.setIF(IF)
    pna.setPwr(pwr)
    pna.avgClear()
    
    freq, S21 = pna.getData(cplx=True) # S21 in linear scale

    if data is not None:
        data = np.column_stack((data, S21))
    else:
        data = S21
    
    # plot update
    # extent = [params.power_start, pwr, params.freq_start, params.freq_end]
    # plotobj.update(data, extent)
    quad_plotter.update(x_axis=powers, y_axis=freq
                        , amp=np.abs(data), phase=np.angle(data, deg=True), real=data.real, imag=data.imag)

    # save data in each iteration
    with open(params.full_file_path,'wb') as f:
        np.savetxt(f, data, delimiter=',',fmt='%.9e')

# Post measurement
if params.flux is not None:
        params.flux.setVolage(parama.flux.flux_final)

plotobj = plot_data(quad_plotter, plot_type='amp')
fig_full_file_path = params.full_file_path.replace('dat','png')
plotobj.fig.savefig(fig_full_file_path)
log.info('Measurement complete!!!')

=======
%%time
import logger as log
from plotter import quad_plot # singleton
import copy
import json

def create_log_file(params):
    """  Create a log file in json using parameters"""
    
    full_file_name = get_full_file_name(params)
    params.full_file_path = os.path.join(params.base_path,full_file_name)    
    
    with open(logFileName, 'w') as f:
        json.dump(vars(params),f,indent=4, sort_keys=True)
    log.info(f'{params.full_file_path} created')
 
def get_full_file_name(params):
    """ Create a full file name with file extension 'dat'.
        File name structure: ID number_Sample ID_Exp name.dat. 
        ex) 1_NbTi_VI.dat
    """
    full_file_name = get_file_ID_number(params) + '_' + params.sample_ID + '_' + params.exp_name + '.dat'
    
    return full_file_name

def get_file_ID_number(params):
    """ Find ID number used to create a full file name. 
        Under base path, search for all ID numbers of files and decide
        what ID to be used next
        Args: 
            params: instance of Params class
        Return: next ID number in str to be used
        """
    ID_numbers = []
    for (root,dirs,files) in os.walk(params.base_path, topdown=True):
        
        for file in files:
            matchobj = re.match(r'^\d+', file)
            if matchobj:
                ID_numbers.append(int(matchobj.group()))    
    if ID_numbers:
        return str(np.max(ID_numbers) + 1)
    else:
        return str(1)

       json.dump(para,f,indent=4, sort_keys=True)
    
class Parameters:
    """ Placehoder for parameters """

def PNA_configure(**kwargs):
    for k,v in kwargs:
        try:
            setattr(self, k, v)
        except AttributeError:
            print(f'method named '{k}' does not exist. Check instrument driver')
            continue
 
def linear_to_dB(S21_linear):
    dB = 20 * np.log10(np.absolute(S21_linear))
    return dB

def find_res_freq(freqs, S21):
    '''
    Fit with lorentzian 
    Args:
        freqs: numpy array of frequencies
        S21: numpy arrary of S21 in complex
    Return:  resonance frequency
    '''
    pass

############################ Set parameters ################################################
PNA_GPIB = 2
SIM_GPIB = 5

params = Parameters()

# PNA
params.pna = Agilent.Agilent(PNA_GPIB)
params.freq_start, params.freq_end = 4.5e9, 5.1e9
params.num_points = 801
params.avg = 1
params.IF_start = 100
params.IF_end = 2000

# flux params
params.flux = SIM.SIM(SIM_GPIB, ch=1) # or put None if SIM is not used.
params.flux_init = 0
params.flux_final = 0

# sweep params
params.power_start = -80
params.power_end = -20
params.power_step = 1

# file params
params.base_path = ''
params.sample_ID = 'WiscCST'
params.exp_name = 'Cav_vs_P_2D'

# plot
params.plot_type = 'amp' # 'amp', 'phase', 'real', 'imag'
###########################################################3#################################

create_log_file(params)

# plotobj= plotter.PNAplot(xlabel='Power (dBm)'
#                           , ylabel = 'Frequency(Hz)'
#                           , title = params.full_file_path.replace('.dat',''))
quad_plotter.initialze(plot_dim=2
                        , xlabel='Power (dBm)'
                        , ylabel='Frequency (Hz)'
                        , title=get_full_file_name(params))

# initialize instruments
pna.setupMeas()
pna.setSweepType('linear')
pna.setFreqStartEnd(params.freq_start, params.freq_end)
pna.avgCount(params.avg)
pna.numPoints(params.num_points)
pna.setIF(params.IF)

if params.flux is not None:
    params.flux.setVoltage(parama.flux.flux_init)

# sweep
powers = np.arange(params.power_start, params.power_end + params.power_step, params.power_step): # traverse in [pmin, pmax].
IFBandwiths = np.linspace(params.IF_start, params.IF_end, len(params.powers)) # IFbandwidth scales up linearly

data = None

for pwr, IF in zip(powers, IFBandwiths):
    # configure
    pna.setIF(IF)
    pna.setPwr(pwr)
    pna.avgClear()
    
    freq, S21 = pna.getData(cplx=True) # S21 in linear scale

    if data is not None:
        data = np.column_stack((data, S21))
    else:
        data = S21
    
    # plot update
    # extent = [params.power_start, pwr, params.freq_start, params.freq_end]
    # plotobj.update(data, extent)
    quad_plotter.update(x_axis=powers, y_axis=freq
                        , amp=np.abs(data), phase=np.angle(data, deg=True), real=data.real, imag=data.imag)

    # save data in each iteration
    with open(params.full_file_path,'wb') as f:
        np.savetxt(f, data, delimiter=',',fmt='%.9e')

# Post measurement
if params.flux is not None:
        params.flux.setVolage(parama.flux.flux_final)

fig_full_file_path = params.full_file_path.replace('dat','png')
quad_plotter.fig.savefig(fig_full_file_path)
log.info('Measurement complete!!!')

>>>>>>> 76acf166fada59a6cf887bbada085ed923f56f58
