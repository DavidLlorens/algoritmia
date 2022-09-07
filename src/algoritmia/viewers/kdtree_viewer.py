"""
Created on 19/11/2018

@author: David Llorens dllorens@uji.es
"""
import sys

from algoritmia.datastructures.kdtrees import Axis, KDTree, KDNode, KDLeaf
from easypaint import EasyPaint


class KDTreeViewer(EasyPaint):
    def __init__(self, kdtree: KDTree):
        EasyPaint.__init__(self)
        self.kdtree = kdtree

    def draw_kdtree(self, kdtree: KDTree, min_x: float, min_y: float, max_x: float, max_y: float):
        if isinstance(kdtree, KDLeaf):
            if kdtree.point is not None:
                self.create_point(kdtree.point[0], kdtree.point[1])
        elif isinstance(kdtree, KDNode):
            if kdtree.axis == Axis.X:
                self.create_line(kdtree.split_value, min_y, kdtree.split_value, max_y, 'red')
                self.draw_kdtree(kdtree.child1, min_x, min_y, kdtree.split_value, max_y)
                self.draw_kdtree(kdtree.child2, kdtree.split_value, min_y, max_x, max_y)
            else:
                self.create_line(min_x, kdtree.split_value, max_x, kdtree.split_value, 'red')
                self.draw_kdtree(kdtree.child1, min_x, min_y, max_x, kdtree.split_value)
                self.draw_kdtree(kdtree.child2, min_x, kdtree.split_value, max_x, max_y)
        else:
            raise TypeError("Wrong type on 'kdtree' parameter")

    def get_points(self, kdtree: KDTree) -> list[tuple[float, float]]:
        if isinstance(kdtree, KDLeaf):
            return [kdtree.point]
        elif isinstance(kdtree, KDNode):
            return self.get_points(kdtree.child1) + self.get_points(kdtree.child2)
        else:
            raise TypeError("Wrong type on 'kdtree' parameter")

    def on_key_press(self, keysym):
        if keysym in ['Return', 'Escape']:
            self.close()

    def main(self):
        points = self.get_points(self.kdtree)
        x = list(map(lambda p: p[0], points))
        y = list(map(lambda p: p[1], points))
        min_x, max_x = min(x), max(x)
        min_y, max_y = min(y), max(y)

        sizex = 800
        sizey = sizex * (max_y - min_y) / (max_x - min_x)

        b = (max_x - min_x) * 0.05  # el borde será el 5% del tamaño del eje x
        self.easypaint_configure(title='KDTreeViewer',
                                 background='white',
                                 size=(sizex, sizey),
                                 coordinates=(min_x - b, min_y - b, max_x + b, max_y + b))

        self.create_rectangle(min_x, min_y, max_x, max_y, 'red')
        self.draw_kdtree(self.kdtree, min_x, min_y, max_x, max_y)


if __name__ == '__main__':
    # sys.argv.append("kdtree1.txt")
    if len(sys.argv) != 2:
        print("Use: python3 kdtreeviewer.py <file-kdtree.txt>")
        sys.exit()

    with open(sys.argv[1]) as content_file:
        content = content_file.read()
    try:
        loaded_kdtree = eval(content)
        KDTreeViewer(loaded_kdtree).run()
    except Exception:
        print("ERROR: el fichero no contiene un kdtree es el formato requerido.")
