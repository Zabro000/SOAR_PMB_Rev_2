import numpy as np
from engineering_notation import EngNumber


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


def test():
    or_bus_voltage = 15
    buck_1 = PMB_Converter("12 Buck", 0.9, 5, 12, or_bus_voltage, 0.15)
    buck_1.run_all_computations()

    buck_2 = PMB_Converter("5 Buck", 0.9, 5, 5, or_bus_voltage, 0.15)
    buck_2.run_all_computations()

    ldo_1 = PMB_Converter("3V3 LDO", 0.65, 3, 3.3, buck_2.converter_input_voltage, 0.15)
    ldo_1.run_all_computations()

    PMB_Converter.run_new_PMB_configuration(buck_1, buck_2, ldo_1)
    PMB_Converter.update_entire_system_values(1)


def main():
    test()

if __name__ == "__main__":
    main()