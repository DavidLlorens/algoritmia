from abc import abstractmethod, ABC


class Axis:
    X = 0
    Y = 1


class KDTree(ABC):
    @abstractmethod
    def pretty(self, level: int = 0) -> str: pass


class KDNode(KDTree):
    def __init__(self, axis: Axis, split_value: float, child1: KDTree, child2: KDTree):
        self.axis = axis  # Eje utilizado para separar sus hijos (Axis.X o Axis.Y)
        self.split_value = split_value  # Coordenada x o y (depende de axis)
        self.child1 = child1  # Hijo izquierdo o superior (Coordenada x o y (depende de axis) < split_value)
        self.child2 = child2  # Hijo dererecho o inferior (Coordenada x o y (depende de axis) >= split_value)

    def pretty(self, level: int = 0) -> str:
        return "       " * level + f"KDNode({self.axis}, {self.split_value},\n" + \
               self.child1.pretty(level + 1) + ",\n" + self.child2.pretty(level + 1) + "\n" + \
               "       " * level + ")"


class KDLeaf(KDTree):
    def __init__(self, point: tuple[float, float]):
        self.point = point

    def pretty(self, level: int = 0) -> str:
        return "       " * level + "KDLeaf({0})".format(self.point)
