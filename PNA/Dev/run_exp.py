# Usage in jupyter notebook
# 1) Set parameters
# 2) Run a measurement function, e.g., pnaExp.cav_power_2D(exp_name, params)

import pnaExp

# common parameters
params = pnaExp.Params() # a placeholder object for experiment parameters

# Instruments address
params.PNA_GPIB_ADDR = 0
params.SIM_GPIB_ADDR = 0
params.SIM_SERIAL_PORT = 'COM6'
params.SIM_channels = {'ch'+str(i):i for i in range(1,7)}  # channel dictionary
params.Hittite_GPIB_ADDR = 0

# Define instruments to use
# params.pna = AgilentN5230A.AgilentN5230A(params.PNA_GPIB_ADDR)
# params.SIM1 = SIM.SIM(params.SIM_GPIB_ADDR, params.SIM_channels['ch2'])
# params.SIM2 = SIM.SIM(params.SIM_GPIB_ADDR, params.SIM_channels['ch3'])
# params.Hittite = Hittite.Hittite(params.Hittite_GPIB_ADDR)

params.pna = InstrumentParams(instr_obj=AgilentN5230A.AgilentN5230A(params.PNA_GPIB_ADDR))
params.flux1 = InstrumentParams(instr_obj=SIM.SIM(params.SIM_GPIB_ADDR, params.SIM_channels['ch2']))
params.flux2 = InstrumentParams(instr_obj=SIM.SIM(params.SIM_GPIB_ADDR, params.SIM_channels['ch3']))
params.spec = InstrumentParams(instr_obj=Hittite.Hittite(params.Hittite_GPIB_ADDR))

# File params. file name = ID num + sampleID + exp_name
params.save_base_path = 'z:\User\Jaseung'
params.device_ID = 'WisCST'  # Folder with sample_ID is created under save_path

# end of common block

pna = Instrument(instr, measType='S21', sweeptype='linear',avg=1, IF=50, num_points=101)
flux01 = InstrumentParams(instr, setVoltage=0)
spec = InstrumentParams(instr, power=-20)
exp.add_instrument([pna, flux01, spec])

sweep1 = Sweep(flux1, start=-10, end=0.2, step=0.1, order=1)
sweep2 = SweepParams(flux2, start=-2, end =0.2, step=0.2, order=2)
sweep1 = SweepParams(pna, start=5e9, end=6e9, num_points=101, order=1)
sweep3 = SweepParams(pna, start=-20, end=0, step=1, order=2)
sweep4 = SweepParams(pna, start=100, end=5000, num_points=101, order=2
exp.add_sweep([sweep1, sweep2])


# cav, 1D

# instruments to use
# params.instrument_list = [params.pna, params.flux1]

# pna setting
params.pna.mode = 'linear'  # 'linear' or 'CW'
params.pna.start_freq, params.pna.end_freq = 4.5e9, 5.1e9
params.pna.num_points = 801
params.pna.avg, params.pna.IF = 1, 500

# flux1 setting
params.flux1.voltage = 0


# run measurement
pnaExp.cav_1D(params, 'cav')


# cav_power_2D 

# Set fixed parameters per each instrument
params.pna_start_freq, params.pna_end_freq = 4.5e9, 5.1e9
params.num_points = 801
params.avg, params.IF = 1, 500

params.flux1.voltage = 0

# Sweep params
params.IF_start, params.IF_end = 100, 2000  # linearly scaled
params.sweep1_start, params.sweep1_end, params.sweep1_step =  -80, -20, 1

# run measurement
pnaExp.cav_power_2D(params, 'cav_power_2D')


# cav_flux_2D 

# PNA params
params.pna_start_freq, params.pna_end_freq = 4.5e9, 5.1e9
params.num_points = 801
params.avg, params.IF = 1, 500

# Sweep params
params.sweep1_start, params.sweep1_end, params.sweep1_step =  -2, 2, 0.005

data = pnaExp.cav_flux_2D(params, expName)
