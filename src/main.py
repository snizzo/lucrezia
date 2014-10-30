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
from extract.extract import ExtractTitle
from configmanager.configmanager import Configmanager
from audio.audioManager import AudioManager
from gui.menuParent import MenuParent
from camera.camera import CustomCamera
from utils.fadeout import FadeOut

__builtin__.resourceManager = ResourceManager()
__builtin__.configmanager = Configmanager()
#configmanager.loadConfig()

#fullscreen e grandezza finestra
loadPrcFileData("","""
fullscreen 0
win-size 1366 768
text-encoding utf8
show-frame-rate-meter 1
sync-video #f
""")

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        
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
        
        #defining global variables
        # TAKE CARE: these must be objects created form classes which
        # structure has been built with globalness in mind!!
        #
        # for completeness: add minus 'p' before class name for naming variables
        __builtin__.pGrid = Grid()
        __builtin__.extract = ExtractTitle()
        #__builtin__.configmanager = Configmanager() 
        __builtin__.audioManager = AudioManager()
        __builtin__.customCamera = CustomCamera()

        # ===========================================
        #load the config class
        #configmanager.loadConfig()
        #lang = configmanager.getData("LANGUAGE").lower()
        # ===========================================
                 
        __builtin__.manuParent = MenuParent(lang)         
        
        lang = configmanager.getData("LANGUAGE").lower()
                 
	pGrid.loadMap(resourceManager.getResource("Mappe/camera.map"))
        
        #extract.extractTxt("ita")
        extract.extractTxt(lang)
        #DEBUG for the getResource
        #print resourceManager.getResource("misc/grass.png")
        
        configmanager.saveConfig("LANGUAGE","ITA")
        lang = configmanager.getData("LANGUAGE").lower()
        print "====="
        print lang
        extract.extractTxt(lang)
        
        """  
        r = ResourceManager()
        print r.getResource('misc/grass') # deve dire path assoluto = res/misc/grass.png
        """
        #f= FadeOut()
        audioManager.playMusic("misc/bgmusic.ogg")
        audioManager.playEffect("misc/car.ogg")
        audioManager.playEffect("misc/car.ogg")
        
app = MyApp()
app.run()
