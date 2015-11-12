from direct.showbase.DirectObject import DirectObject
from camera.camera import CustomCamera

#importing task
from direct.task import Task

class EditorCamera(CustomCamera):
    def __init__(self):
        #executing parent's constructor
        CustomCamera.__init__(self)
    
    def setEditorMode(self, value):
        if value == True:
            self.dontFollow()
        else:
            #add disable commands when editor mode goes off
            pass
        
        
