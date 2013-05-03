import ika
from data import data
import game

"""
TODO:
-take out non-tribal stuff

-center cursor in middle (vertically) of slot instead of top-left
-add option for menu to have a header (ie, if list['header']....)
-add option to display tooltips (probably best done by re-reversing dict 
	to normal and have it return key instead of value so that
	value would become tooltip... I was having fun and didn't see need for 
	the functionality -- an easy enough fix.)
-change position of menu to set x/y coords instead of
	trying to center on screen. That entire FigureAndSetXY() should probably
	be revamped.
	(user movable? ...no. that would be controlled by another class if/when immplemented) 
-tweak borders so a) not off center b) can be pretty
-add mouse functionality
-add functionality (possibly) such that a list (not dict) could be 
	used instead with blank tooltips (ie. probably just turn list into dict
	then procede as usual)
-possibly compact Select() into Menu() as indicated in note (near bottom)
"""

cursors = {'face': ika.Image('images\\cursor_face.png')
			}

class Slot():
	def __init__(self, x, y, text, parent):
		self.x = x
		self.y = y
		
		self.margin = parent.margin
		self.font = parent.font
		self.cursor = parent.cursor
		
		self.text_x = self.x + parent.cursor_size + self.margin
		self.text_y = self.y + self.margin
		
		self.text = text
		self.selected = False
		
	def Render(self):
		if self.selected:
			self.cursor.Blit(self.x, self.y + self.margin)
		self.font.Print(self.text_x, self.text_y, self.text)
		
class Menu():
	def __init__(self, list = {'this': 'this_', 'a': 'a_', 'test':'test_', 'menu': 'menu_'}):
		
		self.font = data.Fonts["Interface"]
		
		global cursors
		self.cursor = cursors['face']
		self.cursor_size = 16
		
		#Note: This dictionary is backwards.
		#The keys are what is displayed, the program operates with the values.
		self.list = list
		
		self.menu_options = self.list.keys()
		
		#none of these values are set in stone.. they are simply there to be initialized
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0
		
		self.margin = 5 ##
		
		self.FigureAndSetXY()
		
		self.slots = []
		self.MakeSlots()
		
		self.current_selection = 0
		self.InitializeSelectedSlot()
		
		self.calls = None
		self.returns_to = None
		
		self.mask = ika.Image("images\\mask.png")
		
	def Update(self):
		if ika.Input.keyboard["UP"].Pressed():
			self.CursorUp()
		if ika.Input.keyboard["DOWN"].Pressed():
			self.CursorDown()
		if ika.Input.keyboard["RETURN"].Pressed():
			self.Select()
		if ika.Input.keyboard['ESCAPE'].Pressed():
			self.Return()
			
	def Render(self):
		ika.Video.Blit(self.mask, 0 ,0)
		ika.Video.DrawRect(self.x-1, self.y-1, self.x + self.width + 1, self.y + self.height + 1, data.color['white'], 0)
		ika.Video.DrawRect(self.x, self.y, self.x + self.width, self.y + self.height, data.color['black'], 1)
		
		for slot in self.slots:
			slot.Render()
		
	def FigureAndSetXY(self):
		font_height = self.font.height
		#figure x
		max_string_width = 0
		for option in self.menu_options:
			w = self.font.StringWidth(option)
			if w > max_string_width:
				max_string_width = w
		board_center_x = int(data.map_width/2)
		#set x
		self.x = board_center_x - int(max_string_width/2) - self.margin - 8 ##see below me
		self.width = max_string_width + 3*self.margin + 16 ##16 = cursor size, should not be const
		
		#figure y
		needed_text_y = len(self.menu_options)*(font_height+1)
		board_center_y = int(data.map_height/2)
		#set y
		self.y = board_center_y - int(needed_text_y/2) - self.margin
		self.height = needed_text_y + 2*self.margin
	
	def MakeSlots(self):
		x = self.x + self.margin
		y = self.y + self.margin
		font_height = self.font.height
		
		for i, option in enumerate(self.menu_options):
			new_slot = Slot(x, y, option, self)
			self.slots.append(new_slot)
			y += font_height
	def InitializeSelectedSlot(self):
		self.slots[self.current_selection].selected = True
		
	def CursorUp(self):
		#note: does not act on a cursor, but rather tells selected slot to display cursor
		self.current_selection -= 1
		try:
			self.slots[self.current_selection].selected = True
			self.slots[self.current_selection+1].selected = False
		except:
			self.current_selection += 1
	
	def CursorDown(self):
		#note: does not act on a cursor, but rather tells selected slot to display cursor
		self.current_selection += 1
		try:
			self.slots[self.current_selection].selected = True
			self.slots[self.current_selection-1].selected = False
		except:
			self.current_selection -= 1
	
	def Select(self):
		slot = self.slots[self.current_selection]
		key = slot.text
		program_code = self.list[key]
		data.gains_control.remove(self)
		self.calls(program_code)
	
	def Return(self):
		data.gains_control = [] #.remove(self)
		self.returns_to()
		
class SpeedMenu(Menu):
	def __init__(self):
		self.speeds = {'Slow': 24,
			'Medium': 18,
			'Fast': 12,
			'Very Fast': 6
			}
		Menu.__init__(self, self.speeds)
				
		self.returns_to = game.StartScreen
		
	def Select(self):
		
		data.gains_control.remove(self)
		slot = self.slots[self.current_selection]
		program_code = slot.text
		data.block_speed = self.speeds[program_code]
		
		from data import score
		score.speed = slot.text
		
class CabinSizeMenu(Menu):
	def __init__(self):
		list = {"Leanto": 'small',
				'Shed    ':'medium',
				'House   ': 'large',
				'Mansion': 'v. large'
				}
		Menu.__init__(self, list)
		self.calls = game.SetCabinSize
		self.returns_to = game.StartScreen
		
class SoundMenu(Menu):
	def __init__(self):
		list = {"Sounds On": 'on',
				"Sounds Off":"off"
				}
		Menu.__init__(self, list)
	
		self.calls = game.SoundSelection
		self.returns_to = game.StartScreen
		
class StartMenu(Menu):
	def __init__(self):
		list = {"Play Game": 'play',
				"Sound": 'sound',
				"View Scores": 'scores',
				"About": 'about'
				}
		
		self.titleImage = ika.Image("images\\title.png")
		Menu.__init__(self,list)
		
		self.calls = game.StartSelection
		self.returns_to = game.StartScreen
	
		
	def Render(self):
		ika.Video.Blit(self.titleImage, 60,50)
		
		ika.Video.DrawRect(self.x-1, self.y-1, self.x + self.width + 1, self.y + self.height + 1, data.color['white'], 0)
		ika.Video.DrawRect(self.x, self.y, self.x + self.width, self.y + self.height, data.color['black'], 1)
		
		for slot in self.slots:
			slot.Render()
		