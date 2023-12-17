
# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task

#libs imports

from geometries.PrimitiveCone import PrimitiveCone

from tests.Test import Test



class TestPrimitiveCone(Test):
    def __init__(self):
        Test.__init__(self)

        cone = PrimitiveCone(size=1.0)
        cone.setWireframe(True)

        # Set the position, scale, and color of the cone
        cone.setPosition(0, 0, 0)
        cone.setScale(2, 2, 2)
        cone.setColor(1.0, 0.5, 0.2)  # Set color to orange

        # Reparent the cone to the render node
        cone.node_path.reparentTo(render)