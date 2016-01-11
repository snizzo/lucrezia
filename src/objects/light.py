#panda3d
from panda3d.core import NodePath, PointLight, VBase4, Spotlight, PerspectiveLens, Point3

from grid.XMLExportable import XMLExportable
from editor.gui.PropertiesTableAbstract import PropertiesTableAbstract

class Light(PropertiesTableAbstract, XMLExportable):
    def __init__(self, attributes, parent):
        
        self.plnp = -1
        self.parent = parent
        self.typeName = 'light'
        self.properties = {
            'distance' : '',
            'attenuation' : '',
            'type' : '',
            'on' : '',
            'color' : '',
            'id' : ''
        }
        
        if attributes.has_key('distance'):
            self.properties['distance'] = distance = float(attributes['distance'].value)
        else:
            distance = 1.0
        
        if attributes.has_key('attenuation'):
            self.properties['attenuation'] = self.attenuation = attenuation = float(attributes['attenuation'].value)
        else:
            self.properties['attenuation'] = self.attenuation = attenuation = 0.0
            
        if attributes.has_key('type'):
            self.properties['type'] = ltype = attributes['type'].value
        else:
            self.properties['type'] = ltype = 'point'
        
        if attributes.has_key('on'):
            if attributes['on'].value == "false":
                self.properties['on'] = 'false'
                self.on = False
            else:
                self.properties['on'] = 'true'
                self.on = True
        else:
            self.on = True
        
        if attributes.has_key('color'):
            self.properties['color'] = color = attributes['color'].value
        else:
            color = '1,1,1,1'
        
        if attributes.has_key('id'):
            self.properties['id'] = self.uid = uid = attributes['id'].value
        else:
            self.properties['id'] = self.uid = uid = 'light'
        
        self.generateNode()
    
    def destroy(self):
        if self.plnp != -1:
            render.clearLight(self.plnp)
    
    def generateNode(self):
        rgba = self.properties['color'].split(',')
        if len(rgba) < 3:
            print "ERROR: please define a correct color for light. (example: r,g,b,a in float values)!"
        realcolor = VBase4(float(rgba[0])/255,float(rgba[1])/255,float(rgba[2])/255,1.0)
        
        if self.properties['type'] == 'spot':
            self.plight = Spotlight('slight')
            self.plight.setColor(realcolor)
            self.lens = PerspectiveLens()
            self.plight.setLens(self.lens)
            self.plnp = self.parent.attachNewNode(self.plight)
            self.plnp.setPos(0.5, -self.properties['distance'], 0.5)
            self.plnp.lookAt(Point3(0.5, 0, 0.5))
        
        if self.properties['type'] == 'point':
            self.plight = PointLight('plight')
            self.plight.setColor(realcolor)
            if self.on == True:
                self.plight.setAttenuation(self.properties['attenuation'])
            else:
                self.plight.setAttenuation((1.0,0,1))
            self.plnp = self.parent.getNode().attachNewNode(self.plight)
            self.plnp.setPos(0.5, -self.properties['distance'], 0.5)
        
        render.setLight(self.plnp)
        
        if self.on:
            self.setOn()
        
        #set unique id
        self.plnp.setTag("id", self.properties['id'])
        self.plnp.setPythonTag("gamenode", self)
    
    def getName(self):
        return self.properties['id']
    
    def xmlAttributes(self):
        return self.properties
    
    def xmlTypeName(self):
        return self.typeName
    
    '''
    Sanitize properties data to be of correct type from string
    '''
    def sanitizeProperties(self):
        #sanitizing data
        self.properties['distance'] = float(self.properties['distance'])
        self.properties['attenuation'] = float(self.properties['attenuation'])
    
    #interface needed by PropertiesTable
    # regenerates the node at every change
    def onPropertiesUpdated(self):
        self.sanitizeProperties()
        
        rgba = self.properties['color'].split(',')
        if len(rgba) < 3:
            print "ERROR: please define a correct color for light. (example: r,g,b,a in float values)!"
        realcolor = VBase4(float(rgba[0])/255,float(rgba[1])/255,float(rgba[2])/255,1.0)
        
        self.plight.setColor(realcolor)
        self.plight.setAttenuation((self.properties['attenuation']))
    
    def getPropertyList(self):
        return self.properties
    
    def setProperty(self, key, value):
        self.properties[key] = value
    
    def getNode(self):
        return self.plnp
 
    def setOn(self):
        self.plight.setAttenuation(self.attenuation)
        self.on = True
    
    def setOff(self):
        self.plight.setAttenuation(1.0)
        self.on = False
    
    def toggle(self):
        if self.on:
            self.setOff()
        else:
            self.setOn()
