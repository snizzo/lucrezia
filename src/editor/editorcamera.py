from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText

#engine imports
from camera.camera import CustomCamera

#importing task
from direct.task import Task
'''
ingoing messages:

outgoing messages:
editor_analyzecell [x] [y]
'''
class EditorCamera(CustomCamera):
    def __init__(self):
        #executing parent's constructor
        CustomCamera.__init__(self)
        base.camera.setX(0.5)
        base.camera.setZ(0.5)
        
        self.accept("wheel_up", self.zoomIn)
        self.accept("wheel_down", self.zoomOut)
        self.accept("f5", self.analyzeCurrentCell)
        self.accept("arrow_up", self.moveUp)
        self.accept("arrow_down", self.moveDown)
        self.accept("arrow_left", self.moveLeft)
        self.accept("arrow_right", self.moveRight)
        
        self.selectedCellX = 0
        self.selectedCellY = 0
    
    def moveUp(self):
        self.selectedCellY += 1
        base.camera.setZ(self.selectedCellY + 0.5)
    
    def moveDown(self):
        self.selectedCellY -= 1
        base.camera.setZ(self.selectedCellY - 0.5)
    
    def moveLeft(self):
        self.selectedCellX -= 1
        base.camera.setX(self.selectedCellX - 0.5)
    
    def moveRight(self):
        self.selectedCellX += 1
        base.camera.setX(self.selectedCellX + 0.5)
    
    def analyzeCurrentCell(self):
        messenger.send("editor_analyzecell", [self.selectedCellX, self.selectedCellY])
    
    def zoomOut(self):
        base.camera.setY(base.camera.getY()-0.5)
    
    def zoomIn(self):
        base.camera.setY(base.camera.getY()+0.5)
    
    #refactor?
    def setEditorMode(self, value):
        if value == True:
            self.dontFollow()
        else:
            #add disable commands when editor mode goes off
            pass
        
        
