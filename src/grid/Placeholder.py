# pylint: disable=undefined-variable, global-variable-not-assigned

# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task
from direct.showbase.ShowBase import ShowBase


from geometries.PrimitiveBox import PrimitiveBox
from geometries.PrimitiveSphere import PrimitiveSphere
from geometries.ColorCodes import ColorCodes

#lucrezia imports
from grid.Entity import Entity

class PlaceHolder(Entity):
    def __init__(self, parent = None):

        self.sphere = PrimitiveSphere(size=1.0)
        self.sphere.setWireframe(False)
        self.setColor("red")  # Set color to orange

        if parent != None:
            self.setParent(parent)
    
    def setParent(self, parent):
        self.sphere.reparentTo(parent)
        self.sphere.setPos(0, 0, 0) # root relative to the parent
        self.sphere.setVisible(True)

        # get panda3d bounding box
        bb = parent.getBounds()
        radius = bb.getRadius()
        self.sphere.setScale(radius, radius, radius)
    
    def setColor(self, color):
        self.sphere.setColor(ColorCodes.get(color))
        self.sphere.setAlpha(0.5)

