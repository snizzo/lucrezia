from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import *

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
        
        self.accept("wheel_up", self.zoomIn)
        self.accept("wheel_down", self.zoomOut)
        self.accept("arrow_up", self.moveUp)
        self.accept("arrow_down", self.moveDown)
        self.accept("arrow_left", self.moveLeft)
        self.accept("arrow_right", self.moveRight)
        
        self.selectedCellX = 0
        self.selectedCellY = 0
        
        base.camera.setX(0.5)
        base.camera.setZ(0.5)
        
        #added
        self.currentCellNode = None
        self.currentCellNodePath = None
        
        self.createSelectedCellGrid()
    
    def createSelectedCellGrid(self):
        
        self.currentCellLines = LineSegs()
        
        self.currentCellLines.setThickness(15)
        self.currentCellLines.setColor(1,0,0)
        self.currentCellLines.moveTo(0,-0.1,0)
        self.currentCellLines.drawTo(0,-0.1,1)
        self.currentCellLines.drawTo(1,-0.1,1)
        self.currentCellLines.drawTo(1,-0.1,0)
        self.currentCellLines.drawTo(0,-0.1,0)
        
        #Create selector lines node and path then reparent
        self.currentCellNode = self.currentCellLines.create()
        self.currentCellNodePath = NodePath(self.currentCellNode)
        self.currentCellNodePath.reparentTo(render)
        self.currentCellNodePath.setLightOff()
    
    def moveUp(self):
        self.selectedCellY += 1
        base.camera.setZ(self.selectedCellY + 0.5)
        self.currentCellNodePath.setZ(self.selectedCellY)
        self.analyzeCurrentCell()
    
    def moveDown(self):
        self.selectedCellY -= 1
        base.camera.setZ(self.selectedCellY + 0.5)
        self.currentCellNodePath.setZ(self.selectedCellY)
        self.analyzeCurrentCell()
    
    def moveLeft(self):
        self.selectedCellX -= 1
        base.camera.setX(self.selectedCellX + 0.5)
        self.currentCellNodePath.setX(self.selectedCellX)
        self.analyzeCurrentCell()
    
    def moveRight(self):
        self.selectedCellX += 1
        base.camera.setX(self.selectedCellX + 0.5)
        self.currentCellNodePath.setX(self.selectedCellX)
        self.analyzeCurrentCell()
    
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
        
        
