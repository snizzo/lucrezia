
# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task

#libs imports

#lucrezia imports
from grid.LoadPoint import LoadPoint
from grid.Placeholder import Placeholder
from grid.KeyboardMovable import KeyboardMovable

#from utils.once import Once
from utils.misc import Misc

from tests.Test import Test

class TestPlaceholder(Test, KeyboardMovable):
    def __init__(self):
        
        # create new empty nodepath
        pht_np = render.attachNewNode("placeholder_test")
        # create placeholder object
        pht = Placeholder(pht_np)
        pht.setParent(pht_np)


        # mainMenu = MainMenu(lang)
        self.myLP = LoadPoint(render, 'test', Point3(5,5,5), 2)
        self.myLP.setVisible(False)
        pht.setParent(self.myLP.node)

        self.setMovableNode(self.myLP)
        self.setMovable(True, speed=0.8)

        self.accept("t", self.toggleVisible)

    def toggleVisible(self):
        self.myLP.setVisible(not self.myLP.isVisible())
        print("toggleVisible")