height = 0.100
width = 0.100
nodes_number_for_height = 4
nodes_number_for_width = 4
conductivity = 25
specific_heat = 700
density = 7800
alfa = 300
simulation_time = 500
simulation_step_time = 50
initial_temperature = 100
ambient_temperature = 1200

nodes_number = nodes_number_for_height * nodes_number_for_width
elements_number = (nodes_number_for_height - 1) * (nodes_number_for_width - 1)
distance_between_nodes_for_height = height / (nodes_number_for_height - 1)
distance_between_nodes_for_width = width / (nodes_number_for_width - 1)
