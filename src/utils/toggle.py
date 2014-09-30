'''
Simple toggle data structure that alternates value between true and false
'''
class Toggle:
	def __init__(self, start):
		self.value = start
	
	def get(self):
		return self.value
		
	def toggle(self):
		if self.value == False:
			self.value = True
		else:
			self.value = False
