from PCB_Calc_Lib.PCB_lib import PCB_Object 
import numpy as np
from engineering_notation import EngNumber
from matplotlib import pyplot as plt


def pmb_power_and_current_calculations():
    average_efficiency = 0.92
    efficiency = [average_efficiency, average_efficiency, average_efficiency]
    output_voltages = [12, 5, 3.3]
    output_currents = [5, 5, 5]
    input_votlages = [48, 45, 16.8, 14, 13.5]
    safety_factor = 0.15

    pmb_1 = PCB_Object(efficiency, output_currents, output_voltages, current_safety_factor = safety_factor)

    total_input_current_list_with_saftey_factor = []
    for i in input_votlages:
        print(f"Current input votlage: {i}")
        pmb_1.input_voltage = i 
        pmb_1.run_all_computations()
        pmb_1.print_all_values()
        print()
        total_input_current_list_with_saftey_factor.append(pmb_1.total_nominal_input_current_with_safety_factor)

    input_votlages_new = np.linspace(13.5, 48, 500)
    total_input_current = np.array([])

    for i in input_votlages_new:
        pmb_1.input_voltage = i 
        pmb_1.run_all_computations()
        total_input_current = np.append(total_input_current, pmb_1.total_nominal_input_current_with_safety_factor)

    fig, ax = plt.subplots(figsize = (4*3,3*3))
    ax.plot(input_votlages_new, total_input_current, color = 'green', linestyle = 'solid')
    ax.grid(True, color = 'k', linestyle = "--")

    plt.show()


def test():
    pmb_power_and_current_calculations()


def main():
    test()


if __name__ == "__main__":
    main()
