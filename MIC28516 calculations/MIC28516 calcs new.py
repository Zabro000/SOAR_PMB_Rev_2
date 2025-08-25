import MIC28516_lib as Buck





def buck_12V():
    # defining inital values
    fsw = 300e3
    vin =  48
    vout = 12 
    tss = 30e-3
    ripple_ratio = 0.2
    fb_rtop = 21e3
    curent_limit = 8
    c_out = 330e-6
    esr_c_out = 14e-3
    feedforward_cap = 4.7e-9
    ripple_resistor = 56.2e3
    ripple_capacitor = 100e-9
    eff = 0.9
    winding_res = 1.9e-3

    buck_1 = Buck.MIC28516(fsw, vin, vout, tss, ripple_ratio, fb_rtop, curent_limit, output_capacitance = c_out, output_capacitance_esr = esr_c_out, 
                      ripple_injection_resistor= ripple_resistor, ripple_injection_capacitor = ripple_capacitor, feedforward_capacitor = feedforward_cap,
                      typical_efficiency = eff, inductor_winding_resistance = winding_res)
    
    buck_1.run_all_calcs_compare()

    buck_1.input_voltage = 16.8

    buck_1.run_all_calcs_compare(set_inductance = True, set_inductance_value = buck_1.inductance)

def buck_5V():
    # defining inital values
    fsw = 300e3
    vin =  48
    vout = 5 
    tss = 30e-3
    ripple_ratio = 0.2
    fb_rtop = 21e3
    curent_limit = 8
    c_out = 330e-6
    esr_c_out = 14e-3
    feedforward_cap = 4.7e-9
    ripple_resistor = 56.2e3
    ripple_capacitor = 100e-9
    eff = 0.9

    buck_1 = Buck.MIC28516(fsw, vin, vout, tss, ripple_ratio, fb_rtop, curent_limit, output_capacitance = c_out, output_capacitance_esr = esr_c_out, 
                      ripple_injection_resistor= ripple_resistor, ripple_injection_capacitor = ripple_capacitor, feedforward_capacitor = feedforward_cap,
                      typical_efficiency = eff)
    
    buck_1.run_all_calcs_compare()

    buck_1.export_list_of_values()
    


def buck_3V3():
    fsw = 300e3
    vin =  48
    vout = 3.3 
    tss = 30e-3
    ripple_ratio = 0.2
    fb_rtop = 21e3
    curent_limit = 8
    c_out = 330e-6
    esr_c_out = 14e-3
    feedforward_cap = 4.7e-9
    ripple_resistor = 56.2e3
    ripple_capacitor = 100e-9
    eff = 0.9

    buck_1 = Buck.MIC28516(fsw, vin, vout, tss, ripple_ratio, fb_rtop, curent_limit, output_capacitance = c_out, output_capacitance_esr = esr_c_out, 
                      ripple_injection_resistor= ripple_resistor, ripple_injection_capacitor = ripple_capacitor, feedforward_capacitor = feedforward_cap,
                      typical_efficiency = eff)
    
    buck_1.run_all_calcs_compare()

    buck_1.export_list_of_values()


def main():
    buck_12V()

if __name__ == "__main__":
    main()
