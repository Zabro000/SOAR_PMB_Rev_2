import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import math
from engineering_notation import EngNumber
import os
import random

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

class LM73100RPWR:
    undervoltage_rising_pin = 1.2
    overvotlage_rising_pin = 1.2
    power_good_rising_pin = 1.2
    current_monitor_pin_voltage_max = 0.5
    gain_current_monitor = 182

    def __init__(self, buck_converter_output_capacitance, estimated_output_capacitance, estimated_inrush_current, 
                 overvoltage_input: float, undervoltage_input: float, maximum_output_current, top_resistor: float = None, power_good_top_resistor: float = None, power_good_rising_voltage: float = None):
        self.buck_converter_output_capacitance = buck_converter_output_capacitance
        self.estimated_output_capacitance = estimated_output_capacitance
        self.estimated_inrush_current = estimated_inrush_current
        self.overvoltage_input = overvoltage_input
        self.undervoltage_input = undervoltage_input
        self.top_resistor = top_resistor
        self.power_good_top_resistor = power_good_top_resistor
        self.power_good_rising_voltage = power_good_rising_voltage
        self.maximum_output_current = maximum_output_current
        
        

        self.output_slew_rate = None
        self.limiter_capacitance_value = None
        self.middle_resistor = None 
        self.bottom_resistor = None

        self.power_good_bottom_resistor = None 

        self.current_monitor_resistor = None

    def inrush_current_limiter_capacitor_calculation(self):
        self.output_slew_rate = (self.estimated_inrush_current * 1000) / ((self.estimated_output_capacitance + self.buck_converter_output_capacitance) * 1e6)
        self.limiter_capacitance_value = 2000 / (self.output_slew_rate)

    def uv_ov_resistor_divider_calculations(self, print_val, real_middle_resistor = None, real_bottom_resistor = None):
        C = LM73100RPWR.overvotlage_rising_pin
        D  = LM73100RPWR.undervoltage_rising_pin

        A_prime = C - self.overvoltage_input
        B_prime = D - self.undervoltage_input

        self.middle_resistor = (self.top_resistor * ((-B_prime * C) + (A_prime *  D))) / (A_prime * self.undervoltage_input - A_prime * D + B_prime * C)
        self.bottom_resistor = (-C * (self.top_resistor + self.middle_resistor)) / (A_prime)

        if (real_bottom_resistor is not None) and (real_middle_resistor is not None):
            minimum_current = self.undervoltage_input / (self.top_resistor + real_bottom_resistor + real_bottom_resistor)

        else:
            minimum_current = self.undervoltage_input / (self.top_resistor + self.bottom_resistor + self.middle_resistor)

        if print_val:
            value_print_block("Undervoltage and Overvotlage Resistor Divider Calculations")
            print(f"Top Resistor = {EngNumber(self.top_resistor)}ohm, Middle Resitor = {EngNumber(self.middle_resistor)}ohm, Bottom Resistor = {EngNumber(self.bottom_resistor)}ohm")
            print(f"At {EngNumber(self.undervoltage_input)}V, the minimum current is {EngNumber(minimum_current)}A which needs to be more than 2uA")
        

    def power_good_resistor_divider_calculations(self, print_val, real_bottom_resistor = None):
        A = LM73100RPWR.power_good_rising_pin
        self.power_good_bottom_resistor = (-A * self.power_good_top_resistor) / (A - self.power_good_rising_voltage)


        if real_bottom_resistor is not None:
            minimum_current = self.power_good_rising_voltage / (self.power_good_top_resistor + real_bottom_resistor)
        else: 
            minimum_current = self.power_good_rising_voltage / (self.power_good_top_resistor + self.power_good_bottom_resistor)


        if print_val:
            value_print_block("Resistor Divider 2 Way Calculations")
            print(f"Power Good Top Resistor = {EngNumber(self.power_good_top_resistor)}ohm, Power Good Bottom Resistor = {EngNumber(self.power_good_bottom_resistor)}ohm")
            print(f"At {EngNumber(self.power_good_rising_voltage)}V, the minimum current is {EngNumber(minimum_current)}A which needs to be more than 20uA")


    def current_monitor_resistor_calcualtions(self, print_val):

        A = LM73100RPWR.current_monitor_pin_voltage_max
        B = LM73100RPWR.gain_current_monitor 

        self.current_monitor_resistor = (A * 1e6) / (self.maximum_output_current * B)
        
        if print_val:
            value_print_block("Current monitor resistor")
            print(f"Power Good Top Resistor = {EngNumber(self.current_monitor_resistor)}ohm")



