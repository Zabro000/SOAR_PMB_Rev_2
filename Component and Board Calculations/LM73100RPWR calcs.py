from PCB_Calc_Lib.PMB_New_lib import PMB_Power_Source_Voltage_Divider as vd
from PCB_Calc_Lib.PMB_New_lib import General_Resistor_Divider as gd
from PCB_Calc_Lib.LM73100RPWR_lib import LM73100RPWR as L



def rail_3V3():
    div_1 = vd(None, 12000, 1.2, 3)
    div_1.calculate_all_resistors_2_divider(True)
    div_2 = gd(3.1, 10000, None, 1.2, 1.2)
    div_2.calculate_all_resistors_3_divider(True)


def new_func():
    div_4 = L(None, None, None, 5, 3, 10000)
    div_4.uv_ov_resistor_divider_calculations(True)



def main():
    new_func()

if __name__ == "__main__":
    main()