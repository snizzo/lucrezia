from parserFile.parserFile import Parser
import getpass                  #for user name of the pc

class ExtractTitle:
    
    def __init__(self):
        self.pc_name = getpass.getuser()
        self.langdir = 'lang'
        self.current_menu= {
            'START_MENU': ['MN_START'],
            'MAIN_MENU': ['MN_PLAY','MN_LOAD','MN_OPTION','MN_CREDITS','MN_QUIT'],
            'LOAD_MENU': ['MN_LOAD','MN_DELETE','MN_BACK'],
            'OPTION_MENU': ['MN_VIDEO','MN_COMMANDS','MN_AUDIO','MN_LANG','MN_BACK'],
            'VIDEO_MENU' : ['MN_BACK'],
            'COMMANDS_MENU' : ['MN_BACK'],
            'AUDIO_MENU' : ['MN_BACK'],
            'LANG_MENU' : ['MN_BACK'],
            'QUIT_MENU': ['MN_EXIT','MN_Y','MN_N'],
            'MN_VERSION' : ['VERSION']
        }

    
    def extractTxt(self,lang):
        current_menup = Parser(resourceManager.getResource(self.langdir + '/' + lang + '.var')) 
        data = current_menup.get()    # lista di coppie es: MN_PLAY gioca
       
        #ciclo per l associazione dei titoli
        for coppia in data:
            for menu in self.current_menu:
                for index, value in enumerate(self.current_menu[menu]):
                    if coppia[0]==value:
                        self.current_menu[menu][index] = coppia[1]
                        print self.current_menu[menu][index] 
           
        versionM = Parser(resourceManager.getResource("config/" + self.pc_name +"Config.var"))
        data2 = versionM.get()
        
        for coppia in data2:
            for menu in self.current_menu:
                for index, value in enumerate(self.current_menu[menu]):
                    if coppia[0]==value:
                        self.current_menu[menu][index] = coppia[1]
        
        
        print self.current_menu