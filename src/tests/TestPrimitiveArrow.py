
# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task

#libs imports

from geometries.PrimitiveArrow import PrimitiveArrow

from tests.Test import Test



class TestPrimitiveArrow(Test):
    def __init__(self):
        Test.__init__(self)

        arrow = PrimitiveArrow(size=1.0)
        arrow.setWireframe(True)

        # Set the position, scale, and color of the arrow
        arrow.setPosition(0, 0, 0)
        arrow.setScale(2, 2, 2)
        arrow.setColor(1.0, 0.5, 0.2)  # Set color to orange

        # Reparent the arrow to the render node
        arrow.node_path.reparentTo(render)