from direct.showbase.DirectObject import DirectObject
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

import os, subprocess

class PropertiesTable(DirectObject):
    def __init__(self, table):
        self.table = table
        
        self.currentSelection = []
        self.lastPropertyRowSelected = None
        
        self.accept("selected one", self.oneobj)
        self.accept("selected none", self.noneobj)
        self.accept("open-editor-onPicked", self.onOpenEditor, ['onPicked'])
        self.accept("open-editor-onWalked", self.onOpenEditor, ['onWalked'])
        self.accept("open-editor-onLoad", self.onOpenEditorMap, ['onLoad'])
        self.accept("open-editor-onUnload", self.onOpenEditorMap, ['onUnload'])
        self.accept("increaseProperty", self.increaseProperty)
        self.accept("decreaseProperty", self.decreaseProperty)
        self.accept("colorPicker", self.colorPicker)
        
        self.table.cellChanged.connect(self.cellChanged)
        self.table.cellClicked.connect(self.cellClicked)
    
    #holder is the object holding and using the props
    def oneobj(self, obj):
        self.clearTable()
        self.currentSelection = []
        
        #adding properties
        for key, value in obj.getPropertyList().iteritems():
            self.addPropertyRow(key, value)
        
        #storing temporary selection in a cleared list
        self.currentSelection.append(obj)
        
        #sort on first column alphabetically ascending
        self.table.sortItems(0)
    
    #multiple selection / modifying still not supported
    def manyobj(self, object_list):
        pass
    
    def noneobj(self):
        self.clearTable()
    
    '''
    refreshes properties table with values from current selection object
    '''
    def refresh(self):
        self.oneobj(self.currentSelection[0])
    
    '''
    used only for maps
    '''
    def onOpenEditorMap(self, event):
        obj = pGrid
        if event == 'onLoad':
            inlineCode = pGrid.getOnLoad()
        elif event == 'onUnload':
            inlineCode = pGrid.getOnUnload()
        
        #creates and opens new python script file
        if inlineCode == '' or inlineCode == False:
            scriptMapDir = resourceManager.getResource('scripts/'+pGrid.getCurrentMapName())
            
            if not os.path.exists(scriptMapDir):
                os.makedirs(scriptMapDir)
            
            relpath = 'scripts/'+pGrid.getCurrentMapName()+'/'+pGrid.getCurrentMapName()+event+'.py'
            path = resourceManager.getResource(relpath)
            #creating file if not exists
            open(path, 'a').close()
            #opening file
            subprocess.call(["xdg-open", path])
            if event == 'onLoad':
                inlineCode = pGrid.setOnLoad('script.load(\''+relpath+'\')')
            elif event == 'onUnload':
                inlineCode = pGrid.setOnUnload('script.load(\''+relpath+'\')')
        #opens already present script
        else:
            inlineCode = inlineCode.replace('script.load(\'', '')
            inlineCode = inlineCode.replace('\')', '')
            #TODO: this is linux dependant!!
            subprocess.call(["xdg-open", resourceManager.getResource(inlineCode)])
        
    
    '''
    used for every object
    '''
    def onOpenEditor(self, event):
        obj = self.currentSelection[0]
        inlineCode = obj.getPropertyList()[event]
        
        #creates and opens new python script file
        if inlineCode == '':
            uid = obj.getPropertyList()['id']
            scriptMapDir = resourceManager.getResource('scripts/'+pGrid.getCurrentMapName())
            
            if not os.path.exists(scriptMapDir):
                os.makedirs(scriptMapDir)
            
            relpath = 'scripts/'+pGrid.getCurrentMapName()+'/'+str(obj.getTileX())+'x'+str(obj.getTileY())+uid+event+'.py'
            path = resourceManager.getResource(relpath)
            #creating file if not exists
            open(path, 'a').close()
            #opening file
            #TODO: linux dependant
            subprocess.call(["xdg-open", path])
            obj.setProperty(event, 'script.load(\''+relpath+'\')')
            self.refresh()
        #opens already present script
        else:
            inlineCode = inlineCode.replace('script.load(\'', '')
            inlineCode = inlineCode.replace('\')', '')
            #TODO: this is linux dependant!!
            subprocess.call(["xdg-open", resourceManager.getResource(inlineCode)])
    
    def cellClicked(self, row, column):
        self.lastPropertyRowSelected = row
    
    def cellChanged(self, row, column):
        if len(self.currentSelection)>0: #if something is selected, else is bogus
            
            key = self.table.item(row,0).text().__str__()
            value = self.table.item(row,1).text().__str__()
        
            self.currentSelection[0].setProperty(key,value)
        
            #reload everything
            self.oneobj(self.currentSelection[0])
            self.currentSelection[0].onPropertiesUpdated()
    
    '''
    Increase value of current selected property
    '''
    def increaseProperty(self, multiplier):
        if len(self.currentSelection)>0: #if something is selected, else is bogus
            if self.lastPropertyRowSelected != None:
                row = self.lastPropertyRowSelected
                
                key = self.table.item(row,0).text().__str__()
                value = self.table.item(row,1).text().__str__()
            
                self.currentSelection[0].increaseProperty(key, multiplier)
            
                self.reloadSelection()
    
    '''
    Decrease value of current selected property
    '''
    def decreaseProperty(self, multiplier):
        if len(self.currentSelection)>0: #if something is selected, else is bogus
            if self.lastPropertyRowSelected != None:
                row = self.lastPropertyRowSelected
                key = self.table.item(row,0).text().__str__()
                value = self.table.item(row,1).text().__str__()
            
                self.currentSelection[0].decreaseProperty(key, multiplier)
                
                self.reloadSelection()
    
    '''
    Open graphical color picker
    '''
    def colorPicker(self):
        pass
    
    def reloadSelection(self):
        if len(self.currentSelection)>0: #if something is selected, else is bogus
            #reload everything
            self.oneobj(self.currentSelection[0])
            self.currentSelection[0].onPropertiesUpdated()
        else:
            print "Warning: attempted reloading selected PropertiesTable selected object, but nothing is selected."
    
    '''
    Adds every property to prop table
    '''
    def addPropertyRow(self, label, value):
        
        value = str(value)
        
        #resizing table size
        self.table.setRowCount(self.table.rowCount()+1)
        self.table.setColumnCount(2)
        
        #creating items
        namelabel = QTableWidgetItem(label)
        valuelabel = QTableWidgetItem(value)
        
        #attaching items to correct position
        self.table.setItem(self.table.rowCount()-1,0, namelabel)
        self.table.setItem(self.table.rowCount()-1,1, valuelabel)
    
    '''
    Clear all table
    '''
    def clearTable(self):
        self.currentSelection = [] #clearing selection list
        self.table.clear()
        
        #clearing rows and columns
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
