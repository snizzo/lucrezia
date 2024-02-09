
# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task

#libs imports

#lucrezia imports
from grid.LoadPoint import LoadPoint
from grid.Placeholder import PlaceHolder

#from utils.once import Once
from utils.misc import Misc

from tests.Test import Test

class TestPlaceholder(Test):
    def __init__(self):
        
        # create new empty nodepath
        pht_np = render.attachNewNode("placeholder_test")
        # create placeholder object
        pht = PlaceHolder(pht_np)
        pht.setParent(pht_np)


        # mainMenu = MainMenu(lang)
        self.myLP = LoadPoint('test', Point3(5,5,5), 2)
        self.myLP.reparentTo(render)
        self.myLP.setVisible(False)
        pht.setParent(self.myLP.node)

        # move only in x and z direction (to the front of the camera)
        self.accept('arrow_up', self.move, [0,0,1]) # up
        self.accept('arrow_down', self.move, [0,0,-1]) # down
        self.accept('arrow_left', self.move, [-1,0,0]) # left
        self.accept('arrow_right', self.move, [1,0,0]) # right
    
    def move(self, directionX, directionY, directionZ):
        # z-up i suppose
        originalX = self.myLP.getPos().getX()
        originalY = self.myLP.getPos().getY()
        originalZ = self.myLP.getPos().getZ()
        self.myLP.getNode().setPos(originalX+directionX,originalY+directionX,originalZ+directionZ)