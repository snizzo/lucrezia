from direct.showbase.DirectObject import DirectObject

'''
This class will provide persistence to the world of lucrezia.
Here can be set variables that are cross levels, cross maps
and that can be saved in the future in a savefile and loaded.
'''
class Persistence(DirectObject):
    def __init__(self):
        self.data = {}
    
    def save(self, key, value):
        self.data[key] = value
    
    def load(self, key):
        if self.data.has_key(key):
            return self.data[key]
        else:
            return False
    
    def delete(self, key):
        if self.data.has_key(key):
            del self.data[key]
