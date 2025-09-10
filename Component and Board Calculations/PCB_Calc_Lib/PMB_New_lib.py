import numpy as np
from engineering_notation import EngNumber
import pandas as pd


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

class PMB_Power_Source_Voltage_Divider():
    def __init__(self, bottom_resistor, enable_node_votlage: float, enable_source_voltage: float):
        self.bottom_resistor = bottom_resistor
        self.enable_node_votlage = enable_node_votlage
        self.enable_source_voltage = enable_source_voltage

        self.top_resistor = None 
        self.middle_resistor = None
        self.divider_current = None

    def calculate_all_resistors(self, print_val = None):
        self.divider_current = self.enable_node_votlage / self.bottom_resistor

        self.top_resistor = (0.5 * self.enable_source_voltage) / self.divider_current
        self.middle_resistor = (0.5 * self.enable_source_voltage - self.enable_node_votlage) / self.divider_current

        if print_val:
            value_print_block("Resistor Divider Calculations")
            print(f"Top Resistor = {EngNumber(self.top_resistor)}ohm, Middle Resitor = {EngNumber(self.middle_resistor)}ohm, Bottom Resistor = {EngNumber(self.bottom_resistor)}ohm")
            print(f"Total divider current = {EngNumber(self.divider_current)}A")
            

# Make converter object to do the math but I have write code since some converters are nested
class PMB_Converter():
    number_of_boards = None
    per_board_total_output_power = None
    per_board_total_input_power = None
    per_board_total_input_current = None 
    per_board_total_input_current_with_safety_factor = None
    av_system_total_output_power = None
    av_system_total_input_power = None 
    av_system_total_input_current = None
    av_system_total_input_current_with_safety_factor = None
    av_system_nominal_input_voltage = None

    def __init__(self, name: str, converter_efficiency: float, converter_nominal_output_current: float, converter_output_voltage, 
                 converter_input_voltage: float, input_current_safety_factor: float):
        
        self.converter_name = name
        self.converter_efficiency = converter_efficiency
        self.converter_nominal_output_current = converter_nominal_output_current
        self.converter_output_voltage = converter_output_voltage
        self.converter_input_voltage = converter_input_voltage
        self.input_current_safety_factor = input_current_safety_factor

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


    def print_all_values(self):
        value_print_block(f"Calculations for the {self.converter_name}")

        value_printer("Output current", self.converter_nominal_output_current, "A")
        value_printer("Input current", self.converter_input_current, "A")
        value_printer(f"Input current with {self.input_current_safety_factor} safety factor", self.converter_input_current_with_safety_factor, "A")

        value_printer("Output power", self.converter_output_power, "W")
        value_printer(f"Input power with {self.converter_efficiency} efficiency", self.converter_input_power, "W")

    def run_all_computations(self):
        self.compute_output_power()
        self.compute_input_power()
        self.compute_input_current()
        self.compute_input_current_with_safety_factor()
        self.print_all_values()


    @staticmethod
    def run_new_PMB_configuration(buck_12V, buck_5V, ldo_3V3):

        buck_5V_remaning_output_power = buck_5V.converter_output_power - ldo_3V3.converter_input_power

        total_output_power = buck_12V.converter_output_power + buck_5V.converter_output_power - (ldo_3V3.converter_input_power - ldo_3V3.converter_output_power)
        total_input_power = buck_12V.converter_input_power + buck_5V.converter_input_power
        total_input_current = buck_12V.converter_input_current + buck_5V.converter_input_current
        total_input_current_with_safety_factor = buck_12V.converter_input_current_with_safety_factor + buck_5V.converter_input_current_with_safety_factor

        PMB_Converter.per_board_total_input_power = total_input_power
        PMB_Converter.per_board_total_output_power = total_output_power
        PMB_Converter.per_board_total_input_current = total_input_current
        PMB_Converter.per_board_total_input_current_with_safety_factor = total_input_current_with_safety_factor

        value_print_block(title = "Calculations for the New PMB Configuration")
        value_printer(f"3V3 LDO Output Power when its output current = {ldo_3V3.converter_nominal_output_current}A is", ldo_3V3.converter_output_power, "W")
        value_printer(f"3V3 LDO Input Power when its efficiency = {ldo_3V3.converter_efficiency} is", ldo_3V3.converter_input_power, "W")
        value_printer(f"3V3 LDO Wasted Power when its efficiency = {ldo_3V3.converter_efficiency} is", ldo_3V3.converter_input_power - ldo_3V3.converter_output_power, "W")
        value_print_block()
        value_printer("5V Buck Output power", buck_5V.converter_output_power, "W")
        value_printer(f"5V Buck Input power whens its efficiency = {buck_5V.converter_efficiency} ", buck_5V.converter_input_power, "W")
        value_printer(f"5V Buck remaining output power", buck_5V_remaning_output_power, "W")
        value_print_block()
        value_printer(f"The total output power including the 12V buck is", total_output_power, "W")
        value_printer(f"The total input power including the 12V buck is", total_input_power, "W")

        if buck_12V.converter_input_voltage == buck_5V.converter_input_voltage:
            value_printer(f"The total input current when the input voltage is {buck_12V.converter_input_voltage}V is", total_input_current, "A")
            PMB_Converter.av_system_nominal_input_voltage = buck_12V.converter_input_voltage
        else:
            raise ValueError
        

    @classmethod
    def update_entire_system_values(cls, number_of_boards: int):
        cls.number_of_boards = number_of_boards

        cls.av_system_total_input_power = cls.per_board_total_input_power * cls.number_of_boards
        cls.av_system_total_output_power = cls.per_board_total_output_power * cls.number_of_boards
        cls.av_system_total_input_current = cls.per_board_total_input_current * cls.number_of_boards
        cls.av_system_total_input_current_with_safety_factor = cls.per_board_total_input_current_with_safety_factor * cls.number_of_boards

        value_print_block("Av System Calculations")
        value_printer(f"The total output power of the system with {cls.number_of_boards} boards is", cls.av_system_total_output_power, "W")
        value_printer(f"The total input power of the system with {cls.number_of_boards} boards is", cls.av_system_total_input_power, "W")
        value_print_block()
        value_printer(f"The total input current per board when the input voltage is {PMB_Converter.av_system_nominal_input_voltage}V is", PMB_Converter.per_board_total_input_current, "A")
        value_printer(f"The total input current per board with safety factor when the input voltage is {PMB_Converter.av_system_nominal_input_voltage}V is", PMB_Converter.per_board_total_input_current_with_safety_factor, "A")
        value_print_block()
        value_printer(f"The total input current of the system with {cls.number_of_boards} board(s) is", cls.av_system_total_input_current, "A")
        value_printer(f"The total input current of the system with {cls.number_of_boards} board(s) and with safety factor is", cls.av_system_total_input_current_with_safety_factor, "A")


def test_bucks():
    or_bus_voltage = 15
    buck_1 = PMB_Converter("12 Buck", 0.9, 5, 12, or_bus_voltage, 0.15)
    buck_1.run_all_computations()

    buck_2 = PMB_Converter("5 Buck", 0.9, 5, 5, or_bus_voltage, 0.15)
    buck_2.run_all_computations()

    ldo_1 = PMB_Converter("3V3 LDO", 0.65, 3, 3.3, buck_2.converter_input_voltage, 0.15)
    ldo_1.run_all_computations()

    PMB_Converter.run_new_PMB_configuration(buck_1, buck_2, ldo_1)
    PMB_Converter.update_entire_system_values(1)

def test_divider():
    div_1 = PMB_Power_Source_Voltage_Divider(10e3, 5.2, 14)
    div_1.calculate_all_resistors(True)

    bottom_values = np.linspace(start= 5000, stop = 20000, num = 51)
    middle_resistors = np.array([])
    top_resistors = np.array([])
    for i in bottom_values:
        div_1.bottom_resistor = i
        div_1.calculate_all_resistors()
        middle_resistors = np.append(middle_resistors, div_1.middle_resistor)
        top_resistors = np.append(top_resistors, div_1.top_resistor)


    data = {"Top resistor": top_resistors, "Middle resistor": middle_resistors, "Bottom_resistors": bottom_values}

    dataframe = pd.DataFrame(data = data)

    print(dataframe)


    


def main():
    test_divider()

if __name__ == "__main__":
    main()