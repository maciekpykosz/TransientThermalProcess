from global_system.Grid import Grid
from local_system.UniversalElement import UniversalElement

first_grid = Grid()
print("The grid's created.")

first_uni_element = UniversalElement()
print("Universal element's created")

first_uni_element.create_jacobian_matrix(first_grid.elements[0], 2)
print("Jacobian matrix's created")
