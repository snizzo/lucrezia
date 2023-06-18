
# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task

#libs imports

from geometries.PrimitiveSphere import PrimitiveSphere

from tests.Test import Test



class TestPrimitiveSphere(Test):
    def __init__(self):
        Test.__init__(self)

        sphere = PrimitiveSphere(size=1.0)
        sphere.setWireframe(True)

        # Set the position, scale, and color of the sphere
        sphere.setPosition(0, 0, 0)
        sphere.setScale(2, 2, 2)
        sphere.setColor(1.0, 0.5, 0.2)  # Set color to orange

        # Reparent the sphere to the render node
        sphere.node_path.reparentTo(render)