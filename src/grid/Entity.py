"""
Entities are objects that can be loaded in the game, be it Grids or Objects. They share some common methods, used by EntityManager.

The entity name is used to identify the entity uniquely in the game, across Grids, Objects 
and any other kind of entity that will be implemented in the future.
"""

class Entity():
    def __init__(self) -> None:
        self.entityName = ""
    
    def getEntityName(self) -> str:
        return self.entityName

    def setEntityName(self, name) -> None:
        self.entityName = name