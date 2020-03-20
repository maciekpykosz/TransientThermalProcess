from math import sqrt

import numpy as np

from global_system import GlobalData as GlDt
from global_system.Element import Element
from global_system.Grid import Grid
from global_system.Node import Node
from local_system.UniversalElement import UniversalElement


def calc_shape_fun_deriv_in_one_direct(uni_el: UniversalElement, jacobian, integration_point, shape_fun_num, coordinate_num):
    shape_fun_der_in_dir = np.linalg.inv(jacobian)[coordinate_num][0] \
                           * uni_el.shape_fun_dksi_matrix[integration_point][shape_fun_num] \
                           + np.linalg.inv(jacobian)[coordinate_num][1] \
                           * uni_el.shape_fun_deta_matrix[integration_point][shape_fun_num]
    return shape_fun_der_in_dir


def calc_shape_fun_dx(element, jacobian, integration_point, shape_fun_num):
    return calc_shape_fun_deriv_in_one_direct(element, jacobian, integration_point, shape_fun_num, 0)


def calc_shape_fun_dy(element, jacobian, integration_point, shape_fun_num):
    return calc_shape_fun_deriv_in_one_direct(element, jacobian, integration_point, shape_fun_num, 1)


def det_jacobian_1d(node1: Node, node2: Node):
    det = sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) / 2.0
    return det


def calc_for_integration_point(element: Element, uni_elem: UniversalElement, h_current, p_current):
    jacobians = []
    interpolated_temp_list = []
    nodes_temp = element.nodes_temperature()
    c_current = np.zeros((4, 4))

    for integration_point in range(4):
        jacobians.append(uni_elem.create_jacobian_matrix(element, integration_point))
        shape_fun_dx = []
        shape_fun_dy = []
        interpolated_temp = 0

        for shape_fun_num in range(4):
            shape_fun_dx.append(calc_shape_fun_dx(uni_elem, jacobians[integration_point], integration_point, shape_fun_num))
            shape_fun_dy.append(calc_shape_fun_dy(uni_elem, jacobians[integration_point], integration_point, shape_fun_num))
            interpolated_temp += nodes_temp[shape_fun_num] * uni_elem.shape_fun_matrix[integration_point][shape_fun_num]
        interpolated_temp_list.append(interpolated_temp)

        for shape_fun_vertic in range(4):
            for shape_fun_horiz in range(4):
                c_current[shape_fun_vertic][shape_fun_horiz] = GlDt.specific_heat \
                                                               * GlDt.density \
                                                               * uni_elem.shape_fun_matrix[integration_point][shape_fun_vertic] \
                                                               * uni_elem.shape_fun_matrix[integration_point][shape_fun_horiz] \
                                                               * np.linalg.det(jacobians[integration_point])
                h_current[shape_fun_vertic][shape_fun_horiz] += GlDt.conductivity \
                                                                * (shape_fun_dx[shape_fun_vertic]
                                                                   * shape_fun_dx[shape_fun_horiz]
                                                                   + shape_fun_dy[shape_fun_vertic]
                                                                   * shape_fun_dy[shape_fun_horiz]) \
                                                                * np.linalg.det(jacobians[integration_point]) \
                                                                + c_current[shape_fun_vertic][shape_fun_horiz] \
                                                                / GlDt.simulation_step_time
                p_current[shape_fun_horiz] += c_current[shape_fun_vertic][shape_fun_horiz] \
                                              / GlDt.simulation_step_time \
                                              * interpolated_temp_list[integration_point]


def calc_for_integration_point_on_surface(element: Element, uni_elem: UniversalElement, h_current, p_current):
    for surf in range(element.amount_of_surface_with_bc):
        id = element.id_of_surface_with_bc[surf]
        node1 = element.surfaces[id].__getitem__(0)
        node2 = element.surfaces[id].__getitem__(1)
        det = det_jacobian_1d(node1, node2)

        for integration_point in range(2):
            for shape_fun_vertic in range(4):
                for shape_fun_horiz in range(4):
                    h_current[shape_fun_vertic][shape_fun_horiz] += GlDt.alpha \
                                                                    * uni_elem.shape_fun_surf_matrices[id][integration_point][shape_fun_vertic] \
                                                                    * uni_elem.shape_fun_surf_matrices[id][integration_point][shape_fun_horiz] \
                                                                    * det
                p_current[shape_fun_vertic] += GlDt.alpha \
                                               * GlDt.ambient_temperature \
                                               * uni_elem.shape_fun_surf_matrices[id][integration_point][shape_fun_vertic] \
                                               * det


def agregate_to_h_and_p_global_matrices(element: Element, h_current, p_current, h_global, p_global):
    for shape_fun_vertic in range(4):
        for shape_fun_horiz in range(4):
            h_global[element.nodes_id()[shape_fun_vertic]][element.nodes_id()[shape_fun_horiz]] += \
                h_current[shape_fun_vertic][shape_fun_horiz]
        p_global[element.nodes_id()[shape_fun_vertic]] += p_current[shape_fun_vertic]


def solve():
    uni_elem = UniversalElement()
    h_global = np.zeros((GlDt.nodes_number, GlDt.nodes_number))
    p_global = np.zeros(GlDt.nodes_number)
    for element in grid.elements:
        h_current = np.zeros((4, 4))
        p_current = np.zeros(4)
        calc_for_integration_point(element, uni_elem, h_current, p_current)
        calc_for_integration_point_on_surface(element, uni_elem, h_current, p_current)
        agregate_to_h_and_p_global_matrices(element, h_current, p_current, h_global, p_global)
    return h_global, p_global


def set_nodes_temperature(temperature):
    for node, temp in zip(grid.nodes, temperature):
        node.temp = temp


grid = Grid()
