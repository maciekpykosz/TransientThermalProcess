from global_system import GlobalData


class Node(object):
    def __init__(self, id: int, x: float, y: float):
        self.__id = id
        self.__x = x
        self.__y = y
        self.__temp = GlobalData.initial_temperature
        self.__boundary_condition = None

        # Określamy czy wezeł zawiera warunki brzegowe
        if self.__x == 0.0 or self.__x >= GlobalData.width or self.__y == 0.0 or self.__y >= GlobalData.height:
            self.__boundary_condition = True
        else:
            self.__boundary_condition = False

    @property
    def id(self):
        return self.__id

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def temp(self):
        return self.__temp

    @temp.setter
    def temp(self, value):
        self.__temp = value

    @property
    def boundary_condition(self):
        return self.__boundary_condition
