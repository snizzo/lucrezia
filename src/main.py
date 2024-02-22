#panda imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import OrthographicLens, LightRampAttrib
from panda3d.core import loadPrcFileData, LPoint2i, Point3
from panda3d.core import WindowProperties
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenImage import OnscreenImage
from direct.task import Task

#libs imports
import builtins
import os
import argparse

#lucrezia imports
from grid.grid import Grid
from grid.GridManager import GridManager
from grid.LoadPoint import LoadPoint

#from utils.once import Once
from parser.parser import Parser
from resourcemanager.resourcemanager import ResourceManager
from extract.extract import ExtractTitle
from configmanager.configmanager import ConfigManager
from audio.audioManager import AudioManager
from gui.menuParent import MainMenu
from gui.baloonmanager import BaloonManager
from gui.fadingtext import FadingTextManager
from camera.camera import CustomCamera
from utils.fadeout import FadeOut
from intro.intro import Intro
from script.script import Script
from persistence.persistence import Persistence
from cinematics.flow import Flow
from utils.misc import Misc
from tests.Tests import Tests

__builtins__.resourceManager = ResourceManager()
__builtins__.configManager = ConfigManager(resourceManager)
#configmanager.loadConfig()

#fullscreen e grandezza finestra
loadPrcFileData("","""
gl-debug false
fullscreen 0
win-size 800 600
text-encoding utf8
show-frame-rate-meter 0
sync-video #t
framebuffer-srgb #t
window-type none
""")


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # dryRun is a flag to avoid the instantiation of the 3d window if not necessary
        # false -> 3d window is instantiated
        # true -> 3d window is instantiated offscreen, without support for oobe
        self.dryRun = False

        # editormode is a flag to enable the editor mode, with various adjustments to workflow
        # and mechanics disabled. Has to be set to true only in editor.py
        # false -> editor mode is disabled
        # true -> editor mode is enabled
        self.editormode = False

        # windowType is a flag to set the type of window to be instantiated
        # onscreen -> 3d window is instantiated
        # none -> 3d window is not instantiated
        # offscreen -> 3d window is instantiated but not shown
        self.windowType = 'onscreen'

        # preparsing commandline arguments (runtest) before showbase constructor to avoid the instantiation of the 3d window if not necessary
        # for cli operations
        parser = argparse.ArgumentParser(description='Panda3D RPG cli mode')
        parser.add_argument('-t', '--runtest', default=None, action="store", help='Specify a string for the runtest argument.')
        parser.add_argument('-lt', '--listtest', default=False, action="store_true", help='List all available tests')
        args = parser.parse_args()

        # list the args that forces a dry (offscreen) run, like list tests
        if args.listtest == True:
            self.dryRun = True
            self.windowType = 'offscreen'

        self.load3DWindow(self.windowType)

        lang="ita"

        runTest = True

        '''
        #ortho camera lens
        lens = OrthographicLens()
        lens.setFilmSize(12, 9)  #TODO: quattro terzi, fixare, spostare tutto nella classe telecamera e adattare in base allo schermo utente
        base.cam.node().setLens(lens)
        base.cam.setY(-5)
        base.cam.setP(-355)
        '''
        
        #enabling shader system (and ppl)
        render.setShaderAuto()

        # all the world is instantiated correctly and rendered offscreen but oobe specifically breaks windowType offscreen
        if self.dryRun!=True:
            base.oobe()
        
        #filters -- experimental
        #filters = CommonFilters(base.win, base.cam)
        #filters.setAmbientOcclusion()
        
        #defining global variables
        __builtins__.main = self                       #everyone can access the main class
        __builtins__.gridManager = GridManager()       #manages grids around the world
        __builtins__.extract = ExtractTitle()
        __builtins__.baloons = BaloonManager()
        #__builtins__.configManager = ConfigManager()
        __builtins__.audioManager = AudioManager()
        __builtins__.fadingtext = FadingTextManager()
        __builtins__.customCamera = CustomCamera()
        __builtins__.script = Script()
        __builtins__.persistence = Persistence()
        __builtins__.fademanager = FadeOut()
        __builtins__.flow = Flow()
        #__builtins__.myfilters = filters

        # set this to true to enable debug mode
        __builtins__.debug = True
        # issue 9
        # __builtins__.pGrid = lambda: gridManager.get(0)

        # ===========================================
        #load the config class
        #configmanager.loadConfig()
        #lang = configmanager.getData("LANGUAGE").lower()
        # ===========================================
                 
        
        
        lang = configManager.getData("LANGUAGE").lower()
        
        #extract.extractTxt("ita")
        extract.extractTxt(lang)
        #DEBUG for the getResource
        #print(resourceManager.getResource("misc/grass.png"))
        
        configManager.saveConfig("LANGUAGE","ITA")
        

        # test dev map
        self.entrypoint = ['test.map', '3,3']
        
        #UNCOMMENT TO ENABLE INTRO
        #i = Intro()
        #i.start()

        # argument parsing effects
        self.runTest(args.runtest)
        self.listTests(args.listtest)

    def runTest(self, testName):
        if testName is not None:
            t = Tests()
            t.autoImport()
            t.runTest(testName)
    
    def listTests(self,listTest=False):
        if listTest is True:
            t = Tests()
            t.autoImport()
            t.listTests()
    
    def load3DWindow(self, windowType = 'onscreen'):
        '''
        Panda3d starts with a dry mode (without any 3d window active).

        Instantiates the 3d window and sets the background color
        '''
        base.windowType = windowType
        wp = WindowProperties.getDefault()
        base.openDefaultWindow(props = wp)

        base.win.setClearColor((0, 0, 0, 1))
        base.win.setClearColorActive(True)

    def isDryRun(self):
        return self.dryRun


    def ping (self):
        print("main: PONG!")
        

app = MyApp()
if not app.isDryRun():
    app.run()
