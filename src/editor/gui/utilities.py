from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.LerpInterval import LerpHprInterval
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject

import glob, os

debug = True

def debug(s,v=""):
	if debug == True:
		print s,v

class Utilities:
	def __init(self):
		pass
	
	@staticmethod
	def getFilesIn(directory):
		prevDir = os.getcwd()
		os.chdir(directory)
		files = glob.glob("*.egg")
		os.chdir(prevDir)
		
		return files
	
	@staticmethod
	def getEverythingIn(directory): #TODO: should this be set to be getDirectoryIn ?
		prevDir = os.getcwd()
		os.chdir(directory)
		files = glob.glob("*")
		os.chdir(prevDir)
		
		return files
		
	@staticmethod
	def getFileExtension(filename):
		chunks = filename.split(".")
		lastChunk = chunks[-1]
		return lastChunk
	
	@staticmethod
	def hasFileExtension(filename):
		chunks = filename.split(".")
		if len(chunks)>1:
			return True
		else:
			return False
	
	@staticmethod
	def getHalfPoint(p1,p2):
		x = (p1.getX()+p2.getX())/2
		y = (p1.getY()+p2.getY())/2
		z = (p1.getZ()+p2.getZ())/2
		p = Point3(x,y,z)
		return p
	
	@staticmethod
	def render2aspect(x,y,z):
		ratio = base.getAspectRatio()
		f = x * ratio
		return Point3(f,y,z)
		
	@staticmethod
	def render2aspect(pos):
		x = pos.getX()
		y = pos.getY()
		z = pos.getZ()
		ratio = base.getAspectRatio()
		f = x * ratio
		return Vec3(f,y,z)
		
	@staticmethod
	def aspect2render(x,y,z):
		ratio = base.getAspectRatio()
		f = x / ratio
		return Point3(f,y,z)
		
	@staticmethod
	def aspect2render(pos):
		x = pos.getX()
		y = pos.getY()
		z = pos.getZ()
		ratio = base.getAspectRatio()
		f = x / ratio
		return Point3(f,y,z)
