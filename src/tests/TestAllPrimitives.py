
# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task

#libs imports

#lucrezia imports
from grid.LoadPoint import LoadPoint
from geometries.PrimitiveBox import PrimitiveBox
from geometries.PrimitiveSphere import PrimitiveSphere

#from utils.once import Once
from utils.misc import Misc

from tests.Test import Test



class TestAllPrimitives(Test):
    def __init__(self):
        Test.__init__(self)

        nitems = 2
        distances = [i for i in range(0, nitems*4, 4)]

        box = PrimitiveBox(size=1.0)
        box.setWireframe(True)

        # Set the position, scale, and color of the box
        box.setPosition(distances.pop(), 0, 0)
        box.setScale(1.5, 1.5, 1.5)
        box.setColor(1.0, 0.5, 0.2)  # Set color to orange

        # Reparent the box to the render node
        box.node_path.reparentTo(render)

        sphere = PrimitiveSphere(size=1.0)
        sphere.setWireframe(True)

        # Set the position, scale, and color of the sphere
        sphere.setPosition(distances.pop(), 0, 0)
        sphere.setScale(1.5, 1.5, 1.5)
        sphere.setColor(1.0, 0.5, 0.2)  # Set color to orange

        # Reparent the sphere to the render node
        sphere.node_path.reparentTo(render)