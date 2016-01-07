from direct.task import Task
from direct.showbase.DirectObject import DirectObject

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from mainwindow import Ui_MainWindow

from utilities import *

import sys, os, string

import xml.etree.cElementTree as ET

class MapExporter:
    def __init__(self):
        self.clear()
        self.xml = ''
    
    def save(self):
        print "attempt saving..."
        print pGrid.getCurrentMapPath()
        
        self.addXMLLine('<data tilesize="32.0" showcollisions="false" camdistance="15.0">',0)
        
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
            
            self.addXMLLine('<tile>',2)
            
            self.addXMLLine('</tile>',2)
        
        self.addXMLLine('</row>',1)
        self.addXMLLine('</data>',0)
            
        
        print self.xml
    
    '''
    Clears everything
    MODIFY self.xml set to empty
    '''
    def clear(self):
        self.xml = ''
    
    '''
    Add a line of xml
    @param s        string to be added
    @param depth    indentation depth
    '''
    def addXMLLine(self, s, depth):
        for i in range(depth):
            self.xml += "\t"
        self.xml += s+"\n"
