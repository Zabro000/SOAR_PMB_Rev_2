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
    def __init__(self, buck_converter_output_capacitance, estimated_output_capacitance, estimated_inrush_current, 
                 overvoltage_input: float, undervoltage_input: float, top_resistor: float = None):
        self.buck_converter_output_capacitance = buck_converter_output_capacitance
        self.estimated_output_capacitance = estimated_output_capacitance
        self.estimated_inrush_current = estimated_inrush_current
        self.overvoltage_input = overvoltage_input
        self.undervoltage_input = undervoltage_input
        self.top_resistor = top_resistor

        self.output_slew_rate = None
        self.limiter_capacitance_value = None
        self.middle_resistor = None 
        self.bottom_resistor = None


    def inrush_current_limiter_capacitor_calculation(self):
        self.output_slew_rate = (self.estimated_inrush_current * 1000) / ((self.estimated_output_capacitance + self.buck_converter_output_capacitance) * 1e6)
        self.limiter_capacitance_value = 2000 / (self.output_slew_rate)

    def uv_ov_resistor_divider_calculations(self, print_val):
        C = LM73100RPWR.overvotlage_rising_pin
        D  = LM73100RPWR.undervoltage_rising_pin

        A_prime = C - self.overvoltage_input
        B_prime = D - self.undervoltage_input

        self.middle_resistor = (self.top_resistor * ((-B_prime * C) + (A_prime *  D))) / (A_prime * self.undervoltage_input - A_prime * D + B_prime * C)
        self.bottom_resistor = (-C * (self.top_resistor + self.middle_resistor)) / (A_prime)
        

        if print_val:
            value_print_block("Resistor Divider 3 Way Calculations")
            print(f"Top Resistor = {EngNumber(self.top_resistor)}ohm, Middle Resitor = {EngNumber(self.middle_resistor)}ohm, Bottom Resistor = {EngNumber(self.bottom_resistor)}ohm")




