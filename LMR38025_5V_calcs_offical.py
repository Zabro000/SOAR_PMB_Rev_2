import math

# General values
v_out = 5 # V
V_REF = 1 # V
f_sw = 3e5 # Hz


# Feedback voltage divider (Pg 10, 20)
r_fbt = 10e4 # ohms

# Enable pin votlage divider to set under voltage limits
v_turn_on_voltage = 14 # V
V_EN_FALLING_THRESHOLD = 0.95 # V
V_EN_RAISING_THRESHOLD = 1.4 # V
V_BATT = 16.8 # V
r_enb = 10e3 # ohm

# Inductor selection (Pg 20,21)
INDUCTOR_RIPPLE_CURRENT = 0.4 # 40% of load current
max_load_current = 2.5# A

# Ripple voltage
max_ripple_voltage = 0.02 #V


def fb_output_voltage_resistor_divider(v_out, top_resistor):
    return (top_resistor * V_REF) / (v_out - V_REF)

def enable_pin_voltage_divider_calculations(enable_turn_on_voltage, bottom_resistor_value):
    top_resistor = bottom_resistor_value * ((enable_turn_on_voltage / V_EN_RAISING_THRESHOLD) -1)
    turn_off_voltage = V_EN_FALLING_THRESHOLD * (enable_turn_on_voltage / V_EN_RAISING_THRESHOLD)
    return [top_resistor, turn_off_voltage]

def switching_frequency_resistor(switching_frequency):
    return 30970 * (switching_frequency / 1000) ** (-1.027)


def output_inductor(voltage_out, max_load_current, voltage_in, switching_frequency):
    return ((voltage_in - voltage_out) / (switching_frequency * INDUCTOR_RIPPLE_CURRENT * max_load_current)) * (voltage_out / voltage_in)

def subharmonic_oscillation_check(minimum_inductance, switching_frequency, output_voltage):
    return minimum_inductance >= 0.25 * (output_voltage / switching_frequency)


def input_rms_current_through_ceramic_capacitor_check(load_current):
    return load_current / 2

def ripple_voltage_percentage(v_out, ripple_voltage):
    return (ripple_voltage / v_out) * 100


def main():
    print("Values: \n")
    enable_pin_values = enable_pin_voltage_divider_calculations(v_turn_on_voltage, r_enb)
    print(f"R_fbb = {fb_output_voltage_resistor_divider(v_out, r_fbt):.0f}ohm")
    print(f"R_T = {switching_frequency_resistor(f_sw) * 1000:.0f}ohm")
    print(f"L = {output_inductor(v_out, max_load_current, V_BATT, f_sw) * 10**6:.2f}uH")
    print(f"Subharmonic inductor sizing check: {subharmonic_oscillation_check(11e-6, f_sw, v_out)}")
    print(f"RMS current though the input ceramic capacitor: {input_rms_current_through_ceramic_capacitor_check(max_load_current)}A")
    print(f"R_ent = {enable_pin_values[0]}ohm R_enb = {r_enb}ohm")
    print(f"Disable voltage = {enable_pin_values[1]}V Enable voltage = {v_turn_on_voltage}V")
    print(f"Ripple voltage = {max_ripple_voltage * 1000}mV")
    print(f"Ripple voltage percentage = {ripple_voltage_percentage(v_out, max_ripple_voltage):.2f}%")
    print()
    pass


if __name__ == "__main__":
    main()


