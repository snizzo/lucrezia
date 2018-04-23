#panda imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import OrthographicLens, LightRampAttrib
from panda3d.core import loadPrcFileData
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenImage import OnscreenImage

#libs imports
import __builtin__
import os

#lucrezia imports
from grid.grid import Grid

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

__builtin__.resourceManager = ResourceManager()
__builtin__.configManager = ConfigManager()
#configmanager.loadConfig()

#fullscreen e grandezza finestra
loadPrcFileData("","""
gl-debug false
fullscreen 0
win-size 1280 800
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
        #base.oobe()
        
        #filters -- experimental
        filters = CommonFilters(base.win, base.cam)
        
        #defining global variables
        # TAKE CARE: these must be objects created form classes which
        # structure has been built with globalness in mind!!
        #
        # for completeness: add minus 'p' before class name for naming variables
        __builtin__.main = self
        __builtin__.pGrid = Grid()
        __builtin__.extract = ExtractTitle()
        __builtin__.baloons = BaloonManager()
        #__builtin__.configManager = ConfigManager()
        __builtin__.audioManager = AudioManager()
        __builtin__.fadingtext = FadingTextManager()
        __builtin__.customCamera = CustomCamera()
        __builtin__.script = Script()
        __builtin__.persistence = Persistence()
        __builtin__.fademanager = FadeOut()
        __builtin__.flow = Flow()
        __builtin__.myfilters = filters

        # ===========================================
        #load the config class
        #configmanager.loadConfig()
        #lang = configmanager.getData("LANGUAGE").lower()
        # ===========================================
                 
        __builtin__.mainMenu = MainMenu(lang)
        
        lang = configManager.getData("LANGUAGE").lower()
        
        #extract.extractTxt("ita")
        extract.extractTxt(lang)
        #DEBUG for the getResource
        #print resourceManager.getResource("misc/grass.png")
        
        configManager.saveConfig("LANGUAGE","ITA")
        lang = configManager.getData("LANGUAGE").lower()
        extract.extractTxt(lang)
        
        """
        r = ResourceManager()
        print r.getResource('misc/grass') # deve dire path assoluto = res/misc/grass.png
        """
        
        #self.entrypoint = ['finedemo.map', '1,1']
        #self.entrypoint = ['parcogiochi.map', '9,12']
        #self.entrypoint = ['incidente.map', '20,11']
        #self.entrypoint = ['macchinadasola.map', '2,2']
        #self.entrypoint = ['black.map', '5,5']
        self.entrypoint = ['tetto.map', '4,2']
        mainMenu.show()
        
        
        #UNCOMMENT TO ENABLE INTRO
        #i = Intro()
        #i.start()
        persistence.save("blackstate", 1)

    def ping (self):
        print "main: PONG!"
        
app = MyApp()
app.run()
