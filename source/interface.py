import ika
from engine import data
import collision

class InterfaceArea(collision.HollowBox):
	def __init__(self, x, y, width, height):
		collision.HollowBox.__init__(self, x, y, width, height)
		
		self.x = x
		self.y = y
		
		self.width = width
		self.height = height
		
		global data
		self.data = data
		
		self.tile_size = self.data.tile_size
		self.color = self.data.color['white']
		self.background_color = self.data.color['black']
		
	def Update(self):
		pass
		
	def Render(self):
		ika.Video.DrawRect(self.x, self.y, self.x+self.width, self.y+self.height, self.background_color, 1)
		ika.Video.DrawRect(self.x, self.y, self.x+self.width, self.y+self.height, self.color, 0)

		
class PlayingArea(InterfaceArea):
	def __init__(self, x, y):
		InterfaceArea.__init__(self, x, y, 1, 1)
		self.width = self.tile_size*self.data.board_width+1
		self.height = self.tile_size*self.data.board_height+1
		
class BigBlockQueue(InterfaceArea):
	def __init__(self, x, y):
		InterfaceArea.__init__(self, x, y, 1, 1)
		self.width = self.tile_size*16
		self.height = self.tile_size*4
		
		
		self.slot1_x = self.x + self.tile_size
		self.slot1_y = self.y + self.tile_size
		self.slot2_x = self.slot1_x + self.tile_size*5
		self.slot2_y = self.slot1_y
		self.slot3_x = self.slot2_x + self.tile_size*5
		self.slot3_y = self.slot1_y
		
		self.UpdateQueueBlocks()
	'''
	def Render(self):
		ika.Video.DrawRect(self.x, self.y, self.x+self.width, self.y+self.height, self.background_color, 1)
		ika.Video.DrawRect(self.x, self.y, self.x+self.width, self.y+self.height, self.color, 0)
	'''
	
	def UpdateQueueBlocks(self):
		try:
			self.data.bigblock_queue[0].SetXY(self.slot1_x, self.slot1_y)
			self.data.bigblock_queue[1].SetXY(self.slot2_x, self.slot2_y)
			self.data.bigblock_queue[2].SetXY(self.slot3_x, self.slot3_y)
		except:
			pass
			
class BlockCount(InterfaceArea):
	def __init__(self, x, y):
		InterfaceArea.__init__(self, x, y, 1,1)
		self.width = self.tile_size*16
		self.height = self.tile_size*16
		
		self.font_x = self.x + 2*self.tile_size
		
		self.font = self.data.Fonts["Interface"]
		self.red = self.data.Fonts["Interface Red"]
		self.yellow = self.data.Fonts["Interface Yellow"]
		self.green = self.data.Fonts["Interface Green"]
		
	def Render(self):
		ika.Video.DrawRect(self.x, self.y, self.x+self.width, self.y+self.height, self.background_color, 1)
		ika.Video.DrawRect(self.x, self.y, self.x+self.width, self.y+self.height, self.color, 0)
		
		wood_count = self.data.built_block_count['wood']
		stone_count = self.data.built_block_count['stone']
		fur_count = self.data.built_block_count['fur']
		hammer_count = self.data.built_block_count['hammer']
		
		##all the same for now... if ever you vary numbers, this will need to change
		max = self.data.win_block_count['wood']
		half = int(max/2)
		
		
		if wood_count <= half:
			self.red.Print(self.font_x, self.y + self.tile_size*2, "Wood: " + str(wood_count) + '/' +str(max))
		elif wood_count < max:
			self.yellow.Print(self.font_x, self.y + self.tile_size*2, "Wood: " + str(wood_count) + '/' +str(max))
		else:
			self.green.Print(self.font_x, self.y + self.tile_size*2, "Wood: " + str(wood_count) + '/' +str(max))
		
		if stone_count <=half:
			self.red.Print(self.font_x, self.y + self.tile_size*5, "Stone: " + str(stone_count) + '/' + str(max))
		elif stone_count < max:
			self.yellow.Print(self.font_x, self.y + self.tile_size*5, "Stone: " + str(stone_count) + '/' + str(max))
		else:
			self.green.Print(self.font_x, self.y + self.tile_size*5, "Stone: " + str(stone_count) + '/' + str(max))
		
		if fur_count <= half:
			self.red.Print(self.font_x, self.y + self.tile_size*8, "Fur: " + str(fur_count) + '/' +str(max))
		elif fur_count < max:
			self.yellow.Print(self.font_x, self.y + self.tile_size*8, "Fur: " + str(fur_count) + '/' +str(max))
		else:
			self.green.Print(self.font_x, self.y + self.tile_size*8, "Fur: " + str(fur_count) + '/' +str(max))
		
		if hammer_count <= half:
			self.red.Print(self.font_x, self.y + self.tile_size*11, "Tools: " + str(hammer_count) + '/' + str(max))
		elif hammer_count < max:
			self.yellow.Print(self.font_x, self.y + self.tile_size*11, "Tools: " + str(hammer_count) + '/' + str(max))
		else: 
			self.green.Print(self.font_x, self.y + self.tile_size*11, "Tools: " + str(hammer_count) + '/' + str(max))