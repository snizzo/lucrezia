#panda3d
from panda3d.core import NodePath, LPoint2i
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *

#internals
from utils.toggle import Toggle
from utils.once import Once
from objects.grass import Grass
from objects.light import Light
from tile import Tile
from character import Character

from utils.fadeout import FadeOut

import os, sys

'''
This class abstracts the 2D grid commoly used in 2D games
to use with panda3d.

INTERNAL TILESET EXAMPLE GRAPH:
  ^
  |
  |
y |
  |
  |
  O------------>
        x
'''
class ChangeMapAnimations(DirectObject):
    '''
    Autogenerates empty tileset at start
    '''
    def __init__(self):
        pass
