
# copy paste imports from main.py
#panda imports
from panda3d.core import Point3
from direct.task import Task

#libs imports

#lucrezia imports
from grid.KeyboardMovable import KeyboardMovable

#from utils.once import Once
from utils.misc import Misc

from tests.Test import Test

class TestStaticLoading(Test):
    def __init__(self):

        #spawn dev map through new map paradigm
        gridManager.add('camera.map', 'prova1', 'static', 2)

        #uncomment to test against offset map
        gridManager.get('prova1').setPos(Point3(5,0,6))

