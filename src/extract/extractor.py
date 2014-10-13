from parser.parser import Parser

class Extractor:
    
    """
    input = file directory
    output = a list of the file directory
    """
    
    def extractText(self,key):
        fileLoaded = Parser(key) 
        data = fileLoaded.get()    # list of couples
        return data
    
    