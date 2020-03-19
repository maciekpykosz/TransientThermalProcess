from global_system.Node import Node


class Surface(object):
    def __init__(self, id: int, node1: Node, node2: Node):
        self.__id = id
        self.__nodes = [node1, node2]
        self.__boundary_condition = None

        # Określamy czy krawędź zawiera warunki brzegowe
        if self.__nodes[0].boundary_condition and self.__nodes[1].boundary_condition:
            self.__boundary_condition = True
        else:
            self.__boundary_condition = False

    @property
    def nodes(self):
        return self.__nodes

    @property
    def id(self):
        return self.__id

    @property
    def boundary_condition(self):
        return self.__boundary_condition

    def __getitem__(self, item):
        return self.__nodes[item]
