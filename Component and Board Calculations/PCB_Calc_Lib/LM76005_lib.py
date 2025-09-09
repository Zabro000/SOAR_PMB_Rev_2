import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import math
from engineering_notation import EngNumber
import os

def value_print_block(title: str = None):
    if title is None: 
        print()

    else:
        print()
        print(f"{title:-^100}")

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

    def __init__(self, switching_freq: float, input_voltage: float, output_voltage: float, output_current: float, typical_efficiency: float, soft_start_time: float, ripple_current_ratio: float, ripple_current_ratios: list,
                 feedback_top_resistor: float, enable_top_resistor: float, power_good_top_resistor: float, enable_turn_on_votlage: float, target_output_votlage_undershoot: float):
        
        self.switching_frequency = switching_freq
        self.soft_start_time = soft_start_time
        self.input_voltage = input_voltage
        self.output_voltage = output_voltage
        self.output_current = output_current
        self.ripple_current_ratio = ripple_current_ratio
        self.ripple_current_ratios = ripple_current_ratios
        self.feedback_top_resistance = feedback_top_resistor
        self.enable_top_resistance = enable_top_resistor
        self.power_good_top_resistance = power_good_top_resistor
        self.typical_efficiency = typical_efficiency
        self.enable_turn_on_rising_voltage = enable_turn_on_votlage
        self.target_output_votlage_undershoot = target_output_votlage_undershoot

        # LM76005 Things
        self.soft_start_capacitance = None 
        self.feedback_bottom_resistance = None
        self.enable_bottom_resistance = None 
        self.power_good_bottom_resistance = None

        self.inductor_ripple_current = None
        self.range_of_inductance_values = None 
        self.peak_to_peak_inductor_ripple_current = None
        self.maximum_inductor_current = None
 
        self.switching_period = None
        self.maximum_output_voltage_no_frequency_foldback = None 
        self.ideal_nominal_duty_cycle = None 
        self.inverse_ideal_nominal_duty_cycle = None 
        self.max_duty_cycle = None  
        self.min_duty_cycle = None 
        self.maximum_input_voltage = None 
        self.minimum_input_voltage_no_frequency_foldback = None 
        self.switching_frequency_resistance = None 
        self.feedforward_capacitance = None  

        self.undervoltage_input_high_level_rising_voltage = None 
        self.undervoltage_input_low_level_falling_voltage = None 

        if len(ripple_current_ratios) != 2:
            raise ValueError


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
            value_print_block(title = "Preliminary Calcs")
            value_printer("Max duty cycle", self.max_duty_cycle * 100, "%")
            value_printer("Min duty cycle", self.min_duty_cycle * 100, "%")
            value_printer("Ideal Nominal duty cycle", self.ideal_nominal_duty_cycle * 100, "%")
            value_printer("Inverse Ideal Nominal duty cycle", self.inverse_ideal_nominal_duty_cycle * 100, "%")
            value_printer("Switching frequency", self.switching_frequency, "Hz")
            value_printer("Switching period", self.switching_period, "s")
            value_printer("Max input voltage", self.maximum_input_voltage, "V")
            value_printer("Min input voltage with no freq foldback", self.minimum_input_voltage_no_frequency_foldback, "V")

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
            value_printer("Top enable resistor value", self.enable_top_resistance, "ohm")
            value_printer("Bottom enable resistor value", self.enable_bottom_resistance, "ohm")
            value_printer("Undervoltage turn on votlage", self.undervoltage_input_high_level_rising_voltage, "V")
            value_printer("Undervoltage turn off votlage", self.undervoltage_input_low_level_falling_voltage, "V")

    
    def soft_start_capacitor(self, print_val = None):
        self.soft_start_capacitance = (LM76005.internal_soft_start_current * self.soft_start_time)

        if print_val:
            value_print_block()
            value_printer("Soft start capacitance value", self.soft_start_capacitance, "F")


    def switching_frequency_resistor(self, print_val = None): 
        
        self.switching_frequency_resistance = (1000 * 38400) / ((self.switching_frequency / 1000) - 14.33)

        if print_val:
            value_print_block()
            value_printer("Switching freq setting resistor value", self.switching_frequency_resistance, "ohm")


    def power_good_bottom_resistor(self, print_val = None):

        if self.output_voltage > 10: 
            self.power_good_bottom_resistance = self.power_good_top_resistance

        if print_val:
            value_print_block()
            print("Since for all of our bucks the output voltage is small the bottom resistor is the same as the top resistor.")
            value_printer("Top and bottom resistor value", self.power_good_top_resistance, "ohm")



    def output_inductor(self, print_val = None):
        correcting_factor = 1e-6


        self.peak_to_peak_inductor_ripple_current = self.ripple_current_ratio * self.output_current
        self.maximum_inductor_current = self.output_current + 0.5 * (self.peak_to_peak_inductor_ripple_current)

        higher_inductance_bound = ((self.input_voltage - self.output_voltage) * self.ideal_nominal_duty_cycle) / (self.switching_frequency * self.ripple_current_ratios[0] * self.output_current)
        lower_inductance_bound = ((self.input_voltage - self.output_voltage) * self.ideal_nominal_duty_cycle) / (self.switching_frequency * self.ripple_current_ratios[1] * self.output_current)
        
        self.range_of_inductance_values = [lower_inductance_bound, higher_inductance_bound]
        
        if print_val:
            value_print_block()
            print(f"~ Max inductance for the minimum ripple ratio of {self.ripple_current_ratios[0]}, inductance = {EngNumber(higher_inductance_bound)}H")
            print(f"~ Min inductance for the maximum ripple ratio of {self.ripple_current_ratios[1]}, inductance = {EngNumber(lower_inductance_bound)}H")
            value_printer("Peak to peak inductor current ripple", self.peak_to_peak_inductor_ripple_current, "A")
            value_printer("Peak current", self.maximum_inductor_current, "A")


    def output_capacitor(self, print_val = None):
        func_1 = math.pow((self.switching_frequency * self.ripple_current_ratio * (self.target_output_votlage_undershoot / self.output_current)), -1)
        func_2 = math.pow(self.ripple_current_ratio, 2) * (1 + self.inverse_ideal_nominal_duty_cycle) / 12
        func_3 = (self.inverse_ideal_nominal_duty_cycle * (1 + self.ripple_current_ratio))

        self.minimum_output_capacitance = func_1 * (func_2 + func_3)
        
        func_4 = self.inverse_ideal_nominal_duty_cycle / (self.switching_frequency * self.minimum_output_capacitance)
        func_5 = math.pow(self.ripple_current_ratio, -1) + 0.5

        self.maximum_output_capacitor_esr = func_4 * func_5

        if print_val:
            value_print_block()
            value_printer("Target votlage undershoot", self.target_output_votlage_undershoot, "V")
            value_printer("Min output capacitance", self.minimum_output_capacitance, "F")
            value_printer("Max output capacitor esr", self.maximum_output_capacitor_esr, "ohm")


    def feedforward_capacitor(self, print_val = None): 

        crossover_frequency = (15.46) / (self.output_voltage * self.minimum_output_capacitance)

        func_1 = math.pow(2 * math.pi * crossover_frequency, -1)
        func_2 = (self.feedback_bottom_resistance * self.feedback_top_resistance) / (self.feedback_bottom_resistance + self.feedback_top_resistance)
        func_3 = math.pow(self.feedback_top_resistance * func_2, -(1/2))

        self.feedforward_capacitance = func_1 * func_3 

        if print_val:
            value_print_block()
            value_printer("Feedforward capacitor value approx", self.feedforward_capacitance, "F")



    def block_standard_run_calculations(self):
        print_values = True 
        self.preliminary_calculations(print_values)
        self.feedback_bottom_resistor(print_values)
        self.enable_bottom_resistor(print_values)
        self.power_good_bottom_resistor(print_values)
        self.switching_frequency_resistor(print_values)
        self.soft_start_capacitor(print_values)

        self.output_inductor(print_values)
        self.output_capacitor(print_values)

        self.feedforward_capacitor(print_values)



def test():
    fsw = 400e3
    vin =  48
    vout = 12 
    tss = 30e-3
    ripple_ratio = 0.2
    ripple_ratios = [ripple_ratio, ripple_ratio * 2]
    fb_rtop = 21e3
    en_rtop = 100e3
    pg_rtop = 100e3
    current = 5
    eff = 0.9
    turn_on = 14
    undershoot = 10e-3 
    
    buck_1 = LM76005(fsw, vin, vout, current, eff, tss, ripple_ratio, ripple_ratios, fb_rtop, en_rtop, pg_rtop, turn_on, undershoot)
    buck_1.block_standard_run_calculations()


def test_3V3_values(): 
    fsw = 400e3
    vin =  48
    vout = 3.3
    tss = 15e-3
    ripple_ratio = 0.2
    ripple_ratios = [ripple_ratio, ripple_ratio * 2]
    fb_rtop = 8.87e3
    en_rtop = 110e3
    pg_rtop = 100e3
    current = 5
    eff = 0.9
    turn_on = 14
    undershoot = 10e-3 
    
    buck_1 = LM76005(fsw, vin, vout, current, eff, tss, ripple_ratio, ripple_ratios, fb_rtop, en_rtop, pg_rtop, turn_on, undershoot)
    buck_1.block_standard_run_calculations()



def main():
    test()


if __name__ == "__main__":
    main()








        
        



