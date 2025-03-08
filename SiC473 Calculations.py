import math

# https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/752/SiC47x_Jul04_2018.pdf


Vin_max = 52
Vin_min = 14
Vout_1 = 12
Vout_2 = 5
Vout_3 = 3.3
output_cap_1_esr = 0
output_cap_esr_list = [output_cap_1_esr]
CURRENT_OUT_MAX = 4 # subject to change 
MAXIMUM_RIPPLE_CURRENT_PERCENTANGE = 0.25


D_constant = 0 # Pg 7 that D in the equation for Rx WHAT EVEN IS THAT
D_constant_test = 0.5 # Im just guessing the D value
power_dissipation_max_for_rx = 0.025 # typical 0603 power dissapation is 25mW so I am using that
VRAMP_MAX = 0.9
VRAMP_MIN = 0.1
Rfb_l_value = 10e4
VOLTAGE_FEEDBACK = 0.8
TRANCONDUCTANCE_OF_ERROR_AMP = 300e-6 


#  Not sure if unknown or not:
switching_freqency = 250_000


# Unknown:
time_on = 0 # Pg 11 the time on used for the on pulse (like from the Vramp crossing Vcomp)
total_output_capacitor_esr = 0
inductance_value = 0
output_ripple_current_max = 0 
output_voltage_adjustment_resistor = 0 
ratio_of_feedback_divider = 0 


# Pg 11 has equation, and is used for the inequality on Pg 7
def time_on_calculation(v_out, v_in, switching_freqnecy):
    t_on = (v_out) / (v_in * switching_freqnecy)
    return t_on


# Formula is not in the datasheet, just a way to find this for different caps
def total_output_capacitor_esr_sum(cap_esr_list):
    total_output_cap_esr = sum(cap_esr_list)
    return total_output_cap_esr


# Pg 7 has the formula and ratonale, inportant to stop oscillations
def oscillation_check_inequality(total_out_cap_esr, total_out_capacitace, t_on):
    return (total_out_cap_esr * total_out_capacitace) > (t_on / 2)


# Pg 7 has the formulae, calculates Cx, Cy, Rx and Vramp following the process outlined on Pg 7
def voltage_ramp_amplitude_Rx_Cx_general_calculation(v_in_max, v_in_min, v_out, D, P_dissapation_max, switching_freqnecy):
    
    # Step 1:
    Rx = (v_in_max * v_out * (1 - D)) / P_dissapation_max

    # Step 2: 
    Cx_min = (P_dissapation_max) / (v_in_max * switching_freqnecy * VRAMP_MAX)
    
    Vramp_min = ((v_in_min - v_out) * v_out) / (v_in_min * switching_freqnecy * Cx_min * Rx)

    print("Checking Vramp Min", Vramp_min)
    if Vramp_min > 0.2:
        Cx_final = Cx_min
    else:
        Cx_final = (Cx_min) * (Vramp_min / 0.2)
        print(Cx_final)
   
    if Vramp_min < 0.1:
        print("INCREASE THE POWER MAX AND TRY AGAIN")
    
    Cy_final = 1 / (820 * switching_freqnecy) # Wrong value it is

    return [Rx, Cx_final, Cy_final]
 

# Pg 11 for equation, voltage feedback value and RFB_L is there too
def output_voltage_setting_feedback_resistor(v_out):
    R_fb_h = (Rfb_l_value * (v_out - VOLTAGE_FEEDBACK))/VOLTAGE_FEEDBACK
    return R_fb_h


# Pg 4
def general_output_voltage(v_in):
    v_out = 0.92 * v_in
    return v_out


# Pg 4 for fsw values, Pg 6 for formula and for pin 24
def resistor_for_switching_freqency(switching_freqnecy, v_out):
    resistor_value = v_out / (switching_freqnecy * 190e-12)
    return resistor_value


# pg 11, intermidate step for calculating the inductor
def time_on_general_calculation(v_out, switching_freqnecy, v_in_min):
    time_on = (v_out) / (v_in_min * switching_freqnecy)
    return time_on

# pg 11, final calculation to get the inductance of the output inductor
def indcutance_calculation(time_on, v_out, v_in_min, max_out_current, ripple_current_percent):
    inductance = ((v_in_min - v_out) * time_on) / (max_out_current * ripple_current_percent)
    return inductance

# pg 11, intermediate step to determine the maximum voltage ripple and to find the minimum required output capacitance
def output_current_ripple_max(max_out_current, ripple_current_percent):
    return max_out_current + max_out_current * ripple_current_percent

# pg 11, equation to find the output capacitances 
def minimum_output_capacitance(inductance, max_out_current, output_ripple_current_max):
    pass

# pg 11 equation 1 for total output capacitance
def total_output_capacitance(max_output_ripple_voltage, max_inductor_ripple_current, switching_freq, total_output_capacitor_ESR):
    output_cap = 1 / (8 * (max_output_ripple_voltage / max_inductor_ripple_current - total_output_capacitor_ESR) * switching_freq)
    return output_cap

# pg 11 might be useful for determining the output minimum output capacitance
def general_voltage_ripple_calculation(max_current_ripple, total_output_capacitance, total_output_esr, switching_freq):
    ripple_voltage = (max_current_ripple) * (1 / (8 * total_output_capacitance * switching_freq) + total_output_esr)
    return ripple_voltage

# pg 8, all equations on this page  COMPLETE, THIS FUNCTION IS NOT DONE YET
def error_amplifier_compensation_calculations(output_voltage_setting_resistor, cross_over_frequency_gain):
    # Step 1:
    feedback_divider_ratio = Rfb_l_value / (output_voltage_setting_resistor + Rfb_l_value)

    # Step 2:
    compensation_resistor = 1 / (TRANCONDUCTANCE_OF_ERROR_AMP * cross_over_frequency_gain * feedback_divider_ratio)
    pass




def main():
    print("VALUES FOR THE 12V RAIL BUCK:\n")
    time_on = time_on_general_calculation(Vout_1, switching_freqency, Vin_min)
    inductance_value = indcutance_calculation(time_on, Vout_1, Vin_min, CURRENT_OUT_MAX, MAXIMUM_RIPPLE_CURRENT_PERCENTANGE)
    output_voltage_adjustment_resistor = output_voltage_setting_feedback_resistor(Vout_1)
    ripple_injection_values = voltage_ramp_amplitude_Rx_Cx_general_calculation(Vin_max, Vin_min, Vout_1, D_constant_test, power_dissipation_max_for_rx, switching_freqency)

    print(f"R(fsw): {resistor_for_switching_freqency(switching_freqency, Vout_1):.4e}")
    print(f"t(on): {time_on:.2e}")
    print(f"Max output voltage is {general_output_voltage(Vin_min)} if the min input voltage is {Vin_min}")
    print(f"L: {inductance_value:.2e}")
    print(f"R(_FB_H): {output_voltage_adjustment_resistor:.4e}")
    print(f"R(x): {ripple_injection_values[0]:.2e}")
    print(f"C(x): {ripple_injection_values[1]:.2e}")
    print(f"C(y): {ripple_injection_values[2]:.2e}")



if __name__ == "__main__":
    main()




