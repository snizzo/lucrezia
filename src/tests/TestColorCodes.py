# pylint: disable=undefined-variable, global-variable-not-assigned

# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task
from direct.showbase.ShowBase import ShowBase

#libs imports

#lucrezia imports
from grid.LoadPoint import LoadPoint
from geometries.PrimitiveBox import PrimitiveBox
from geometries.ColorCodes import ColorCodes

#from utils.once import Once
from utils.misc import Misc

from tests.Test import Test


class TestColorCodes(Test):
    def __init__(self):
        Test.__init__(self)

        self.box = box = PrimitiveBox(size=1.0)
        box.setWireframe(True)

        # Set the position, scale, and color of the box
        box.setPosition(0, 0, 0)
        box.setScale(2, 2, 2)

        # can change color to the primitive
        box.setColor(ColorCodes.get("cyan"))  # Set color to orange

        # Reparent the box to the render node
        box.node_path.reparentTo(render)