'''
    This abstract class defines an interface that has to be used in order to be
    compliant with the PropertiesTable handled objects
'''
import abc

class PropertiesTableAbstract( object ):
    __metaclass__ = abc.ABCMeta
    
    '''
    usually an implementation like this is used
    self.sanitizeProperties()
    '''
    @abc.abstractmethod
    def onPropertiesUpdated(self):
        return
        
    '''
    usually an implementation like this is used
    return self.properties
    '''
    @abc.abstractmethod
    def getPropertyList(self):
        return
    
    '''
    usually an implementation like this is used
    self.properties[key] = value
    '''
    @abc.abstractmethod
    def setProperty(self, key, value):
        return
    
    '''
    use to quickly decrease property values
    using key "-"
    '''
    @abc.abstractmethod
    def decreaseProperty(self, key, multiplier):
        return
    
    '''
    use to quickly increase property values
    using key "+"
    '''
    @abc.abstractmethod
    def increaseProperty(self, key, multiplier):
        return
