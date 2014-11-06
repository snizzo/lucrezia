#panda3d
from panda3d.core import NodePath, PointLight, VBase4, Spotlight, PerspectiveLens, Point3

#this class represents a cluster of grass blade for every tile in grid
class Light():
    def __init__(self, attributes):
        if attributes.has_key('distance'):
            distance = float(attributes['distance'].value)
        else:
            distance = 1.0
        
        if attributes.has_key('attenuation'):
            attenuation = float(attributes['attenuation'].value)
        else:
            attenuation = 0.0
            
        if attributes.has_key('type'):
            ltype = attributes['type'].value
        else:
            ltype = 'point'
        
        if attributes.has_key('color'):
            color = attributes['color'].value
        else:
            color = '1,1,1,1'
        
        rgba = color.split(',')
        if len(rgba) < 3:
            print "ERROR: please define a correct color for light. (example: r,g,b,a in float values)!"
        realcolor = VBase4(float(rgba[0])/255,float(rgba[1])/255,float(rgba[2])/255,1.0)
        
        if ltype == 'spot':
            self.plight = Spotlight('slight')
            self.plight.setColor(realcolor)
            self.lens = PerspectiveLens()
            self.plight.setLens(self.lens)
            self.plnp = render.attachNewNode(self.plight)
            self.plnp.setPos(0.5, -distance, 0.5)
            self.plnp.lookAt(Point3(0.5, 0, 0.5))
            render.setLight(self.plnp)
        
        if ltype == 'point':
            self.plight = PointLight('plight')
            self.plight.setColor(realcolor)
            self.plight.setAttenuation(attenuation)
            self.plnp = NodePath(self.plight)
            self.plnp.setPos(0.5, -distance, 0.5)
            render.setLight(self.plnp)
            #self.plnp.place()
            
    def getNode(self):
        return self.plnp
 
