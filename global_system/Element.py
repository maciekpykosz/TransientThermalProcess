from global_system.Node import Node
from global_system.Surface import Surface


class Element(object):
    def __init__(self, id: int, nodes: [Node]):
        self.__id = id
        self.__nodes = nodes
        self.__amount_of_surface_with_bc = 0
        self.__id_of_surface_with_bc = []

        # Wyznaczamy krawędzie elementu
        self.__surfaces = [Surface(0, self.__nodes[3], self.__nodes[0]),
                           Surface(1, self.__nodes[0], self.__nodes[1]),
                           Surface(2, self.__nodes[1], self.__nodes[2]),
                           Surface(3, self.__nodes[2], self.__nodes[3])]

        # Wyznaczamy ilość krawędzi, na których zachodzą warunki brzegowe, w danym elemencie oraz listę id tych krawędzi
        for surf in self.__surfaces:
            if surf.boundary_condition:
                self.__amount_of_surface_with_bc += 1
                self.__id_of_surface_with_bc.append(surf.id)

    @property
    def amount_of_surface_with_bc(self):
        return self.__amount_of_surface_with_bc

    @property
    def id_of_surface_with_bc(self):
        return self.__id_of_surface_with_bc

    @property
    def nodes(self):
        return self.__nodes

    @property
    def surfaces(self):
        return self.__surfaces

    def nodes_coordinates(self):
        x = [node.x for node in self.__nodes]
        y = [node.y for node in self.__nodes]
        return x, y

    def nodes_temperature(self):
        temp = [node.temp for node in self.__nodes]
        return temp

    def nodes_id(self):
        id = [node.id for node in self.__nodes]
        return id