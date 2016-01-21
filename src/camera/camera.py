from direct.showbase.DirectObject import DirectObject

#importing task
from direct.task import Task

class CustomCamera(DirectObject):
    def __init__(self):
        base.disableMouse()
        self.setDistance(7.5)
        base.camera.setP(3)
        self.obj = 0
        self.t = 0
        pass #nothing for now?
    
    '''
    Set the object to follow
    '''
    def follow(self, obj):
        self.dontFollow()
        if (obj != 0):
            self.obj = obj
            #storing for later use
            self.t = taskMgr.add(self.followTask, "camerafollowtask")
    
    def setDistance(self, d):
        base.camera.setY(-d)
    
    def dontFollow(self):
        if self.t != 0:
            taskMgr.remove(self.t)
            self.t = 0
    
    def followTask(self, task):
        if self.obj != 0:
            print self.obj
            base.camera.setX(self.obj.getWorldPos().getX())
            base.camera.setZ(self.obj.getWorldPos().getZ())
        return Task.cont
        
