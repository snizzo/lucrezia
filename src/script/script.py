from direct.showbase.DirectObject import DirectObject

class Script(DirectObject):
    def __init__(self):
        self.lock = False
        self.queue = []
        self.customLocks = []
        
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
    accepts one object that must have the globalLock property
    set on true or false
    
    those locks are one-timer. They must be added when the lock
    is already set because when the lock is released, it's deleted
    from custom lock list
    '''
    def addOneCustomLock(self, lock):
        if hasattr(lock, 'globalLock'):
            self.customLocks.append(lock)
        else:
            print "WARNING: attempt to add a blocking object without 'globalLock' property"
            print "WARNING: object:", lock
            if hasattr(lock, 'uid'):
                print "WARNING: uid:", lock.uid
    
    '''
    insert here the manager of the locking objects
    that will be checked by script manager before
    allowing more execution
    '''
    def checkLocks(self):
        if baloons.globalLock == True:
            return
        for o in self.customLocks[:]:
            if o.globalLock == True: #or inhibit script running
                return
            else:
                self.customLocks.remove(o) #or removed. one-timer
                
        #allows execution
        self.unlock()
    
    def load(self, resname):
        rl = resourceManager.getResource(resname)
        
        script = open(rl)
        blocks = script.read().split("###pause")
        
        for block in blocks:
            self.queue.append(block)
