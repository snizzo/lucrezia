from direct.task import Task
from direct.showbase.DirectObject import DirectObject

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from mainwindow import Ui_MainWindow

from utilities import *

import sys, os, string
from shutil import copyfile

import xml.etree.cElementTree as ET

class MapExporter:
    def __init__(self):
        self.clear()
        self.mapPath = ''
        self.xml = ''
    
    def save(self):
        self.mapPath = pGrid.getCurrentMapPath()
        
        self.onLoad = 'onLoad="'+pGrid.getOnLoad()+'"' if pGrid.getOnLoad() else ''
        self.onUnload = 'onUnload="'+pGrid.getOnUnload()+'"' if pGrid.getOnUnload() else ''
        self.bgImage = 'bgImage="'+pGrid.getBackgroundImage()+'"' if pGrid.getBackgroundImage() else ''

        self.addXMLLine('<data tilesize="32.0" showcollisions="false" camdistance="18.5" '+self.onLoad+' '+self.onUnload+' '+self.bgImage+'>',0)
        
        tiles = pGrid.getAllTiles()
        
        #computing the max tilesize of the grid
        maxtile = 0
        while pGrid.getTile(0,maxtile) != -1:
            maxtile += 1
        maxtile -= 1
        
        rowcounter = -1
        for t in tiles:
            #prints row opener closer, except last closer
            if t.getY() != rowcounter:
                if rowcounter == -1:
                    self.addXMLLine('<row>',1)
                    rowcounter += 1
                elif rowcounter > -1 and rowcounter < maxtile:
                    self.addXMLLine('</row>',1)
                    self.addXMLLine('<row>',1)
                    rowcounter += 1
            
            #adding tiles
            self.addXMLLine('<'+t.xmlTypeName()+'>',2)
            
            #adding ground
            self.addXMLLine('<ground '+self.fromDictToXmlAttributes(t.xmlAttributes())+'/>',3)
            
            #adding objects
            objects = t.getGameObjects()
            for o in objects:
                self.addXMLLine('<'+o.xmlTypeName()+' '+self.fromDictToXmlAttributes(o.xmlAttributes())+'/>',3)
            
            #closing tags
            self.addXMLLine('</'+t.xmlTypeName()+'>',2)
        
        self.addXMLLine('</row>',1)
        self.addXMLLine('</data>',0)
        
        self.saveToFile()
        #print self.xml
    
    def saveToFile(self):
        #copyfile(self.mapPath,
        path = os.path.dirname(self.mapPath)
        name = os.path.basename(self.mapPath)
        
        backup = path+'/backup/'+name
        
        copyfile(self.mapPath, backup)
        
        savefile = open(self.mapPath, 'w')
        savefile.truncate()
        savefile.write(self.xml)
        savefile.close()
        
    
    def fromDictToXmlAttributes(self, l):
        self.validateData(l)
        xml = ''
        for k,v in l.iteritems():
            xml += k+'="'+str(v)+'" '
        
        return xml
    
    def validateData(self, l):
        for k,v in l.items():
            if v == '':
                del l[k]
        
        for e in l:
            #correctly parsing bool values
            if type(e) is bool:
                if e == False:
                    e = 'false'
                if e == True:
                    e = 'true'
    
    '''
    Clears everything and set to empty
    '''
    def clear(self):
        self.xml = ''
    
    '''
    Add a line of xml
    @param s        string to be added
    @param depth    indentation depth
    '''
    def addXMLLine(self, s, depth, ret=True):
        for i in range(depth):
            self.xml += "\t"
        if ret == True:
            self.xml += s+"\n"
