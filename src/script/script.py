from direct.showbase.DirectObject import DirectObject

class Script(DirectObject):
    def __init__(self):
        self.lock = False
        self.queue = []
        
        #self.accept("resumeGameplay", self.unlock)
        
        #as for now when all baloons are empty, scripting engine will execute more
        taskMgr.add(self.scriptTask, "scripttask")
    
    def unlock(self):
        self.lock = False
        
    def _lock(self):
        self.lock = True
    
    '''
    always run when script engine is active
    '''
    def scriptTask(self, task):
        self.checkLocks()
        if self.lock == False and len(self.queue) > 0:
            block = self.queue.pop(0)
            exec(block)
            self._lock()
        return task.cont
    
    '''
    insert here the manager of the locking objects
    that will be checked by script manager before
    allowing more execution
    '''
    def checkLocks(self):
        if baloons.globalLock == True:
            return
        #allows execution
        self.unlock()
    
    def load(self, resname):
        rl = resourceManager.getResource(resname)
        
        script = open(rl)
        blocks = script.read().split("###pause")
        
        for block in blocks:
            self.queue.append(block)
