'''
Parse a data or variables file
'''
class Parser:
    def __init__(self,file):
        
        self.raw = []                   #raw string that will contain file 
                                        #trimmed per line list
        
        #getting extension
        ext = file.split('.')
        ext = ext[-1]
        
        
        in_file = open(file,"r")        #open stream
        text = in_file.readlines()      #divide lines in a list
        in_file.close()                 #close stream
        
        for i in range(len(text)):      #for each line
            text[i] = text[i].rstrip()
        
        self.raw = list(text)           #actually duplicate list, not using pointer
        
        if ext=='var':
            pass
        if ext=='data':
            pass
        