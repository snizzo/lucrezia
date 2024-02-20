
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

class TestKeyboardMovable(Test, KeyboardMovable):
    def __init__(self):
        
        # create new empty nodepath
        pht_np = render.attachNewNode("placeholder_test")
        # create placeholder object
        pht = Placeholder(pht_np)
        pht.setParent(pht_np)

        self.setMovableNode(pht_np)
        self.setMovable(True, 0.1)