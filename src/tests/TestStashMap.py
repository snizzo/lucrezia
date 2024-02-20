
# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task

#libs imports

#lucrezia imports
from grid.LoadPoint import LoadPoint

#from utils.once import Once
from utils.misc import Misc

from tests.Test import Test

class TestStashMap(Test):
    def __init__(self):

        #spawn current main menu
        # mainMenu = MainMenu(lang)
        self.myLP = LoadPoint(render, 'test', Point3(7,0,7), 3)
        self.myLP.setVisible(True)

        #spawn dev map through new map paradigm
        gridManager.add('camera.map', 'prova1', 'dynamic', 2)

        #uncomment to test against offset map
        gridManager.get('prova1').setPos(Point3(0,0,0))

        #print(gridManager.add('test.map', 'prova2'))
        gridManager.addLoadPoint(self.myLP)
        #gridManager.addLoadPoint(LoadPoint('test2', Point3(5,7,0), 1))

        # self.accept("k", lambda:None)
        self.accept("k", self.test)

    def test(self):
        currentgrid = gridManager.get('prova1')

        currentgrid.stash() if not currentgrid.isStashed() else currentgrid.unstash()