import ika
from data import data, score

class SplashText():
	def __init__(self, text = 'Text Goes Here'):
		data.gains_control.append(self)
		
		self.x = int(data.map_width/2)
		self.y = int(data.map_height/2)
		
		self.font = data.Fonts["Interface"]
		self.mask = ika.Image("images\\mask.png")
		self.text = text
		
	def Update(self):
		if ika.Input.keyboard["RETURN"].Pressed():
			data.gains_control.remove(self)
		elif ika.Input.keyboard["SPACE"].Pressed():
			data.gains_control.remove(self)
	
	def Render(self):
		ika.Video.Blit(self.mask, 0, 0)
		self.font.CenterPrint(self.x, self.y, self.text)

class Notice(SplashText):
	def __init__(self, notice):
		mytext = notice + '\n\n\n'+ "Press 'Enter' to play again"
		SplashText.__init__(self, mytext)
		
	#Note: When Restart() moved to Win() / Lose()
	# bad shit happens since the program doesn't update before resetting data
	def Update(self):
		if ika.Input.keyboard["RETURN"].Pressed():
			data.gains_control.remove(self)
			from game import Restart
			Restart()
		
class Instructions(SplashText):
	def __init__(self):
		mytext = \
			"\t\t\tGreetings.  \n \
			You are cold, alone, and need shelter.	You must\n \
			gather resources (and a decent supply of tools) \n \
			in order to build yourself a place to stay warm. \n \
			\n \
			To gather materials, make either lines of 4 or 2x2 \n \
			squares of the same resource.  Once you break up a \n \
			structured block (the things that fall,) its  pieces \n \
			will fall willy-nilly.  However, once a structured  \n \
			block stops, it will not fall again until broken (it \n \
			will even defy gravity!) \n \
			\n \
			Gather the necessary resources to survive.\n \
			\n \
			Controls:  \n \
			- Move pieces with arrow keys. \n \
			- Rotate pieces with left 'control' and 'alt' buttons. \n \
			- Pause the game with 'Space'. \n \
			"
			
		SplashText.__init__(self, mytext)
		self.y = 40
		
class Scores(SplashText):
	def __init__(self):
		
		mytext = str(score) + '\n\n\n' + "(Press 'DELETE' to clear scores)"
		
		SplashText.__init__(self, mytext)
		self.y = 40
		
	def Update(self):
		if ika.Input.keyboard['DELETE'].Pressed():
			score.Clear()
			self.text = str(score) + '\n\n\n' + "(Press 'DELETE' to clear scores)"
		if ika.Input.keyboard["RETURN"].Pressed():
			data.gains_control.remove(self)
		elif ika.Input.keyboard["SPACE"].Pressed():
			data.gains_control.remove(self)
		
	
class About(SplashText):
	def __init__(self):
		mytext = \
			"\t\t\tCreated by Eve Ragins \n\n\n \
			Special thanks to 'SDHawk' for his begrugding support \n\n\n\n\n\n \
			Copyright 2009"
		
		SplashText.__init__(self, mytext)
		self.y = 100