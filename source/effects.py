import ika
import timer

class Explosion(object):
	def __init__(self, x, y, size):
		self.x = x
		self.y = y
		self.size = size
		self.dead = False
		self.color = ika.RGB(255,244,172, 140)
		self.timer = timer.Timer(15)
		self.timer.Reset()
	
	def Update(self):
		if self.timer.IsDone():
			self.Die()
	
	def Render(self):
		ika.Video.DrawRect(self.x, self.y, self.x + self.size, self.y + self.size, self.color, 2)
		
	def Die(self):
		self.dead = True