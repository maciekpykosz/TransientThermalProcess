from math import sqrt

import numpy as np

from global_system.Element import Element
from local_system.Constants import shape_fun_2d, shape_fun_dksi_2d, shape_fun_deta_2d


class UniversalElement(object):
    def __init__(self):
        self.__ksi = 1. / sqrt(3.)
        self.__eta = 1. / sqrt(3.)

        self.__integration_points = ((-self.__ksi, -self.__eta),
                                     (self.__ksi, -self.__eta),
                                     (self.__ksi, self.__eta),
                                     (-self.__ksi, self.__eta))

        self.__surfaces_integration_points = []
        self.__surfaces_integration_points.append(((-1.0, self.__eta), (-1.0, -self.__eta)))
        self.__surfaces_integration_points.append(((-self.__ksi, -1.0), (self.__ksi, -1.0)))
        self.__surfaces_integration_points.append(((1.0, -self.__eta), (1.0, self.__eta)))
        self.__surfaces_integration_points.append(((self.__ksi, 1.0), (-self.__ksi, 1.0)))

        self.__shape_fun_matrix = np.zeros((4, 4))
        self.__shape_fun_surf_matrices = []
        self.__shape_fun_dksi_matrix = np.zeros((4, 4))
        self.__shape_fun_deta_matrix = np.zeros((4, 4))
        self.__jacobian_matrix = np.zeros((2, 2))

        self.__create_matrixes()

    @property
    def shape_fun_dksi_matrix(self):
        return self.__shape_fun_dksi_matrix

    @property
    def shape_fun_deta_matrix(self):
        return self.__shape_fun_deta_matrix\

    @property
    def shape_fun_matrix(self):
        return self.__shape_fun_matrix

    @property
    def shape_fun_surf_matrices(self):
        return self.__shape_fun_surf_matrices

    def __create_specific_matrix(self, matrix_name, fun_name):
        for integr_point_num, row in enumerate(matrix_name):
            for shape_fun_num, element in enumerate(row):
                np.put(row,
                       shape_fun_num,
                       fun_name[shape_fun_num](ksi=self.__integration_points[integr_point_num][0],
                                               eta=self.__integration_points[integr_point_num][1]))

    def __create_shape_fun_surf_matrices(self):
        for surf in range(4):
            self.__shape_fun_surf_matrix = np.zeros((2, 4))
            for integr_point_num, row in enumerate(self.__shape_fun_surf_matrix):
                for shape_fun_num, element in enumerate(row):
                    np.put(row,
                           shape_fun_num,
                           shape_fun_2d[shape_fun_num](ksi=self.__surfaces_integration_points[surf][integr_point_num][0],
                                                       eta=self.__surfaces_integration_points[surf][integr_point_num][1]))
            self.__shape_fun_surf_matrices.append(self.__shape_fun_surf_matrix)

    def __create_matrixes(self):
        self.__create_specific_matrix(self.__shape_fun_matrix, shape_fun_2d)
        self.__create_specific_matrix(self.__shape_fun_dksi_matrix, shape_fun_dksi_2d)
        self.__create_specific_matrix(self.__shape_fun_deta_matrix, shape_fun_deta_2d)
        self.__create_shape_fun_surf_matrices()

    def create_jacobian_matrix(self, el: Element, coordinates_num_of_integr_point):
        x, y = el.nodes_coordinates()
        self.__jacobian_matrix.itemset((0, 0), np.dot(self.__shape_fun_dksi_matrix[coordinates_num_of_integr_point],
                                                      np.array([x]).transpose())[0])
        self.__jacobian_matrix.itemset((0, 1), np.dot(self.__shape_fun_dksi_matrix[coordinates_num_of_integr_point],
                                                      np.array([y]).transpose())[0])
        self.__jacobian_matrix.itemset((1, 0), np.dot(self.__shape_fun_deta_matrix[coordinates_num_of_integr_point],
                                                      np.array([x]).transpose())[0])
        self.__jacobian_matrix.itemset((1, 1), np.dot(self.__shape_fun_deta_matrix[coordinates_num_of_integr_point],
                                                      np.array([y]).transpose())[0])
        return self.__jacobian_matrix
