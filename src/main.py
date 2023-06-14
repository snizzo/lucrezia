#panda imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import OrthographicLens, LightRampAttrib
from panda3d.core import loadPrcFileData, LPoint2i, Point3
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
""")


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        
        self.editormode = False
        
        base.win.setClearColor((0, 0, 0, 1))
        base.win.setClearColorActive(True)
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
        base.oobe()
        
        #filters -- experimental
        filters = CommonFilters(base.win, base.cam)
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
        __builtins__.myfilters = filters

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

        # parsing commandline arguments (runtest)
        parser = argparse.ArgumentParser(description='Simple program with command-line argument.')
        parser.add_argument('-t', '--runtest', default=None, action="store", help='Specify a string for the runtest argument.')
        args = parser.parse_args()

        testName = args.runtest

        if testName is not None:
            Tests.runTest(testName)

    def ping (self):
        print("main: PONG!")
        
app = MyApp()
app.run()
