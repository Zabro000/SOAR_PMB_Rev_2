import math

# General values
v_out = 12 # volts
V_REF = 1 # volt
f_sw = 3e5


# Feedback voltage divider (Pg 10, 20)
r_fbt = 10e4 # ohms

# Enable pin votlage divider to set under voltage limits
v_in_under_voltage = 10 # volts
V_EN_FALLING_THRESHOLD = 0.95 # volts
V_EN_RAISING_THRESHOLD = 1.4 # volts
V_BATT = 16.8 # volts
r_ent = 10e4

# Inductor selection (Pg 20,21)
INDUCTOR_RIPPLE_CURRENT = 0.4 # 40% of load current
max_load_current = 2.5 # amps






def fb_output_voltage_resistor_divider(v_out, top_resistor):
    return (top_resistor * V_REF) / (v_out - V_REF)

def enable_pin_under_voltage_trip(under_voltage, top_resistor):
    bottom_resistor = (top_resistor * V_EN_FALLING_THRESHOLD) / (under_voltage - V_EN_FALLING_THRESHOLD)
    under_voltage_current = under_voltage / (bottom_resistor + top_resistor)
    nominal_voltage_current = V_BATT / (bottom_resistor + top_resistor)
    enable_pin_nominal_voltage = V_BATT - (top_resistor * nominal_voltage_current)

    return [bottom_resistor, under_voltage_current, nominal_voltage_current, enable_pin_nominal_voltage]


def switching_frequency_resistor(switching_frequency):
    return 30970 * (switching_frequency / 1000) ** (-1.027)


def output_inductor(voltage_out, max_load_current, voltage_in, switching_frequency):
    return (voltage_in - voltage_out) * (voltage_out / voltage_in) / (switching_frequency * INDUCTOR_RIPPLE_CURRENT * max_load_current)



def main():
    print(f"R_fbb = {fb_output_voltage_resistor_divider(v_out, r_fbt):.0f}ohm")
    print(enable_pin_under_voltage_trip(v_in_under_voltage, r_ent))
    print(switching_frequency_resistor(f_sw))
    print(output_inductor(v_out, max_load_current, V_BATT, f_sw) * 10**6)
    pass


if __name__ == "__main__":
    main()


