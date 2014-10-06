from pandac.PandaModules import CardMaker
from panda3d.core import NodePath, TextureStage
from pandac.PandaModules import TransparencyAttrib
#TODO: fix the mess
class Character():
    
        def __init__(self, baseDimension):
        #public props
        self.resources = []
        
        self.innerX = 0
        self.innerY = 0
        self.innerDimension = 0
        
        self.baseDimension = baseDimension
        
        self.node = NodePath('tilenode')
        self.node.setTwoSided(True)
        
        
        #generating groundnode
        cm = CardMaker("tiletexture")
        cm.setFrame(0,1,0,1)
        
        self.groundnode = NodePath('groundtilenode')
        self.groundnode.attachNewNode(cm.generate())
        self.groundnode.reparentTo(self.node)
    
    #add a static texture to basic 128x128 tile pixel image
    #use just to paint the world basicly. Use addObject for every object that has to do with collision etc
    def addTexture(self, name):
        tex = loader.loadTexture('../res/'+name+'.png')
        
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MDecal)
        
        self.groundnode.setTexture(ts, tex)
