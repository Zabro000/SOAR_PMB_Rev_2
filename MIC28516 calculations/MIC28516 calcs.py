switching_frequency = 300e3
MIN_ON_TIME = 240e-9
RDS_LOW_SIDE_MOSFET = 18e-3
ADJUSTED_FSW = 800e3 
INERTAL_SS_CURRENT = 1.4e-6
soft_start_time = 50e-3
VREF = 0.6
V_INTERNAL_FB_VOLTAGE = 0.6 
selected_output_voltage = 12
inductor_ripple_current = None
CURRENT_LIMIT_SOURCE_CURRENT = 96e-6
load_current_limit = None
AC_RIPPLE_CURRENT_TO_DC_RATIO = 0.2


def time_on_estimate(Vout, Vin, fsw):
    return Vout / (Vin * fsw)


def max_duty_cycle(fsw):
    return 1 - (MIN_ON_TIME * fsw)


def negitive_current_limit(switching_node_voltage):
    return switching_node_voltage / RDS_LOW_SIDE_MOSFET

def adjusted_switching_frequency(top_resistor, bottom_resistor):
    return (top_resistor * ADJUSTED_FSW) / (top_resistor + bottom_resistor)

def soft_start_capacitor(soft_start_time):
    return (INERTAL_SS_CURRENT * soft_start_time) / VREF

def output_voltage_bottom_resistor(top_resistor, vout):
    return (V_INTERNAL_FB_VOLTAGE * top_resistor) / (vout - V_INTERNAL_FB_VOLTAGE)


def source_current_limit_resistor(load_I_lim, inductor_ripple_current):
    return (load_I_lim + (inductor_ripple_current / 2)) * RDS_LOW_SIDE_MOSFET / CURRENT_LIMIT_SOURCE_CURRENT


def inductor_selection_and_indcutor_ppk_to_pkk_current_ripple(v_out, v_in_max, v_in_nom, fsw, current_output_max):
    inductance = (v_out * (v_in_max - v_out)) / (v_in_max * fsw * AC_RIPPLE_CURRENT_TO_DC_RATIO * current_output_max)
    peak_to_peak_inductor_ripple = (v_out * (v_in_nom - v_out)) / (v_in_nom * switching_frequency * inductance)
    peak_current = current_output_max + (0.5 * peak_to_peak_inductor_ripple)
    rms_inductor_current = (current_output_max ** 2 + (peak_to_peak_inductor_ripple ** 2) / 12) ** (1/2)

def output_voltage_ripple(peak_to_peak_i_ripple, output_cap, fsw, output_cap_esr):
    v_out_ripple = ((peak_to_peak_i_ripple / (output_cap * fsw * 8)) ** 2 + (peak_to_peak_i_ripple * output_cap_esr) ** 2) ** (0.5)
    return v_out_ripple


def output_cap_i_rms(indcutor_ripple_i_peak_to_peak):
    return indcutor_ripple_i_peak_to_peak / (12) ** (1/2)


def power_loss_output_cap(cap_i_rms, esr_output_cap):
    return (cap_i_rms ** 2) * esr_output_cap

def input_cap_calculations(peak_indcutor_current, input_cap_esr, max_output_current, duty_cycle_maybe):
    input_voltage_ripple = input_cap_esr * peak_indcutor_current
    approx_input_cap_rms_current = max_output_current * (duty_cycle_maybe * (1 - duty_cycle_maybe)) ** (1/2)
    power_loss_input_capacitor = approx_input_cap_rms_current * (input_cap_esr ** 2)


def ripple_injection_calculations(input_voltage, k_div, duty_cycle, switching_frequency):
    k_div = None ### silly thing here
    injected_ripple = input_voltage * k_div * duty_cycle * switching_frequency



def running_12V_ripple_injection():
    pass


def running_simple_values_for_12V_buck_converter(): 
    #print(output_voltage_bottom_resistor(20.8e3, selected_output_voltage))
    #print(soft_start_capacitor(30e-3) * 10e8)


    print("Please note these values calculate the worst case voltage ripple because the max voltage input and current ripple is used. " \
    "The actual voltage ripple will be much lower.")
    out_cap_vals = [220e-6, 100e-6, 55e-6, 22e-6]
    esr_values = [5,4,3,2,1,0.2,0.1,0.05,0.01,0.005]
    capacitance_1 = 330e-6
    esr_1 = 14e-3

    for esr in esr_values:
        print(f"ESR: {esr}ohm")
        for val in out_cap_vals:
            print(f"Capacitance: {val * 1e6}uF voltage ripple: {output_voltage_ripple(1.6, val, switching_frequency, esr):.5f}V")

        print("\n\n\n")

    print(f"Capacitance: {capacitance_1 * 1e6}uF voltage ripple: {output_voltage_ripple(1.6, capacitance_1, switching_frequency, esr_1):.5f}V")


def main():
    print(57 / 36)
    print(432 / 270)




if __name__ == "__main__":
    main()

    