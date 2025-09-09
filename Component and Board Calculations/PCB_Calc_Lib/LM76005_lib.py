import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import math
from engineering_notation import EngNumber
import os

def value_print_block():
    print()

def value_printer(sentance, value, unit: str = None, floating: int = None, end = None) -> None:

    if floating is None:
        floating = 2

    if unit is None:
        unit = " "

    eng_number = EngNumber(value)

    if not end:
        message = f"~ {sentance}: {eng_number}{unit}"
        print(message)
    else:
        message = f"~ {sentance}: {eng_number}{unit} {end}"
        print(message)


class LM76005():
    minimum_switch_on_time = 95e-9 
    minimum_switch_off_time = 130e-9

    feedback_referance_voltage_internal = 1.006
    enable_input_high_level_voltage = 1.14 # Used the minimum value
    enable_input_low_level_falling_voltage = 1.05

    internal_soft_start_current = 2.2e-6



    def __init__(self, switching_freq: float, input_voltage: float, output_voltage: float, soft_start_time: float, ripple_current_ratio: float,
                 feedback_top_resistor: float, load_current_limit: float, feedforward_capacitor: float = None,
                 ripple_injection_resistor: float = None, ripple_injection_capacitor: float = None, output_capacitance: float = None,
                 output_capacitance_esr: float = None, typical_efficiency: float = None, inductor_winding_resistance: float = None, injected_ripple_method_3: float = None, 
                 input_capacitance_esr: float = None):
        
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
        self.export_csv_filename = None 
        self.ideal_nominal_duty_cycle = None 
        self.time_off_aprrox = None
        self.switching_period = None
        self.period_approx = None
        self.inductor_copper_loss = None
        self.feedforward_capacitor_time_contsant_value = None # Yapped about on Pg 25


        # LM76005 Things
        self.maximum_output_voltage_no_frequency_foldback = None 


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

        if injected_ripple_method_3 is None:
            self.peak_to_peak_feedback_voltage_ripple_using_method_3 = None
        else:
            self.peak_to_peak_feedback_voltage_ripple_using_method_3 = injected_ripple_method_3

        if output_capacitance is None:
            self.output_capacitance = None
        else: 
            self.output_capacitance = output_capacitance

        if output_capacitance_esr is None:
            self.output_capacitance_esr = None
        else:
            self.output_capacitance_esr = output_capacitance_esr

        if typical_efficiency is None:
            self.typical_efficiency = None
        else:
            self.typical_efficiency = typical_efficiency

        if inductor_winding_resistance is None:
            self.inductor_winding_resistance = None
        else:
            self.inductor_winding_resistance = inductor_winding_resistance

        if input_capacitance_esr is None:
            self.input_capacitance_esr = None 
        else:
            self.input_capacitance_esr = input_capacitance_esr


    def preliminary_calculations(self, print_val = None):

        self.ideal_nominal_duty_cycle = self.output_voltage / (self.input_voltage * self.typical_efficiency)
        self.inverse_ideal_nominal_duty_cycle = 1 - self.ideal_nominal_duty_cycle 

        self.switching_period = 1 / self.switching_frequency

        self.max_duty_cycle = 1 - (LM76005.minimum_switch_off_time / self.switching_period)
        self.min_duty_cycle = LM76005.minimum_switch_on_time * self.switching_frequency

        self.maximum_output_voltage_no_frequency_foldback = self.input_voltage * self.max_duty_cycle

        self.maximum_input_voltage = self.output_voltage / (self.switching_frequency * LM76005.minimum_switch_on_time)
        self.minimum_input_voltage_no_frequency_foldback = self.output_voltage / (self.switching_frequency * LM76005.minimum_switch_off_time)

        if print_val:
            value_print_block()
            value_printer("Time on aprox", self.time_on_aprrox, "s")
            value_printer("Max duty cycle", self.max_duty_cycle, "")
            value_printer("Nominal duty cycle", self.ideal_nominal_duty_cycle * 100, "%")
            value_printer("Aprrox time off", self.time_off_aprrox, "s")
            value_printer("Switching frequency", self.switching_frequency, "Hz")
            value_printer("Switching period", self.switching_period, "s")
            value_printer("Switching period approx", self.period_approx, "s")

    def feedback_bottom_resistor(self, print_val = None):
        
        self.feedback_bottom_resistance = (LM76005.feedback_referance_voltage_internal * self.feedback_top_resistance) / (self.output_voltage - LM76005.feedback_referance_voltage_internal)
        
        if print_val:
            value_print_block()
            value_printer("Top feedback resistor value", self.feedback_top_resistance, "ohm")
            value_printer("Bottom feedback resistor value", self.feedback_bottom_resistance, "ohm")


    def enable_bottom_resistor(self, print_val = True):
        self.enable_bottom_resistance = (LM76005.enable_input_high_level_voltage * self.enable_top_resistance) / (self.enable_turn_on_rising_voltage - LM76005.enable_input_high_level_voltage)

        self.undervoltage_input_high_level_rising_voltage = LM76005.enable_input_high_level_voltage * (self.enable_bottom_resistance + self.enable_top_resistance) / self.enable_bottom_resistance

        self.undervoltage_input_low_level_falling_voltage = LM76005.enable_input_low_level_falling_voltage * (self.enable_bottom_resistance + self.enable_top_resistance) / self.enable_bottom_resistance

        if print_val:
            value_print_block()

    
    def soft_start_capacitor(self, print_val = None):

        self.soft_start_capacitance = (LM76005.internal_soft_start_current * self.soft_start_time)

        if print_val:
            value_print_block()
            value_printer("Soft start capacitance", self.soft_start_capacitance, "F")


    def switching_frequency_resistor(self, print_val = None): 
        
        self.switching_frequency_resistance = (1000 * 38400) / ((self.switching_frequency / 1000) - 14.33)

        if print_val:
            value_print_block()


    def power_good_bottom_resistor(self, print_val = None):

        if self.output_voltage > 10: 
            self.power_good_bottom_resistance = self.power_good_top_resistance

        if print_val:
            value_print_block()



    def output_inductor(self, print_val = None):
        correcting_factor = 1e-6


        self.peak_to_peak_inductor_ripple_current = self.ripple_current_ratio * self.output_current
        self.maximum_inductor_current = self.output_current + 0.5 * (self.peak_to_peak_inductor_ripple_current)

        higher_inductance_bound = correcting_factor * ((self.input_voltage - self.output_voltage) * self.ideal_nominal_duty_cycle) / (self.switching_frequency * self.ripple_current_ratios[0] * self.output_current)
        lower_inductance_bound = correcting_factor * ((self.input_voltage - self.output_voltage) * self.ideal_nominal_duty_cycle) / (self.switching_frequency * self.ripple_current_ratios[1] * self.output_current)

        if print_val:
            value_print_block()


    def output_capacitor(self, print_val = None):
        func_1 = math.pow((self.switching_frequency * self.ripple_current_ratio * (self.target_output_votlage_undershoot / self.output_current)), -1)
        func_2 = math.pow(self.ripple_current_ratio, 2) * (1 + self.inverse_ideal_nominal_duty_cycle) / 12
        func_3 = (self.inverse_ideal_nominal_duty_cycle * (1 + self.ripple_current_ratio))

        self.minimum_output_capacitance = func_1 * (func_2 + func_3)
        
        func_4 = self.inverse_ideal_nominal_duty_cycle / (self.switching_frequency * self.minimum_output_capacitance)
        func_5 = math.pow(self.ripple_current_ratio, -1) + 0.5

        self.maximum_output_capacitor_esr = func_4 * func_5


    def feedforward_capacitor(self, print_val = None): 

        crossover_frequency = (15.46) / (self.output_voltage * self.output_capacitance)

        func_1 = math.pow(2 * math.pi * crossover_frequency, -1)
        func_2 = (self.feedback_bottom_resistance * self.feedback_top_resistance) / (self.feedback_bottom_resistance + self.feedback_top_resistance)
        func_3 = math.pow(self.feedback_top_resistance * func_2, -(1/2))

        self.feedforward_capacitance = func_1 * func_3 




        
        



