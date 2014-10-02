class Resource:
    def __init__(self, file):
        self.file = file
        self.type = 'nd'
        self.abs = 'nd'
        
        self.getType()
        self.getAbsPath()
    
    def getType(self):
        #qua codice che scopre il tipo del file 'self.file'
        self.type = 'nd'
    
    def getAbsPath(self):
        #qua codice che scopre il percorso assoluto del file 'self.file'
        self.abs = 'nd'
