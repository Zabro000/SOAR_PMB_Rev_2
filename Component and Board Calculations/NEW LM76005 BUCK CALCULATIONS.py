from PCB_Calc_Lib.LM76005_lib import LM76005 
import numpy as np
from matplotlib import pyplot as plt



def buck_converter_5V_calcs():
    fsw = 400e3
    vin =  48
    vout = 5 
    tss = 30e-3
    ripple_ratio = 0.2
    ripple_ratios = [ripple_ratio, ripple_ratio * 2]
    fb_rtop = 10e3
    en_rtop = 100e3
    pg_rtop = 100e3
    current = 5
    eff = 0.9
    turn_on = 14.5
    undershoot = 100e-3 
    my_capacitor = 180e-6
    
    buck_1 = LM76005(fsw, vin, vout, current, eff, tss, ripple_ratio, ripple_ratios, fb_rtop, en_rtop, pg_rtop, turn_on, undershoot, my_capacitor)

    print(f"\n\nINPUT VOLTAGE IS {buck_1.input_voltage}V\n\n")
    buck_1.block_standard_run_calculations()

    buck_1.input_voltage = 3.7 * 5

    print(f"\n\nINPUT VOLTAGE IS {buck_1.input_voltage}V\n\n")
    buck_1.block_standard_run_calculations()

    print(5 * 0.021)

def buck_converter_12V_calcs():
    fsw = 400e3
    vin =  48
    vout = 12
    tss = 30e-3
    ripple_ratio = 0.2
    ripple_ratios = [ripple_ratio, ripple_ratio * 2]
    fb_rtop = 10e3
    en_rtop = 100e3
    pg_rtop = 100e3
    current = 5
    eff = 0.9
    turn_on = 14.5
    undershoot = 100e-3 
    my_capacitor = 180e-6
    
    buck_1 = LM76005(fsw, vin, vout, current, eff, tss, ripple_ratio, ripple_ratios, fb_rtop, en_rtop, pg_rtop, turn_on, undershoot, my_capacitor)

    print(f"\n\nINPUT VOLTAGE IS {buck_1.input_voltage}V\n\n")
    buck_1.block_standard_run_calculations()

    buck_1.input_voltage = 3.7 * 5

    print(f"\n\nINPUT VOLTAGE IS {buck_1.input_voltage}V\n\n")
    buck_1.block_standard_run_calculations()

def main():
    buck_converter_12V_calcs()


if __name__ == "__main__":
    main()