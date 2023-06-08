
"""
Represent a single data block in the grid, as extracted from the xml file.
"""

class GridDataBlock:
    def __init__(self, type="", attributes={}) -> None:
        self.type = type
        self.attributes = attributes
    
    def getType(self) -> str:
        return self.type
    
    def getAttributes(self) -> dict:
        return self.attributes