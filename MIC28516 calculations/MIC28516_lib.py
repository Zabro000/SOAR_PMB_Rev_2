import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 


class MIC28516():
    feedback_referance_voltage = 0.6
    feedback_referance_voltage_internal = 0.6
    min_on_time = 240e-9
    current_limit_source_current = 96e-6
    current_limit_pin_output_current = 96e-6
    internal_low_side_mosfet_rds = 18e-3
    internal_soft_start_current = 1.4e-6
    fundimental_switching_frequency_fo = 800e3


    def __init__(self, switching_freq: float, input_voltages: list, output_voltage: float, soft_start_time: float, ripple_current_ratio: float,
                 feedback_top_resistor):
        self.switching_frequency = switching_freq
        self.soft_start = soft_start_time
        self.input_voltage = input_voltages
        self.output_voltage = output_voltage
        self.ripple_current_ratio = ripple_current_ratio
        self.feedback_top_resistance = feedback_top_resistor


        self.approx_on_time = None
        self.max_duty_cycle = None 
        self.soft_start_capacitor_value = None 
         


        
    def time_on_estimate(Vout, Vin, fsw):
        return Vout / (Vin * fsw)


    def max_duty_cycle(fsw):
        return 1 - (MIN_ON_TIME * fsw)
    


    # Run all the calculations: 
    def run_calculations(self):
        pass
        



switching_frequency = 300e3
MIN_ON_TIME = 240e-9
RDS_LOW_SIDE_MOSFET = 18e-3
ADJUSTED_FSW = 800e3 
INERTAL_SS_CURRENT = 1.4e-6
soft_start_time = 50e-3
VREF = 0.6
V_INTERNAL_FB_VOLTAGE = 0.6 
selected_output_voltage = 12
inductor_ripple_current = None
CURRENT_LIMIT_SOURCE_CURRENT = 96e-6
load_current_limit = None
AC_RIPPLE_CURRENT_TO_DC_RATIO = 0.2

