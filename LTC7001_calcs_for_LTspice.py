import math

rising_under_voltage_threshold = 4.75 #V
UNDER_VOLTAGE_HYSTERESIS = 0.3 #V

turn_on_rc_resistor = 5e3 #ohm
turn_on_rc_capacitor = 20e-9 #F
output_rail_bulk_capacitance = 100e-6 #F
BOOT_STRAPPED_VOLTAGE = 12 #V
UMBILICAL_VOLTAGE = 48

mosfet_gate_charge = 27e-9
bootstrap_capacitor = 250e-9


def under_voltage_resistor(rising_voltage_threshold):
    resistor = rising_under_voltage_threshold / 70e-6
    falling_threshold = rising_under_voltage_threshold - UNDER_VOLTAGE_HYSTERESIS
    print(f"Rvccuv = {resistor:.0f}ohm")
    print(f"Under voltage falling threshold = {falling_threshold:.2f}V")

def rc_turn_on_delay_circuit(rc_resistor, rc_capacitor, output_bulk_capacitance):
    inrush_current = (0.7 * BOOT_STRAPPED_VOLTAGE * output_bulk_capacitance) / (rc_resistor * rc_capacitor)
    output_voltage_rise_rate = (0.7 * BOOT_STRAPPED_VOLTAGE) / (rc_resistor * rc_capacitor)

    print(f"Approx inrush current = {inrush_current:.4f}A")
    print(f"Approx output voltage rise rate = {output_voltage_rise_rate / 1000:.2f}v/ms")
    print(f"Approx time to reach the umbilical voltage = {UMBILICAL_VOLTAGE / output_voltage_rise_rate * 1000:.2f}ms")

def bootstrap_capacitor_check(mosfet_gate_charge, rc_capacitor, bootstrap_capacitor):
    total_capacitance = mosfet_gate_charge + 10 * rc_capacitor
    print(f"RC capacitance + gate capacitance = {total_capacitance * 10**9:.4f}nF")
    print(f"Bootstrap capactance is {bootstrap_capacitor * 10**9:.4}nF")
    print(bootstrap_capacitor > total_capacitance)



under_voltage_resistor(rising_under_voltage_threshold)
rc_turn_on_delay_circuit(turn_on_rc_capacitor, turn_on_rc_resistor, output_rail_bulk_capacitance)
bootstrap_capacitor_check(mosfet_gate_charge, turn_on_rc_capacitor, bootstrap_capacitor)

