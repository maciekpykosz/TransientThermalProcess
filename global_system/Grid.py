from global_system import GlobalData as GlDt
from global_system.Element import Element
from global_system.Node import Node


class Grid(object):
    def __init__(self):
        self.__nodes = []
        self.__elements = []

        # Tworzenie węzłów
        node_id = 0
        for i in range(GlDt.nodes_number_for_width):
            for j in range(GlDt.nodes_number_for_height):
                self.__nodes.append(Node(node_id,
                                         i * GlDt.distance_between_nodes_for_width,
                                         j * GlDt.distance_between_nodes_for_height))
                node_id += 1

        # Tworzenie elementów
        element_id = 0
        for i in range(GlDt.nodes_number_for_width - 1):
            for j in range(GlDt.nodes_number_for_height - 1):
                node_id = GlDt.nodes_number_for_height * i + j
                self.__elements.append(Element(element_id,
                                               [self.__nodes[node_id],
                                                self.__nodes[node_id + GlDt.nodes_number_for_height],
                                                self.__nodes[node_id + GlDt.nodes_number_for_height + 1],
                                                self.__nodes[node_id + 1]]))
                element_id += 1

    @property
    def elements(self):
        return self.__elements

    @property
    def nodes(self):
        return self.__nodes
