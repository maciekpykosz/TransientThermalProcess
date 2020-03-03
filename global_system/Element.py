from global_system.Node import Node
from global_system.Surface import Surface


class Element(object):
    def __init__(self, id: int, nodes: [Node]):
        self.__id = id
        self.__nodes = nodes
        self.__surfaces = []
        self.__amount_of_surface_with_bc = 0

        # Wyznaczamy krawędzie elementu
        self.__surfaces = [Surface(0, self.__nodes[3], self.__nodes[0]),
                           Surface(1, self.__nodes[0], self.__nodes[1]),
                           Surface(2, self.__nodes[1], self.__nodes[2]),
                           Surface(3, self.__nodes[2], self.__nodes[3])]

        # Wyznaczamy ilość krawędzi, na których zachodzą warunki brzegowe, w danym elemencie
        for surf in self.__surfaces:
            if surf.boundary_condition:
                self.__amount_of_surface_with_bc += 1

    @property
    def amount_of_surface_with_bc(self):
        return self.__amount_of_surface_with_bc

    @property
    def nodes(self):
        return self.__nodes
