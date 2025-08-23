import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import math as M 


def value_print_block():
    print("\n\n")

def value_printer(sentance, value, unit: str = None, floating: int = None) -> None:

    if floating is None:
        floating = 2

    if unit is None:
        unit = " "

    message = f"~~ {sentance}: {floating:.2f} {unit}"
    print(message)
    
    
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
                 feedback_top_resistor: float, load_current_limit: float):
        
        self.switching_frequency = switching_freq
        self.soft_start_time = soft_start_time
        self.input_voltage = input_voltages
        self.output_voltage = output_voltage
        self.ripple_current_ratio = ripple_current_ratio
        self.feedback_top_resistance = feedback_top_resistor
        self.load_current_limit = load_current_limit


        self.approx_on_time = None
        self.max_duty_cycle = None 
        self.soft_start_capacitance = None 
        self.feedback_bottom_resistance = None
        self.current_limit_external_resistance = None
        self.inductor_ripple_current = None
         

    def feedback_bottom_resistor(self, print_val = None):
        
        self.feedback_bottom_resistance = (MIC28516.feedback_referance_voltage_internal * self.feedback_top_resistance) / (self.output_voltage - MIC28516.feedback_referance_voltage_internal)
        
        if print_val:
            value_printer("Feedback bottom resistor value", self.feedback_bottom_resistance, "ohm")

    def soft_start_capacitor(self, print_val = None):
        self.soft_start_capacitance = (MIC28516.internal_soft_start_current * self.soft_start_time) / MIC28516.feedback_referance_voltage

        if print_val:
            value_printer("Soft start capacitance", self.soft_start_capacitance, "nF")

    def maximum_duty_cycle(self):
        self.max_duty_cycle = 1 - (MIC28516.min_on_time * self.switching_frequency)


    def source_current_limit_resistor(self, print_val = None):

        self.current_limit_external_resistance = (self.load_current_limit + (self.inductor_ripple_current / 2)) * MIC28516.internal_low_side_mosfet_rds / MIC28516.current_limit_pin_output_current

        if print_val:
            value_printer("Current Limit Resistor", self.current_limit_external_resistance, "nF")

    
    def run_calcs(self):
        self.source_current_limit_resistor()
        








def test_1():
    fsw = 300e3
    vin = [48]
    vout = 12 
    tss = 30e-3
    ripple_ratio = 0.2
    fb_rtop = 10000
    Ilim = 8
    buck_1 = MIC28516(fsw, vin, vout, tss, ripple_ratio, fb_rtop, Ilim)
    buck_1.feedback_bottom_resistor()
    buck_1.soft_start_capacitor(print_val = True)
    buck_1.source_current_limit_resistor(print_val = True)




def main():
    test_1()



if __name__ == "__main__":
    main()

    

    
         


    




#     def time_on_estimate(self, Vout, Vin, fsw):
#         return Vout / (Vin * fsw)


#     def max_duty_cycle_1(self, fsw):
#         return 1 - (MIN_ON_TIME * fsw)
    


#     # Run all the calculations: 
#     def run_calculations(self):
#         pass
        



# switching_frequency = 300e3
# MIN_ON_TIME = 240e-9
# RDS_LOW_SIDE_MOSFET = 18e-3
# ADJUSTED_FSW = 800e3 
# INERTAL_SS_CURRENT = 1.4e-6
# soft_start_time = 50e-3
# VREF = 0.6
# V_INTERNAL_FB_VOLTAGE = 0.6 
# selected_output_voltage = 12
# inductor_ripple_current = None
# CURRENT_LIMIT_SOURCE_CURRENT = 96e-6
# load_current_limit = None
# AC_RIPPLE_CURRENT_TO_DC_RATIO = 0.2

