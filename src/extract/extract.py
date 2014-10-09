from parser.parser import Parser

class Extract:
    
    def __init__(self):
        self.langdir = 'lang'
        self.current_menu= {
            'START_MENU': [],
            'MAIN_MENU': ['MN_PLAY','MN_LOAD','MN_OPTION','MN_CREDITS','MN_QUIT'],
            'LOAD_MENU': [],
            'OPTION_MENU ': []
        }

    
    def extract_Txt(self,lang):
        current_menup = Parser(resourceManager.getResource(self.langdir + '/' + lang + '.var')) 
        data = current_menup.get()    # lista di coppie es: MN_PLAY gioca
       
        #ciclo per l associazione dei titoli
        for coppia in data:
            for index, value in enumerate(self.current_menu['MAIN_MENU']):
                if coppia[0]==value:
                    self.current_menu['MAIN_MENU'][index] = coppia[1]
                    break
        
        print self.current_menu