import numpy as np
import matplotlib.pyplot as plt
import pyvisa

rm = pyvisa.ResourceManager()

def get_vna_config(vna_address):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    start_freq = vna.query('SENS:FREQ:STAR?') # Get the start frequency
    stop_freq = vna.query('SENS:FREQ:STOP?') # Get the stop frequency
    num_points = vna.query(':SENS:SWE:POIN?') # Get the number of points
    if_bandwidth = vna.query(':SENS:BAND?') # Get the if-bandwidth
    power = vna.query(':SOUR:POW?') # Get power level
    vna.close()

    vna_config = list(map(float, [start_freq, stop_freq, num_points, if_bandwidth, power]))
    return vna_config
    
def config_num_points(vna_address, num_points):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.write(f':SENS:SWE:POIN {num_points}') # Set the number of points
    vna.close()

def config_start_stop_freq(vna_address, start_freq, stop_freq):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.write(f'SENS:FREQ:STAR {start_freq}') # Set the start frequency
    vna.write(f'SENS:FREQ:STOP {stop_freq}') # Set the stop frequency
    vna.close()

def config_center_span_freq(vna_address, center_freq, span_freq):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.write(f'SENS:FREQ:CENT {center_freq}') # Set the center frequency
    vna.write(f'SENS:FREQ:SPAN {span}') # Set the span
    vna.close()

def config_if_bandwidth(vna_address, if_bandwidth):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.write(f':SENS:SWE:POIN {num_points}') # Set the number of points
    vna.write(f':SENS:BAND {if_bandwidth}') # Set the if-bandwidth
    vna.close()

def config_power(vna_address, power):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.write(f':SOUR:POW:PORT:COUP ON')
    vna.write(f':SOUR:POW {power}') # Set the power level
    vna.close()

def config_s(vna_address, s, s_format):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.timeout = 20000  # Set timeout to 20 seconds
    vna.write(f':CALC:PAR:DEF {s}') # Set the VNA to measure {S11, S12, S21, S22}
    vna.write(f':CALC:FORM {s_format}') # Set data format to {MLOG, MLIN, PHAS, PLOG, PLIN, REAL, IMAG}
    vna.close()

def config_s_format(vna_address, s_format):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.timeout = 20000  # Set timeout to 20 seconds
    vna.write(f':CALC:FORM {s_format}') # Set data format to {MLOG, MLIN, PHAS, PLOG, PLIN, REAL, IMAG}
    vna.close()

def config_vna(vna_address, s, s_format, num_points, if_bandwidth):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.timeout = 300000  # Set timeout to 5 mins
    vna.write(f':CALC:PAR:DEF {s}') # Set the VNA to measure {S11, S12, S21, S22}
    vna.write(f':CALC:FORM {s_format}') # Set data format to {MLOG, MLIN, PHAS, PLOG, PLIN, REAL, IMAG}
                                        # MLOG: log magnitude, MLIN: linear magnitdue, PHAS: phase
                                        # PLOG: log magnitude & phase, PLIN: linear magnitude & phase
    vna.write(f':SENS:SWE:POIN {num_points}') # Set the number of points
    vna.write(f':SENS:BAND {if_bandwidth}') # Set the if-bandwidth
    vna.close()

def autoscale_vna(vna_address):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.write(':DISP:WIND:TRAC:Y:AUTO')
    vna.close()
    
def measure_s(vna_address):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.timeout = 300000  # Set timeout to 20 seconds
    
    # Measure
    vna.write(':INIT:CONT ON') # Turn continuous trigger on
    vna.write(':TRIG:SOUR BUS') # Change trigger source to BUS
    vna.write('TRIG:SING') # Initiate a single trigger
    vna.query('*OPC?') # Wait for the measurement to complete
    vna.write(':INIT:CONT OFF') # Turn continuous trigger off
    vna.write(':TRIG:SOUR INT') # Change trigger source to internal

    # Get frequency data
    freq_data = vna.query('SENS:FREQ:DATA?')
    frequencies = np.array([float(x) for x in freq_data.split(',')])

    # Get S-parameter data
    s_data = vna.query('CALC:DATA:FDATA?')
    s_data = np.array([float(x) for x in s_data.split(',')])
    s_data_1 = s_data[::2]
    s_data_2 = s_data[1::2]

    vna.close()

    return frequencies, s_data_1, s_data_2

def measure_s_ss(vna_address, start_freq, stop_freq):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.timeout = 300000  # Set timeout to 20 seconds
    vna.write(f'SENS:FREQ:STAR {start_freq}') # Set the start frequency
    vna.write(f'SENS:FREQ:STOP {stop_freq}') # Set the stop frequency 
    
    # Measure
    vna.write(':INIT:CONT ON') # Turn continuous trigger on
    vna.write(':TRIG:SOUR BUS') # Change trigger source to BUS
    vna.write('TRIG:SING') # Initiate a single trigger
    vna.query('*OPC?') # Wait for the measurement to complete
    vna.write(':INIT:CONT OFF') # Turn continuous trigger off
    vna.write(':TRIG:SOUR INT') # Change trigger source to internal

    # Get frequency data
    freq_data = vna.query('SENS:FREQ:DATA?')
    frequencies = np.array([float(x) for x in freq_data.split(',')])

    # Get S-parameter data
    s_data = vna.query('CALC:DATA:FDATA?')
    s_data = np.array([float(x) for x in s_data.split(',')])
    s_data_1 = s_data[::2]
    s_data_2 = s_data[1::2]

    vna.close()

    return frequencies, s_data_1, s_data_2

def measure_s_cs(vna_address, center_freq, span):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.timeout = 300000  # Set timeout to 20 seconds
    vna.write(f'SENS:FREQ:CENT {center_freq}') # Set the center frequency
    vna.write(f'SENS:FREQ:SPAN {span}') # Set the span
    
    # Measure
    vna.write(':INIT:CONT ON') # Turn continuous trigger on
    vna.write(':TRIG:SOUR BUS') # Change trigger source to BUS
    vna.write('TRIG:SING') # Initiate a single trigger
    vna.query('*OPC?') # Wait for the measurement to complete
    vna.write(':INIT:CONT OFF') # Turn continuous trigger off
    vna.write(':TRIG:SOUR INT') # Change trigger source to internal

    # Get frequency data
    freq_data = vna.query('SENS:FREQ:DATA?')
    frequencies = np.array([float(x) for x in freq_data.split(',')])

    # Get S-parameter data
    s_data = vna.query('CALC:DATA:FDATA?')
    s_data = np.array([float(x) for x in s_data.split(',')])
    s_data_1 = s_data[::2]
    s_data_2 = s_data[1::2]

    vna.close()

    return frequencies, s_data_1, s_data_2
    
def measure_sx(vna_address, s, center_freq, span):
    vna = rm.open_resource(vna_address)  # Open a connection to the VNA
    vna.timeout = 20000  # Set timeout to 20 seconds
    
    vna.write(f':CALC:PAR:DEF {s}') # Set the VNA to measure S12
    vna.write(':CALC:FORM PLOG') # Set data format to log magnitude and phase
    
    vna.write(f'SENS:FREQ:CENT {center_freq}') # Set the center frequency
    vna.write(f'SENS:FREQ:SPAN {span}') # Set the span

    # Measure
    vna.write(':INIT:CONT ON') # Turn continuous trigger on
    vna.write(':TRIG:SOUR BUS') # Change trigger source to BUS
    vna.write('TRIG:SING') # Initiate a single trigger

    vna.query('*OPC?') # Wait for the measurement to complete

    vna.write(':INIT:CONT OFF') # Turn continuous trigger off
    vna.write(':TRIG:SOUR INT') # Change trigger source to internal

    # Get frequency data
    freq_data = vna.query('SENS:FREQ:DATA?')
    frequencies = np.array([float(x) for x in freq_data.split(',')])

    # Get S-parameter data
    s_data = vna.query('CALC:DATA:FDATA?')
    s_data = np.array([float(x) for x in s_data.split(',')])
    s_data_maglog = s_data[::2]
    s_data_phase = s_data[1::2]

    vna.close()

    return frequencies, s_data_maglog, s_data_phase

def plot_s(freq, mag, phase):
    plt.figure()
    
    plt.subplot(2, 1, 1)
    plt.plot(freq/1e9, mag)
    plt.ylabel('Magnitude (dB)')
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(freq/1e9, phase)
    plt.ylabel('Phase (deg)')
    plt.xlabel('Frequency (GHz)')
    plt.grid()

    plt.tight_layout()
    plt.show()

def save_s(freq, mag, phase, save_file):
    all_dat = np.array([freq,mag,phase]).T
    np.savetxt(save_file, all_dat, delimiter = ",")