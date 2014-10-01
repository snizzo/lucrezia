#panda imports
from direct.showbase.ShowBase import ShowBase

#libs imports
import __builtin__

#lucrezia imports
from grid.grid import Grid
#from utils.once import Once

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        
        #defining global variables
        # TAKE CARE: these must be objects created form classes which
        # structure has been built with globalness in mind!!
        #
        # for completeness: add minus 'p' before class name for naming variables
        __builtin__.pGrid = Grid()
        
        
        
app = MyApp()
app.run()
