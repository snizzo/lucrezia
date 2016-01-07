'''
    This class represent an object that can be exported through
    xml map exporter
'''
import abc

class XMLExportable( object ):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def xmlTypeName(self):
        ''' method documentation '''
        return
    
    @abc.abstractmethod
    def xmlAttributes(self):
        ''' method documentation '''
        return
