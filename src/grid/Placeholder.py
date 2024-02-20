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

class Placeholder(Entity):
    def __init__(self, parent = None, size = None, color = "red") -> None:
        '''
        If size isn't set as a custom value, set it to 1.0 as a default value and calculate the bounding box of the parent node.
        If size has a custom value set, then keep it without using the bounding box.
        '''
        self.size = size

        if size == None:
            tempSize = 1.0
        else:
            tempSize = size

        self.node = render.attachNewNode("placeholder")
        
        self.sphere = PrimitiveSphere(tempSize)
        self.sphere.setWireframe(False)
        self.setColor(color)  # Set color to orange
        self.sphere.reparentTo(self.node)
        self.sphere.setVisible(True)

        if parent != None:
            self.setParent(parent)
    
    def setParent(self, parent):
        self.parent = parent
        self.node.reparentTo(parent)
        self.node.setPos(0, 0, 0) # root relative to the parent

        if self.size == None:
        # get panda3d bounding box
            self.adaptToBoundingSize()

    def adaptToBoundingSize(self):
        bb = self.parent.getBounds()
        radius = bb.getRadius()
        self.sphere.setScale(radius, radius, radius)

    def setColor(self, color):
        self.sphere.setColor(ColorCodes.get(color))
        self.sphere.setAlpha(0.5)

