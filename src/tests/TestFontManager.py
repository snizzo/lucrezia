# pylint: disable=undefined-variable, global-variable-not-assigned

# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from grid import Placeholder

#libs imports

#lucrezia imports
from grid.LoadPoint import LoadPoint
from geometries.PrimitiveBox import PrimitiveBox
from geometries.ColorCodes import ColorCodes
from grid.Placeholder import Placeholder

#from utils.once import Once
from utils.misc import Misc

from tests.Test import Test


class TestFontManager(Test):
    def __init__(self):
        Test.__init__(self)

        self.node = render.attachNewNode("testnode")

        self.placeholder = Placeholder(self.node, 1.0, "cyan")
        self.placeholder.reparentTo(self.node)
        self.placeholder.setColor("cyan")
        self.placeholder.setLabel("test label")