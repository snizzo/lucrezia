'''
    This class represent an object that can be paused during gameplay
    through messenger messages:
     - self.accept("pauseGameplay")
     - self.accept("resumeGameplay")
'''
import abc

class Pausable( object ):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def pauseGameplay(self):
        ''' method documentation '''
        return
    
    @abc.abstractmethod
    def resumeGameplay(self):
        ''' method documentation '''
        return
