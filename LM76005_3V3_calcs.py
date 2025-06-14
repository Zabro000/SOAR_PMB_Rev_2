v_out = 3.3

# Feedback resistors
V_REF = 1.006
r_fbt = 8.87e3

# Enable resistor divider






def fb_output_voltage_resistor_divider(v_out, top_resistor):
    return (top_resistor * V_REF) / (v_out - V_REF)


def enable_pin_voltage_divider_calculations(enable_turn_on_voltage, bottom_resistor_value):
    top_resistor = bottom_resistor_value * ((enable_turn_on_voltage / V_EN_RAISING_THRESHOLD) -1)
    turn_off_voltage = V_EN_FALLING_THRESHOLD * (enable_turn_on_voltage / V_EN_RAISING_THRESHOLD)
    return [top_resistor, turn_off_voltage]





def main():
    print(f"R_fbt = {r_fbt:.0f}ohm, R_fbb = {fb_output_voltage_resistor_divider(v_out, r_fbt):.0f}ohm")




if __name__ == "__main__":
    main()