import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import math as M 


def value_print_block():
    print()

def value_printer(sentance, value, unit: str = None, floating: int = None) -> None:

    if floating is None:
        floating = 2

    if unit is None:
        unit = " "

    message = f"~ {sentance}: {value:.3e} {unit}"
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
    maximum_output_current = 8 


    def __init__(self, switching_freq: float, input_voltage: float, output_voltage: float, soft_start_time: float, ripple_current_ratio: float,
                 feedback_top_resistor: float, load_current_limit: float, feedforward_capacitor: float = None,
                 ripple_injection_resistor: float = None, ripple_injection_capacitor: float = None, output_capacitance: float = None,
                 output_capacitance_esr: float = None):
        
        self.switching_frequency = switching_freq
        self.soft_start_time = soft_start_time
        self.input_voltage = input_voltage
        self.output_voltage = output_voltage
        self.ripple_current_ratio = ripple_current_ratio
        self.feedback_top_resistance = feedback_top_resistor
        self.load_current_limit = load_current_limit


        self.time_on_aprrox = None
        self.max_duty_cycle = None 
        self.soft_start_capacitance = None 
        self.feedback_bottom_resistance = None
        self.current_limit_external_resistance = None
        self.inductor_ripple_current = None
        self.negitive_current_limit = None
        self.inductance = None 
        self.peak_to_peak_inductor_ripple_current = None
        self.maximum_inductor_current = None
        self.rms_inductor_current = None
        self.output_voltage_ripple = None
        self.peak_to_peak_feedback_voltage_ripple_using_feedforward_capacitor_only = None
        self.peak_to_peak_feedback_voltage_ripple_using_method_3 = None

        if feedforward_capacitor is None:
            self.feedforward_capacitance = None 
        else:
           self.feedforward_capacitance = feedforward_capacitor 

        if ripple_injection_resistor is None:
            self.ripple_injection_resistance = None 
        else:
           self.ripple_injection_resistance = ripple_injection_resistor 

        if ripple_injection_capacitor is None:
            self.ripple_injection_capacitance = None 
        else:
           self.ripple_injection_capacitance = ripple_injection_capacitor 

        if output_capacitance is None:
            self.output_capacitance = None
        else: 
            self.output_capacitance = output_capacitance

        if output_capacitance_esr is None:
            self.output_capacitance_esr = None
        else:
            self.output_capacitance_esr = output_capacitance_esr


    def update_input_voltage(self, new_voltage):
        self.input_voltage = new_voltage

    
    def preliminary_calculations(self, print_val = None):

        self.time_on_aprrox = self.output_voltage / (self.input_voltage * self.switching_frequency)

        self.max_duty_cycle = 1 - (MIC28516.min_on_time * self.switching_frequency)

        if print_val:
            value_print_block()
            value_printer("Time on", self.time_on_aprrox)
            value_printer("Max duty cycle", self.max_duty_cycle)

    def feedback_bottom_resistor(self, print_val = None):
        
        self.feedback_bottom_resistance = (MIC28516.feedback_referance_voltage_internal * self.feedback_top_resistance) / (self.output_voltage - MIC28516.feedback_referance_voltage_internal)
        
        if print_val:
            value_print_block()
            value_printer("Feedback bottom resistor value", self.feedback_bottom_resistance, "ohm")

    def soft_start_capacitor(self, print_val = None):
        self.soft_start_capacitance = (MIC28516.internal_soft_start_current * self.soft_start_time) / MIC28516.feedback_referance_voltage

        if print_val:
            value_print_block()
            value_printer("Soft start capacitance", self.soft_start_capacitance, "nF")



    def inductor_calculations(self, print_val = None):

        numerator = (self.output_voltage * self.input_voltage - self.output_voltage ** 2)
        denominator = (self.input_voltage * self.switching_frequency * self.ripple_current_ratio * MIC28516.maximum_output_current)
        self.inductance = numerator / denominator

        numerator_2 = (self.output_voltage * self.input_voltage - self.output_voltage ** 2)
        denominator_2 = (self.input_voltage * self.switching_frequency * self.inductance)
        self.peak_to_peak_inductor_ripple_current = numerator_2 / denominator_2

        self.maximum_inductor_current = MIC28516.maximum_output_current + 0.5 * self.peak_to_peak_inductor_ripple_current

        self.rms_inductor_current = M.sqrt(M.pow(MIC28516.maximum_output_current, 2) + M.pow(self.peak_to_peak_inductor_ripple_current, 2) / 12)


        if print_val:
            value_print_block()
            value_printer("Inductance", self.inductance, "H")
            value_printer("Peak to peak ind current ripple", self.peak_to_peak_inductor_ripple_current, "H")
            value_printer("Maximum current", self.maximum_inductor_current)
            value_printer("RMS ind current", self.rms_inductor_current)

    def output_capacitor_value_and_esr_plot(self, value_bounds, esr_bounds):
        pass
    
    def output_voltage_ripple_calculations(self, print_val = None):

        func_1 = M.pow((self.peak_to_peak_inductor_ripple_current / (self.output_capacitance * self.switching_frequency * 8)), 2)
        func_2 = M.pow((self.peak_to_peak_inductor_ripple_current  * self.output_capacitance_esr), 2)
        self.output_voltage_ripple = M.sqrt(func_1 + func_2)

        if print_val:
            value_print_block()
            value_printer("Output voltage ripple", self.output_voltage_ripple)


    def ripple_injection_calculations(self, print_val = None):
        self.peak_to_peak_feedback_voltage_ripple_using_feedforward_capacitor_only = self.output_capacitance_esr * self.peak_to_peak_inductor_ripple_current
        
        func_1 = (M.pow((M.pow(self.feedback_top_resistance, -1) + M.pow(self.feedback_bottom_resistance, -1) + M.pow(self.ripple_injection_resistance, -1)), -1) 
        * self.feedforward_capacitance)
        
        func_2_a = M.pow((M.pow(self.feedback_top_resistance, -1) + M.pow(self.feedback_bottom_resistance, -1)), -1) 
        func_2_b = self.ripple_injection_resistance + func_2_a
        func_2 = func_2_a / func_2_b

        func_3 = self.max_duty_cycle - M.pow(self.max_duty_cycle, 2)
       
        self.peak_to_peak_feedback_voltage_ripple_using_method_3 = self.input_voltage * func_2 * func_3 / (self.switching_frequency * func_1)

        if print_val:
            value_print_block()
            value_printer("Feedback pin voltage ripple from only a feedforward capacitor", self.peak_to_peak_feedback_voltage_ripple_using_feedforward_capacitor_only)
            value_printer("Feedback pin voltage ripple from method 3", self.peak_to_peak_feedback_voltage_ripple_using_method_3)


    def run_all_calcs(self):
        pass
        


def test_2():
    fsw = 300e3
    vin =  48
    vout = 12 
    tss = 30e-3
    ripple_ratio = 0.2
    fb_rtop = 21e3
    Ilim = 8
    Cout = 330e-6
    esr_Cout = 14e-3
    feedforward_cap = 4.7e-9
    ripple_resistor = 56.2e3
    ripple_capacitor = 100e-9
    buck_1 = MIC28516(fsw, vin, vout, tss, ripple_ratio, fb_rtop, Ilim, output_capacitance = Cout, output_capacitance_esr = esr_Cout, 
                      ripple_injection_resistor= ripple_resistor, ripple_injection_capacitor = ripple_capacitor, feedforward_capacitor = feedforward_cap)
    buck_1.preliminary_calculations(True)
    buck_1.feedback_bottom_resistor(True)
    buck_1.soft_start_capacitor(True)
    buck_1.inductor_calculations(True)
    buck_1.output_voltage_ripple_calculations(True)
    buck_1.ripple_injection_calculations(True)





def main():
    test_2()



if __name__ == "__main__":
    main()

    

    
         


    


