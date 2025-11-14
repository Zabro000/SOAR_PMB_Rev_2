from PCB_Calc_Lib.PMB_New_lib import PMB_Power_Source_Voltage_Divider as Div
import numpy as np
import pandas as pd





def batt_voltage_divider():
    bottom_resistor = 1e4
    top_resistor_inital = None
    priority_source_voltage = 5.2 # This is because the propogation delay of the comparators is low when an input 
    power_source_turn_on_voltage = 14


    div_1 = Div(bottom_resistor, top_resistor_inital, priority_source_voltage, power_source_turn_on_voltage)
    div_1.calculate_all_resistors_3_divider()

    bottom_values = np.linspace(start= 1e4, stop = 5e4, num = 101)
    middle_resistors = np.array([])
    top_resistors = np.array([])

    for i in bottom_values:
        div_1.bottom_resistor = i
        div_1.calculate_all_resistors_3_divider()
        middle_resistors = np.append(middle_resistors, div_1.middle_resistor)
        top_resistors = np.append(top_resistors, div_1.top_resistor)


    data = {"Top resistor": top_resistors, "Middle resistor": middle_resistors, "Bottom_resistors": bottom_values}

    dataframe = pd.DataFrame(data = data)
    dataframe = dataframe.round(0)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(dataframe)

def umb_voltage_divider():
    bottom_resistor = 1e4
    top_resistor_inital = None
    priority_source_voltage = 5.2 # This is because the propogation delay of the comparators is low when an input 
    power_source_turn_on_voltage = 45


    div_1 = Div(bottom_resistor, top_resistor_inital, priority_source_voltage, power_source_turn_on_voltage)
    div_1.calculate_all_resistors_3_divider()

    bottom_values = np.linspace(start= 1e4, stop = 5e4, num = 201)
    middle_resistors = np.array([])
    top_resistors = np.array([])

    for i in bottom_values:
        div_1.bottom_resistor = i
        div_1.calculate_all_resistors_3_divider()
        middle_resistors = np.append(middle_resistors, div_1.middle_resistor)
        top_resistors = np.append(top_resistors, div_1.top_resistor)


    data = {"Top resistor": top_resistors, "Middle resistor": middle_resistors, "Bottom_resistors": bottom_values}

    dataframe = pd.DataFrame(data = data)
    dataframe = dataframe.round(0)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(dataframe)




def main():
    umb_voltage_divider()

   


if __name__ == "__main__":
    main()



