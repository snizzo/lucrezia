import os
import shutil                   #for copyfile
import getpass                  #for user name of the pc
from panda3d.core import loadPrcFileData

from resourcemanager.resourcemanager import ResourceManager
from extract.extractor import Extractor

class ConfigManager:
    
    def __init__(self, resourceManager):
        #setting for the folders
        self.folderConfig = "config"                    #configurations
        self.folderLang = 'lang'                        #languages
        
        # take the user name of the current pc
        self.pc_name = getpass.getuser()
    
        # search the UserConfig file  
        # if there isn't... create a user config file from the DefaultConfig file
        if (os.path.exists(resourceManager.getResource(self.folderConfig + "/" + self.pc_name +"Config.var")))!= True :
            shutil.copyfile(resourceManager.getResource(self.folderConfig + "/" +"DefaultConfig.var"),resourceManager.getResource(self.folderConfig + "/" +self.pc_name+"Config.var"))
        
        # directory is the directory of the UserConfig file
        self.directory = resourceManager.getResource(self.folderConfig + "/" + self.pc_name +"Config.var")
        extractor = Extractor()
        
        # setting the list of all the config file
        self.config = extractor.extractText(self.directory)
     
        
    #DEBUG for the directory
    def getDirectory(self):
        return self.directory   
     
        
    # load the loadPrcFileData from the config file
    def loadConfig(self):
        loadPrcFileData("","""
        fullscreen """ + self.getData("FULL_SCREEN") + """
        win-size """ + self.getData("RESOLUTION") + """
        text-encoding """ + self.getData("TEXT_ENCODING") + """
        show-frame-rate-meter """ + self.getData("FRAME_METER") + """
        sync-video """ + self.getData("SYNC_VIDEO") + """
        """)

    # ===========================================
    # loader config variables
    #DEBUG for getting the data
    def getData(self,key):
        for coppia in self.config:
            if coppia[0]==key:
                return coppia[1]
    # ===========================================
 
    def saveConfig(self, pointer, value):
        for coppia in self.config:
            if coppia[0] == pointer:
                coppia[1] = value
                print(coppia[1])
    
    
    
