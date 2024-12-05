
# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task

#lucrezia imports
from grid.StaticGrid import StaticGrid

#from utils.once import Once
from utils.misc import Misc

from tests.Test import Test

class TestCinematic1(Test):
    def __init__(self):

        #spawn dev map through new map paradigm
        gridManager.add('black.map', 'black', 'static')
        
        #uncomment to test against offset map
        gridManager.get('black').setPos(Point3(0,0,0))

