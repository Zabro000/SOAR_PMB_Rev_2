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


# Make the assumption that there are n many buck converters
# Assume all buck converters are in parallel 
class PCB_Object():

    def __init__(self, converter_efficiencies, converter_nominal_output_currents, converter_output_voltages, 
                 input_voltage: float = None, current_safety_factor: float = None):
        
        self.converter_efficiencies = np.array(converter_efficiencies)
        self.converter_nominal_output_currents = np.array(converter_nominal_output_currents)
        self.converter_output_voltages = np.array(converter_output_voltages)

        self.total_input_power = None
        self.total_output_power = None
        self.input_power_per_converter = None
        self.output_power_per_converter = None
        self.input_current_per_converter = None
        self.total_nominal_input_current = None
        self.total_nominal_input_current_with_safety_factor = None 

        if current_safety_factor is None:
            self.current_safety_factor = None 
        else:
            self.current_safety_factor = current_safety_factor

        if input_voltage is None:
            self.input_voltage = None
        else:
            self.input_voltage = input_voltage

    def compute_output_powers(self): 
        self.output_power_per_converter = np.multiply(self.converter_output_voltages, self.converter_nominal_output_currents)
        self.total_output_power = np.sum(self.output_power_per_converter)

    def compute_input_powers(self):
        self.input_power_per_converter = np.divide(self.output_power_per_converter, self.converter_efficiencies)
        self.total_input_power = np.sum(self.input_power_per_converter)


    def compute_input_currents(self):
        self.input_current_per_converter = self.input_power_per_converter * (1 / self.input_voltage)
        self.total_nominal_input_current = np.sum(self.input_current_per_converter)

    def compute_total_input_current_with_safety_factor(self):
        self.total_nominal_input_current_with_safety_factor = self.total_nominal_input_current * (1 + self.current_safety_factor)


    def compute_converter_powers(self):
        self.compute_output_powers()
        self.compute_input_powers()

    
    def run_all_computations(self):
        self.compute_output_powers()
        self.compute_input_powers()
        self.compute_input_currents()
        self.compute_total_input_current_with_safety_factor()


    def print_all_values(self):
        value_printer("\nTotal Output Power", self.total_output_power, "W")
        for i in range(len(self.converter_output_voltages)):
            print(f"Output Power for the {self.converter_output_voltages[i]:.2f}V Buck = {self.output_power_per_converter[i]:.2f}W")

        value_printer("\nTotal Input Power", self.total_input_power, "W")
        for i in range(len(self.converter_output_voltages)):
            print(f"Input Power for the {self.converter_output_voltages[i]:.2f}V Buck assuming eff = {self.converter_efficiencies[i] * 100:.2f}% = {self.input_power_per_converter[i]:.2f}W")

        value_printer("\nTotal Input Current", self.total_nominal_input_current, "A")
        for i in range(len(self.converter_output_voltages)):
            print(f"Input Current for the {self.converter_output_voltages[i]:.2f}V Buck = {self.input_current_per_converter[i]:.2f}A")


        value_printer(f"\nTotal Input Current with safety factor = {self.current_safety_factor * 100:.2f}%", self.total_nominal_input_current_with_safety_factor, "A")

        

        
class PCB_Feature():
    def __init__(self):
        pass

    @staticmethod
    def convert_mm_to_mil_general():
        pass

class PCB_Trace(PCB_Feature):
    def __init__(self):
        super().__init__()


def test():
    eff_avg = 0.92
    eff = [eff_avg, eff_avg, eff_avg]
    out = [12, 5, 3.3]
    curr = [8, 8, 8]
    input_1 = 16.8
    safety = 0.15

    pmb = PCB_Object(eff, curr, out, input_1, safety)
    pmb.test_computation()


def main():
    test() 


if __name__ == "__main__":
    main()
