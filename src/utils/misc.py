from panda3d.core import LVecBase4f, CardMaker, NodePath, Vec4, Texture
from pandac.PandaModules import TransparencyAttrib

'''
Generic collection of static snippets
TODO: rename as a playground for not yet categorized snippets
'''
class Misc():
    
    """
    Load image as 3d plane

    Arguments:
    filepath -- image file path
    yresolution -- pixel-perfect width resolution
    """
    @staticmethod
    def loadImageAsPlane(filepath, yresolution = 600):
        tex = loader.loadTexture(filepath)
        tex.setBorderColor(Vec4(0,0,0,0))
        tex.setWrapU(Texture.WMBorderColor)
        tex.setWrapV(Texture.WMBorderColor)
        cm = CardMaker(filepath + ' card')
        cm.setFrame(-tex.getOrigFileXSize(), tex.getOrigFileXSize(), -tex.getOrigFileYSize(), tex.getOrigFileYSize())
        card = NodePath(cm.generate())
        card.setTransparency(TransparencyAttrib.MAlpha)
        card.setTexture(tex)
        card.setZ(card.getZ()+0.018)
        card.setScale(card.getScale()/ yresolution)
        card.flattenLight() # apply scale
        return card
    
    @staticmethod
    def getDeltaTime():
        return globalClock.getDt()