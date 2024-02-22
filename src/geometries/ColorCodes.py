
#lucrezia imports
from gui.AssetListManager import AssetListManager

class ColorCodes(AssetListManager):

    @staticmethod
    def load():
        if not ColorCodes.isLoaded:
            ColorCodes.isLoaded = True
        
        # add some default color codes
        ColorCodes.add("red", (1.0, 0.0, 0.0, 1.0))
        ColorCodes.add("green", (0.0, 1.0, 0.0, 1.0))
        ColorCodes.add("blue", (0.0, 0.0, 1.0, 1.0))
        ColorCodes.add("yellow", (1.0, 1.0, 0.0, 1.0))
        ColorCodes.add("orange", (1.0, 0.5, 0.2, 1.0))
        ColorCodes.add("white", (1.0, 1.0, 1.0, 1.0))
        ColorCodes.add("black", (0.0, 0.0, 0.0, 1.0))
        ColorCodes.add("gray", (0.5, 0.5, 0.5, 1.0))
        ColorCodes.add("lightgray", (0.8, 0.8, 0.8, 1.0))
        ColorCodes.add("darkgray", (0.3, 0.3, 0.3, 1.0))
        ColorCodes.add("purple", (0.5, 0.0, 0.5, 1.0))
        ColorCodes.add("cyan", (0.0, 1.0, 1.0, 1.0))
        ColorCodes.add("magenta", (1.0, 0.0, 1.0, 1.0))
        ColorCodes.add("brown", (0.5, 0.2, 0.0, 1.0))
        ColorCodes.add("clear", (0.0, 0.0, 0.0, 0.0))
    
    @staticmethod
    def fromRGBA(r, g, b, a):
        return (r, g, b, a)

#color codes can autoload because it uses no panda3d resources to load
ColorCodes.load()