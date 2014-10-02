#panda imports
from direct.showbase.ShowBase import ShowBase

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
        
        #defining global variables
        # TAKE CARE: these must be objects created form classes which
        # structure has been built with globalness in mind!!
        #
        # for completeness: add minus 'p' before class name for naming variables
        __builtin__.pGrid = Grid()
        
        p = Parser('parser/example.data')
        
        r = ResourceManager()
        print r.getResource('misc/grass') # deve dire path assoluto = res/misc/grass.png
        
        
        
app = MyApp()
app.run()
