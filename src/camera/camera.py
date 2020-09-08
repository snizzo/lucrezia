from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.IntervalGlobal import *

#importing task
from direct.task import Task

class CustomCamera(DirectObject):
    def __init__(self):
        base.disableMouse()
        self.setDistance(7.5)
        base.camera.setP(1.5)
        self.obj = 0
        self.t = 0
        
        #blocking for lerp direction scripting
        self.globalLock = False #very important for scripting engine
    
    def lock(self):
        self.globalLock = True
    
    def unlock(self):
        self.globalLock = False
    
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
            base.camera.setX(self.obj.getWorldPos().getX())
            base.camera.setZ(self.obj.getWorldPos().getZ())
        return Task.cont
    
    def moveCameraAtPoint(self, x, y):
        #blocking scripting engine from executing the next code block
        self.lock()
        script.addOneCustomLock(self)
        cameraLerp = LerpPosInterval(base.camera,
                    2,
                    Point3(x,base.camera.getY(),y),
                    startPos=Point3(base.camera.getX(),base.camera.getY(),base.camera.getZ()),
                    other=None,
                    blendType='easeInOut',
                    bakeInStart=1,
                    fluid=0,
                    name=None)
        Sequence(
            cameraLerp,
            Func(self.unlock)
        ).start()
    
    def moveCameraAtObject(self, obj):
        pos = obj.getWorldPos()
        pos.setY(base.camera.getY())
        print(pos)
        #blocking scripting engine from executing the next code block
        self.lock()
        script.addOneCustomLock(self)
        cameraLerp = LerpPosInterval(base.camera,
                    2,
                    pos,
                    startPos=Point3(base.camera.getX(),base.camera.getY(),base.camera.getZ()),
                    other=None,
                    blendType='easeInOut',
                    bakeInStart=1,
                    fluid=0,
                    name=None)
        Sequence(
            cameraLerp,
            Func(self.unlock)
        ).start()
    
    def moveCameraBetweenObjects(self, o1, o2):
        pos1 = o1.getWorldPos()
        pos2 = o2.getWorldPos()
        pos = (pos1 + pos2)/2
        pos.setY(base.camera.getY())
        #blocking scripting engine from executing the next code block
        self.lock()
        script.addOneCustomLock(self)
        cameraLerp = LerpPosInterval(base.camera,
                    2,
                    pos,
                    startPos=Point3(base.camera.getX(),base.camera.getY(),base.camera.getZ()),
                    other=None,
                    blendType='easeInOut',
                    bakeInStart=1,
                    fluid=0,
                    name=None)
        Sequence(
            cameraLerp,
            Func(self.unlock)
        ).start()
        
