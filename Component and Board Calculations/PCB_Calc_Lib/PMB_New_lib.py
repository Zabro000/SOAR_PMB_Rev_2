import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import math as M 
from engineering_notation import EngNumber


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


# Make converter object to do the math but I have write code since some converters are nested
class PMB_Converter():

    def __init__(self, converter_efficiency: float, converter_nominal_output_current: float, converter_output_voltage, 
                 converter_input_voltage: float, input_current_safety_factor: float):
        


        
        self.converter_efficiency = converter_efficiency
        self.converter_nominal_output_current = converter_nominal_output_current
        self.converter_output_voltage = converter_output_voltage
        self.converter_input_voltage = converter_input_voltage
        self.input_current_safety_factor = input_current_safety_factor

    

        self.total_input_power = None
        self.total_output_power = None
        self.converter_input_power = None
        self.converter_output_power = None
        self.converter_input_current = None
        self.converter_input_current_with_safety_factor = None


    def compute_output_power(self): 
        self.converter_output_power = np.multiply(self.converter_output_voltage, self.converter_nominal_output_current)

    def compute_input_power(self):
        self.converter_input_power = np.divide(self.converter_output_power, self.converter_efficiency)

    def compute_input_current(self):
        self.converter_input_current = self.converter_input_power * (1 / self.converter_input_voltage)

    def compute_input_current_with_safety_factor(self):
        self.converter_input_current_with_safety_factor = self.converter_input_current * (1 + self.input_current_safety_factor)


    def run_all_computations(self):
        self.compute_output_power()
        self.compute_input_power()
        self.compute_input_current()
        self.compute_input_current_with_safety_factor()


    def compute_left_over_current_and_power_from_nested_converter():
        pass


    def print_all_values(self):
        value_printer("\nTotal Output Power", self.total_output_power, "W")
        for i in range(len(self.converter_output_voltages)):
            print(f"Output Power for the {self.converter_output_voltages[i]:.2f}V Buck = {self.output_power_per_converter[i]:.2f}W")

        value_printer("\nTotal Input Power", self.total_input_power, "W")
        for i in range(len(self.converter_output_voltages)):
            print(f"Input Power for the {self.converter_output_voltages[i]:.2f}V Buck assuming eff = {self.converter_efficiencies[i] * 100:.2f}% = {self.input_power_per_converter[i]:.2f}W")
        
        value_printer("\nTotal Output Current", sum(self.converter_nominal_output_currents), "A")
        for i in range(len(self.converter_output_voltages)):
            print(f"Input Current for the {self.converter_output_voltages[i]:.2f}V Buck = {self.converter_nominal_output_currents[i]:.2f}A")
      
        value_printer("\nTotal Input Current", self.total_nominal_input_current, "A")
        for i in range(len(self.converter_output_voltages)):
            print(f"Input Current for the {self.converter_output_voltages[i]:.2f}V Buck = {self.input_current_per_converter[i]:.2f}A")

        value_printer(f"\nTotal Input Current with safety factor = {self.current_safety_factor * 100:.2f}%", self.total_nominal_input_current_with_safety_factor, "A")

        


def test():
    buck_1 = PMB_Converter(0.9, 5, 12, 16.8, 0.15)
    buck_1.run_all_computations()

    buck_2 = PMB_Converter(0.9, 5, 5, 16.8, 0.15)
    buck_2.run_all_computations()


test()