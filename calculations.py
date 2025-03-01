import math




# https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/752/SiC47x_Jul04_2018.pdf


Vin_max = 52
Vin_min = 13.5
Vout_1 = 12
Vout_2 = 5
Vout_3 = 3.3
output_cap_1_esr = 0
output_cap_esr_list = [output_cap_1_esr]
CURRENT_OUT_MAX = 4 # subject to change 
MAXIMUM_RIPPLE_CURRENT_PERCENTANGE = 0.25


D_constant = 0 # Pg 7 that D in the equation for Rx WHAT EVEN IS THAT
D_constant_test = 0.5 # Im just guessing the D value
power_dissipation_max_for_rx = 80e-3 # typical 0603 power dissapation is 25mW so I am using that
VRAMP_MAX = 0.9
VRAMP_MIN = 0.1
Rfb_l_value = 10e4
VOLTAGE_FEEDBACK = 0.8



#  Not sure if unknown or not:
switching_freqency = 500_000


# Unknown:
time_on = 0 # Pg 11 the time on used for the on pulse (like from the Vramp crossing Vcomp)
total_output_capacitor_esr = 0
inductance_value = 0
output_ripple_current_max = 0 


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


    Cx_min = (P_dissapation_max) / (v_in_max * switching_freqnecy * VRAMP_MAX)
    print(Cx_min, Rx)


    Vramp_min = ((v_in_min - v_out) * v_out) / (v_in_min * switching_freqnecy * Cx_min * Rx)


    print(Vramp_min)
    if Vramp_min > 0.2:
        Cx_final = Cx_min
    else:
        Cx_final = (Cx_min) * (Vramp_min / 0.2)
        print(Cx_final)
   


    if Vramp_min < 0.1:
        print("INCREASE THE POWER MAX AND TRY AGAIN")
        return None
   
    Cy_final = 1 / (820 * switching_freqnecy) # Wrong value it is
    print(Cy_final)


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

def minimum_output_capacitance(inductance, max_out_current, output_ripple_current_max, )









print(output_voltage_setting_feedback_resistor(12))
print(general_output_voltage(13.5))
print(resistor_for_switching_freqency(switching_freqency, Vout_1))
print(voltage_ramp_amplitude_Rx_Cx_general_calculation(Vin_max, Vin_min, Vout_1, D_constant, power_dissipation_max_for_rx, switching_freqency))


