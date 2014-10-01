'''
ONCE class:

 Simple structure that if checked with get() method, return true on first check,
 false all the others.

'''
class Once:
    
    #constructor
    def __init__(self):
        self.value = True
    
    def get(self):
        if self.value == True:
            self.value = False
            return True
        else:
            return False