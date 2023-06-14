
# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task

#libs imports

#lucrezia imports
from grid.LoadPoint import LoadPoint
from geometries.PrimitiveBox import PrimitiveBox

#from utils.once import Once
from utils.misc import Misc

from tests.Test import Test



class TestPrimitiveBox(Test):
    def __init__(self):
        Test.__init__(self)

        box = PrimitiveBox(size=1.0)
        box.createBox()

        # Set the position, scale, and color of the box
        box.setPosition(0, 0, 0)
        box.setScale(2, 2, 2)
        box.setColor(1.0, 0.5, 0.2)  # Set color to orange

        # Reparent the box to the render node
        box.node_path.reparentTo(render)