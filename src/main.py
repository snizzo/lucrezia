#panda imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import OrthographicLens

#libs imports
import __builtin__

#lucrezia imports
from grid.grid import Grid
#from utils.once import Once
from parser.parser import Parser
from resourcemanager.resourcemanager import ResourceManager

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        
        '''
        #ortho camera lens
        lens = OrthographicLens()
        lens.setFilmSize(16, 12)  #TODO: quattro terzi, fixare, spostare tutto nella classe telecamera e adattare in base allo schermo utente
        base.cam.node().setLens(lens)
        base.cam.setY(-5)
        base.cam.setP(-330)
        '''
        
        #defining global variables
        # TAKE CARE: these must be objects created form classes which
        # structure has been built with globalness in mind!!
        #
        # for completeness: add minus 'p' before class name for naming variables
        __builtin__.pGrid = Grid()
        
        pGrid.loadMap('example.map')
        
        r = ResourceManager()
        print r.getResource('misc/grass') # deve dire path assoluto = res/misc/grass.png
        
        
        
app = MyApp()
app.run()
