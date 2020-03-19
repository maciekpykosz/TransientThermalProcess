import numpy as np

from global_system.Calculation import solve, set_nodes_temperature
from global_system import GlobalData as GlDt

for time_step in range(GlDt.time_step_number):

    # Obliczamy składowe konieczne do rozwiązania układu
    # równań w celu wyznaczenia temperatury w węzłach
    h_global, p_global = solve()

    # Rozwiązujemy układ równań
    nodes_temp = np.dot(np.linalg.inv(h_global), p_global)

    # Ustawiamy nową temperaturę w węzłach
    set_nodes_temperature(nodes_temp)

    # Wyświetlamy temperaturę min i max
    print("TIME STEP: {}\t\tMIN: {:.3f}\t\tMAX: {:.3f}".format(time_step, np.amin(nodes_temp), np.amax(nodes_temp)))
