# pylint: disable=undefined-variable, global-variable-not-assigned

# copy paste imports from main.py
#panda imports
import dis
from panda3d.core import Point3
from direct.task import Task

#libs imports

#lucrezia imports
from grid.LoadPoint import LoadPoint
from geometries.PrimitiveBox import PrimitiveBox
from geometries.PrimitiveSphere import PrimitiveSphere
from geometries.PrimitiveCone import PrimitiveCone
from geometries.PrimitiveArrow import PrimitiveArrow

#from utils.once import Once
from utils.misc import Misc

from tests.Test import Test



class TestAllPrimitives(Test):
    def __init__(self):
        Test.__init__(self)

        self.y_offset = self.offset()

        self.addPrimitive(PrimitiveBox(size=1.0))
        self.addPrimitive(PrimitiveSphere(size=1.0))
        self.addPrimitive(PrimitiveCone(size=1.0))
        self.addPrimitive(PrimitiveArrow(size=1.0))

    def addPrimitive(self, primitive):
        primitive.setWireframe(False)

        # Set the position, scale, and color of the primitive
        primitive.setPosition(next(self.y_offset), 0, 0)
        primitive.setScale(1.5, 1.5, 1.5)
        primitive.setColor(1.0, 0.5, 0.2)
        primitive.setPPL(True)

        # Reparent the box to the render node
        primitive.node_path.reparentTo(render)
    
    def offset(self):
        num = 0
        while True:
            yield num
            num += 4
