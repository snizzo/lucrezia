
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

class TestDynamicLoading(Test):
    def __init__(self):

        #spawn current main menu
        # mainMenu = MainMenu(lang)
        self.myLP = LoadPoint('test', Point3(0,0,0), 2)

        #spawn dev map through new map paradigm
        gridManager.add('camera.map', 'prova1', 'dynamic', 2)
        gridManager.get('prova1').setPos(Point3(2,3,0))
        #print(gridManager.add('test.map', 'prova2'))
        gridManager.addLoadPoint(self.myLP)
        #gridManager.addLoadPoint(LoadPoint('test2', Point3(5,7,0), 1))

        # self.accept("k", lambda:None)
        self.accept("k", self.test)
        self.accept("p", self.pushtest)
        self.accept("p-up", self.releasetest)

    def test(self):
        currentgrid = gridManager.get('prova1')

        currentgrid.stash() if not currentgrid.stashed else currentgrid.unstash()
    
    def pushtest(self):
        print("adding test...")
        taskMgr.add(self.test2, "test2")

    def releasetest(self):
        print("removing test...")
        taskMgr.remove("test2")

    def test2(self, task):
        deltatime = Misc.getDeltaTime()
        self.myLP.move(Point3(0.5*deltatime,0,0))
        return Task.cont