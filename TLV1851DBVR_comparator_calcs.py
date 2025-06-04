v_ref = 5
vcc = 5
r_1 = 8100
r_2 = 10e5


print((5-1.8) / (2e-3) - 1)
print(2000 * (0.43e-9))



def hysteresis_calc(v_ref, v_in, resistor_1, resistor_2):
    hysteresis = v_in * (resistor_1 / resistor_2)
    return hysteresis


print(hysteresis_calc(5,5,r_1, r_2) * 1000)

