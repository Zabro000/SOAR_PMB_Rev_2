import MIC28516_lib as Buck
import numpy as np
from engineering_notation import EngNumber
from matplotlib import pyplot as plt


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
    ripple_resistor = 39e3
    ripple_capacitor = 100e-9
    eff = 0.9
    winding_res = 1.9e-3

    buck_1 = Buck.MIC28516(fsw, vin, vout, tss, ripple_ratio, fb_rtop, curent_limit, output_capacitance = c_out, output_capacitance_esr = esr_c_out, 
                      ripple_injection_resistor= ripple_resistor, ripple_injection_capacitor = ripple_capacitor, feedforward_capacitor = feedforward_cap,
                      typical_efficiency = eff, inductor_winding_resistance = winding_res)
    
    buck_1.run_all_calcs_compare()

    buck_1.input_voltage = 16.8
    set_ind = buck_1.inductance

    buck_1.run_all_calcs_compare(set_inductance = True, set_inductance_value = set_ind)

    ripple_res = np.linspace(start = 15e3, stop = 65e3, num = 20)
    listt = np.array([])

    for i in range(np.size(ripple_res)):
        buck_1.ripple_injection_resistance = float(ripple_res[i])
        buck_1.ripple_injection_calculations_given_components_known()
        listt = np.append(listt, buck_1.peak_to_peak_feedback_voltage_ripple_using_method_3)

    fig, ax = plt.subplots(figsize = (4*2,3*2))
    ax.plot(ripple_res, listt, color = 'green', linestyle = 'dashed', marker = 'o')
    ax.grid(True, color = 'k', linestyle = "--")
    ax.set_xlabel("Ripple Injection Resistor Value (ohm)")
    ax.set_ylabel("Injected Ripple (V)")
    ax.set_title("Injected Ripple vs Ripple Injection Resistor Value")


    plt.savefig("Injected Ripple vs Ripple Injection Resistor Value.png")
    plt.show()


def buck_12V_1():
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
    ripple_resistor = 39e3
    ripple_capacitor = 100e-9
    eff = 0.9
    winding_res = 1.9e-3

    buck_1 = Buck.MIC28516(fsw, vin, vout, tss, ripple_ratio, fb_rtop, curent_limit, output_capacitance = c_out, output_capacitance_esr = esr_c_out, 
                      ripple_injection_resistor= ripple_resistor, ripple_injection_capacitor = ripple_capacitor, feedforward_capacitor = feedforward_cap,
                      typical_efficiency = eff, inductor_winding_resistance = winding_res)
    
    buck_1.run_all_calcs_compare()

    buck_1.input_voltage = 16.8
    set_ind = buck_1.inductance

    buck_1.run_all_calcs_compare(set_inductance = True, set_inductance_value = set_ind)



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
    buck_12V_1()


if __name__ == "__main__":
    main()
