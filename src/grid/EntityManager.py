'''
Superclass that manages all the entities in game.
Have to be subclassed to manage different types of entities.
'''

from grid.grid import Grid
from abc import ABC, abstractmethod

class EntityManager(ABC):
    def __init__(self) -> None:
        self.entities = []

    @abstractmethod
    def add(self, file="", name=""):
        pass
    
    def append(self, entity) -> None:
        self.entities.append(entity)

    def last(self) -> Grid:
        return self.entities[-1]
    
    def getAllLoadedKeys(self) -> list:
        return [entity.getEntityName() for entity in self.entities]
    
    def getAllEntities(self) -> list:
        #return the second element of every tuple inside self.entities
        return self.entities


    def get(self, key) -> Grid:
        #if is a string
        if isinstance(key, str):
            for entity in self.entities:
                if entity.getEntityName() == key:
                    return entity
        
        if isinstance(key, int):
            return self.entities[key]
    

