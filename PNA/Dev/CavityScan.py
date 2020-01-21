%%time

class PNA_ExpManager(object):
    '''
    Base class for experiment with PNA
    '''

    def __init__(self, expSettings):
        self.expSettings = expSettings
        self.sweeper = None
        self.pna = None
        self.plotter = None
        self.fileHandler = None

    def init(self):

    def run(self):
        for itr in self.sweeper:
            freq, S21 = self.pna.getdata()
            self.plotter.update()

    def cleanup(self):
        pass

def PNA_ExpScripter(expName, expSettings):

    ##### Set up  measurement #############
    exp = PNA_ExpManager(expSettings)  # instantiate class

    # Add file hander
    exp.addFileHandler()

    # Add PNA and/or others
    exp.createPNA(self.expSettings['pnaSettings'])

    # Add Sweeper
    exp.createSweeper(self.expSettings['sweepSettings'])

    # Add Plotter
    exp.plotter =  createPlotter()

    #### Initialize measurement and run it ####
    exp.init()
    exp.run()
    exp.post_job()

pna = PNA(18)
sim = SIM.SIM(15, channel=2)

expSettings = { 'pnaSettings' :
                { 'sweepType':sweepType,
                'startFreq': startFreq,
                'endFreq': endFreq,
                'numPoints': numPoints,
                'avg': avg,
                'IF': IF,
                },
               'sweepSettings':
                { 'start': start,
                  'end': end,
                  'step': step,
                  'instr': inst,
                  'setFunc': setFunc
                  }
               }


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


def findResFreq(freqs, S21s):
    '''
    freqs: numpy array of frequencies
    S21s: numpy arrary of S21 in complex
    Return:  resonance frequency
    '''
    pass


def create_logfile(pnaSettings, sweepSettings, fileSettings, *args):
    # dictionary for parameters to be saved in json file. Solely for log.

    timeStr = time.strftime("%H%M%S")

    baseStr = sampleID + '_'+'S21vsFvsP_fr{:.9g}_{:.9g}_Pr{:.4g}_{:.4g}_{:.4g}_V{:.3g}_T{:.4g}_{}_{}'
    baseFileName = baseStr.format(startFreq/1e9, endFreq/1e9, startPwr, endPwr, stepPwr, Vglb_init, FAA, suffix, timeStr)
    dataFileName_mag, dataFileName_phase  = (os.path.join(save_path, baseFileName + '_mag.dat'),
                                         os.path.join(save_path, baseFileName + '_phase.dat'))
    print('filename={}'.format(os.path.join(save_path, baseFileName + '_mag.dat')))


    logFileName =  os.path.join(fileSettings.save_path, fileSettings.fileName + '.json')

    with open(logFileName, 'w') as f:
        json.dump(para,f,indent=4, sort_keys=True)



############################################################################################
class FileHandler(object):
    def __init__(self, setting):
        self.setting = setting

        self.create_log_file()

    def defineDataFormat(self):
        pass

    def create_log_file(self):
        file_name = FileNameFormatter(setting)
        logFileName =  os.path.join(self.setting.save_path, self.setting.fileName + '.json')

        with open(logFileName, 'w') as f:
            json.dump(para, f, indent=4, sort_keys=True)

    def updateDataFile(self):
        with  open(dataFileName_mag, 'wb') as f_mag:
            np.savetxt(f_mag, S21_mag_log_2D, fmt='%.9g', delimiter='\t')

        with open(dataFileName_phase, 'wb') as f_phase:
            np.savetxt(f_phase, S21_phase_2D, fmt='%.9g', delimiter='\t')

class FileNameFormatter(object):
    # Here is allowed format style

    def __init__(self, setting, format=None):
        self.setting = setting
        self.format = format

class DataHandler(object):
    """
        data attribute stores S21 data during sweep.
    """
    def __init__(self):
        self.data = None   # 1D or 2D array of S21
        self._data_dB = None
        self._data_real = None
        self._data_imag = None
        self._data_angle = None

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

    def update(self, S21):
        if self.data is None:
            self.data = S21
        else:
            self.data = np.vstack(self.data, S21)  # append to axis=0 direction


class Setting(object):
    pass  # placehoder for setting parameters

############################ Set parameters ################################################

setting = Setting()

# PNA setting
setting.start_freq, setting.end_freq = 4.5e9, 5.1e9
setting.num_points = 801
setting.avg = 1
setting.IF_start = 100
setting.IF_end = 2000

# flux Setting
setting.flux_init = 0
setting.flux_end =0

# sweep Setting: specify
setting.sweep_start, setting.sweep_end, setting.sweep_step =  -80, -20, 1

# file Setting
setting.save_path = ''
setting.sampleID = 'WiscCST'
setting.suffix = ''
###########################################################3#################################

# instrument setting
pna = PNA_Factory(16)
flux = SIM(18, channel=2)

## data DataHandler
dataobj = DataHandler(dim=2)  # dimension of S21 date collected.

# log and data file
baseStr = sampleID + '_'+'S21vsFvsP_fr{:.9g}_{:.9g}_Pr{:.4g}_{:.4g}_{:.4g}_V{:.3g}_T{:.4g}_{}_{}'
baseFileName = baseStr.format(startFreq/1e9, endFreq/1e9, startPwr, endPwr, stepPwr, Vglb_init, FAA, suffix, timeStr)
filename = f'{sampleID}_S21vsFvsP'
fileobj = FileHandler(setting, file_name_formatter)

# plot setup
plotobj= myplots_py3.plot2D(ylabel = 'Frequency(Hz)', xlabel='Power (dBm)', title = fileobj.base_file_name)

# initialize instruments
pna.configure(sweepTyep='linear', startFreq=setting.start_freq, endFreq=setting.end_freq
            , avg=setting.avg, numPoints=setting.num_points)
pna.pwrOn()
flux.setVolage(setting.flux_init)

# sweep
powers = np.arange(setting.sweep_start, setting.sweep_end + setting.sweep_step, setting.sweep_step): # traverse in [pmin, pmax].
IFBandwiths = np.linspace(setting.IF_start, setting.IF_end, len(setting.powers)) # IFbandwidth scales up linearly

# S21_mag_log_2D, S21_phase_2D = np.array([]), np.array([])

for pwr, IFBW in zip(powers, IFBandwiths):

   # clear_output()
    print('startPwr={:.3g} dBm, endPwr={:.3g} dBm, current power={:.3g} dBm'.format(startPwr, endPwr, pwr))

    # configure
    pna.setIF(IFBW)
    pna.setPwr(pwr)
    pna.avgClear()

    # fetch data from PNA
    freq, S21 = pna.getData(cplx=True) # S21 in linear scale

    # data update
    dataobj.update(S21)

    # plot update
    extent = [setting.sweep_start, pwr, setting.start_freq, setting.end_freq]
    plotobj.update(dataobj.data_dB, extent)

    # save data in each iteration
    fileobj.updateDataFile(dataobj.data)

# Post measurement
pna.setPwr(-70)
pna.pwrOff()
flux.setVoltage(setting.flux_final)

plotobj.fig.savefig(os.path.join(setting.save_path, setting.base_file_name + '.png'))
print('Measurement complete!!!')
