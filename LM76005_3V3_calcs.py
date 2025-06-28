v_out = 3.3 #V

# Feedback resistors
V_REF = 1.006 #V
r_fbt = 8.87e3 #ohm

# Enable resistor divider
r_ent = 110e3 #ohm
turn_on_input_voltage = 14 #V
ENABLE_HIGH = 1.204 #V
V_ENL = 1.05

# Soft start capacitor
CHARGING_CURRENT = 2.2e-6 #A
soft_start_time = 15e-3 #ms





def fb_output_voltage_resistor_divider(v_out, top_resistor):
    return (top_resistor * V_REF) / (v_out - V_REF)


def enable_pin_voltage_divider_calculations(enable_turn_on_voltage, top_resistor):
    bottom_resistor = (ENABLE_HIGH * top_resistor) / (enable_turn_on_voltage - ENABLE_HIGH)
    falling_voltage = V_ENL * (bottom_resistor + top_resistor) / bottom_resistor
    return [bottom_resistor, falling_voltage]

def soft_start_capacitor(soft_start_time):
    return soft_start_time * CHARGING_CURRENT

def output_inductor(voltage_out, max_load_current, voltage_in, switching_frequency):
    duty_c = voltage_out / voltage_in
    print(duty_c)
    low_inductance =  ((voltage_in - voltage_out) * duty_c) / (switching_frequency * 0.2 * max_load_current)
    high_inductance =  ((voltage_in - voltage_out) * duty_c) / (switching_frequency * 0.4 * max_load_current)
    return [low_inductance, high_inductance]
    





def main():
    print(f"R_fbt = {r_fbt:.0f}ohm, R_fbb = {fb_output_voltage_resistor_divider(v_out, r_fbt):.0f}ohm")
    print(f"R_fbt = {r_ent:.0f}ohm, R_fbb = {enable_pin_voltage_divider_calculations(turn_on_input_voltage, r_ent)}ohm")
    print(f"Css = {soft_start_capacitor(soft_start_time)* 10e8:.2f}nF")
    ind_list = output_inductor(v_out, 5, 16.8, ((4e5)))
    print(ind_list)





if __name__ == "__main__":
    main()