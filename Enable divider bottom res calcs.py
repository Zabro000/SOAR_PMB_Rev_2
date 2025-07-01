

comparator_voltage = 5
hysteresis = (200 / 2) * 10 ** (-3)
triggering_voltage = 14
top_res = 6.8e4
def bottom_resistor(input_voltage, top_res, hysteresis, comparator_trigger):
    return ((comparator_trigger - hysteresis)* top_res) / (input_voltage - (comparator_trigger - hysteresis))

print()
print(bottom_resistor(triggering_voltage, top_res, hysteresis, comparator_voltage))
print()