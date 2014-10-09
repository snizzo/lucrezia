#panda imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import OrthographicLens
from panda3d.core import loadPrcFileData

#libs imports
import __builtin__
import os

#lucrezia imports
from grid.grid import Grid
#from utils.once import Once
from parser.parser import Parser
from resourcemanager.resourcemanager import ResourceManager
from extract.extract import Extract

#fullscreen e grandezza finestra
loadPrcFileData("","""
fullscreen 0
win-size 1024 768
text-encoding utf8
show-frame-rate-meter 1
sync-video #t
""")

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        
        '''
        #ortho camera lens
        lens = OrthographicLens()
        lens.setFilmSize(12, 9)  #TODO: quattro terzi, fixare, spostare tutto nella classe telecamera e adattare in base allo schermo utente
        base.cam.node().setLens(lens)
        base.cam.setY(-5)
        base.cam.setP(-355)
        '''
        
        #defining global variables
        # TAKE CARE: these must be objects created form classes which
        # structure has been built with globalness in mind!!
        #
        # for completeness: add minus 'p' before class name for naming variables
        __builtin__.pGrid = Grid()
        __builtin__.resourceManager = ResourceManager() 
        __builtin__.extract = Extract()
        
        pGrid.loadMap('example.map')
        
        extract.extract_Txt("ita")
        extract.extract_Txt("ing")
        
        print resourceManager.getResource("misc/grass.png")
        """
        r = ResourceManager()
        print r.getResource('misc/grass') # deve dire path assoluto = res/misc/grass.png
        """
        
        
app = MyApp()
app.run()
