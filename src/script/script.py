class Script:
	def __init__(self):
		print "scripts are ready to use"
	
	def load(self, resname):
		rl = resourceManager.getResource(resname)
		print "attempt to load script" + rl
		
		script = open(rl)
		exec(script.read())
