from engine import data

class Entity():
	def __init__(self, x, y):
		self.dead = False
		
		global data
		self.data = data
		
	def Update(self):
		pass
	def Render(self):
		pass
		
	def IsAlive(self):
		if self.dead == False:
			return True
		return False