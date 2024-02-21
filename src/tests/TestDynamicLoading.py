
# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task

#libs imports

#lucrezia imports
from grid.LoadPoint import LoadPoint
from grid.KeyboardMovable import KeyboardMovable

#from utils.once import Once
from utils.misc import Misc

from tests.Test import Test

class TestDynamicLoading(Test, KeyboardMovable):
    def __init__(self):

        #spawn current main menu
        # mainMenu = MainMenu(lang)
        self.myLP = LoadPoint(render, 'test', Point3(0,0,0), 2)
        self.myLP.setVisible(True)

        #spawn dev map through new map paradigm
        gridManager.add('camera.map', 'prova1', 'dynamic', 2)

        #uncomment to test against offset map
        gridManager.get('prova1').setPos(Point3(2,3,0))

        #print(gridManager.add('test.map', 'prova2'))
        gridManager.addLoadPoint(self.myLP)
        #gridManager.addLoadPoint(LoadPoint('test2', Point3(5,7,0), 1))

        self.setMovableNode(self.myLP)
        self.setMovable(True)
        #self.setMovableSpeed(0.8)

