import block
import shapes
import ika
from data import data
import entity
import timer

block_types = ['stone', 'wood', 'fur', 'hammer']
possible_blocks = {'stone': block.Stone, 
					'wood': block.Wood, 
					'fur': block.Fur, 
					'hammer': block.Hammer
					}

class BigBlock(entity.Entity):
	def __init__(self, x, y):
		entity.Entity.__init__(self, x,y)
		
		self.shape, self.outlines = shapes.GetShape() #returns 2d array of 1s and 0s
		#shape: a 2d array comprised of 1s and 0s to define the offsets for when Blocks are made
		#as Blocks are made, the 1s are replaced with a string representing type of block made
		
		self.outline_num = 0
		
		self.x = x
		self.y = y
		
		self.speed = data.block_speed
		self.moving = False
		self.waiting = True
		
		self.blocks = []
		#blocks: a list of Block objects
		self.speed_regulator = 0
		
		self.pressed = False
		self.timer = timer.Timer(30)
		
		self.MakeNewBlocksForShape()
		
		
	def Update(self):
		if self.IsMoving():
			kb = ika.Input.keyboard

			#rotating
			if kb["LCTRL"].Pressed():
				self.Rotate()
			if kb["LALT"].Pressed():
				self.ReverseRotate()
				
			#left
			if kb["LEFT"].Position():
				if self.pressed == False:
					self.timer.Reset()
					self.pressed = True
					self.MoveLeft()
				
				if self.pressed and self.timer.IsDone():
					self.MoveLeft()
			
			#right			
			if kb["RIGHT"].Position():
				if self.pressed == False:
					self.timer.Reset()
					self.pressed = True
					self.MoveRight()
				
				if self.pressed and self.timer.IsDone():
					self.MoveRight()
			
			#up/fall			
			if kb["UP"].Pressed():
				if data.sounds_enabled:
					data.Sounds['move'].Play()
				self.Fall()
			
			#down
			if kb["DOWN"].Position():
				if self.pressed == False:
					self.timer.Reset()
					self.pressed = True
					self.MoveDown()
					if data.sounds_enabled:
						data.Sounds['move'].Play()

				if self.pressed and self.timer.IsDone():
					self.MoveDown()
					if data.sounds_enabled:
						data.Sounds['move'].Play()

			
			#pause
			if kb['SPACE'].Pressed():
				import game
				game.Pause()
			
			#natural falling
			if self.speed_regulator == self.speed:
				self.speed_regulator = 0
				self.MoveDown()
			self.speed_regulator += 1
			
			self.UpdateBlocks()
		
			#reset 'pressed' position
			if kb["DOWN"].Position() == 0 \
				and kb["RIGHT"].Position() == 0 \
				and kb["LEFT"].Position() == 0:
				self.pressed = False
				
				
	def Render(self):
		for block in self.blocks:
			block.Render()
		if not self.waiting:
			self.outlines[self.outline_num].Blit(data.board[self.x][self.y].x, data.board[self.x][self.y].y, 1)
		
	def Start(self):
		self.SetXY(3, 0)
		self.waiting = False
		self.moving = True
	def IsWaiting(self):
		return self.waiting
	def IsMoving(self):
		return self.moving
	def Stop(self):
		if self.moving is True:
			self.moving = False
		self.UpdateBlocksXY()
		for block in self.blocks:	#this must be seperate to ensure all blocks in engine.
			game_lost = block.ParentStopped()	
			if game_lost: 
				break		#MUST break out of loop before calling Lose(), or any other kids might cause multiple losses
		if game_lost:
			from game import Lose
			Lose()
	
	def ChildDied(self):
		self.Die()
	def Die(self):
		for block in self.blocks:
			data.objects.append(block)
			block.ParentDied()
		self.dead = True
		
	def CheckIfBlocksCollide(self):
		for block in self.blocks:
			block.UpdateXY()
			col = block.Collides()
			if col:
				return True
				
		return False
	

	"""
	===========================================================================
	-----ROTATION--------------------------------------------------------------
	===========================================================================
	"""	
	def Rotate(self):
		num_rows, num_cols = self.GetNewShapeSize()
		new_shape= [[0 for i in range(num_cols)] for j in range(num_rows)]
		
		old_shape = self.shape
		old_x_y = self.x, self.y
		
		for i, array in enumerate(reversed(self.shape)):
			for j, slot in enumerate(array):
				new_shape[j][i] = slot
		
		self.shape = new_shape
		self.MakeNewBlocksForShape()
		
		for block in self.blocks:
			block.UpdateXY()
		
		if self.FitBlock() == False:
			self.shape = old_shape
			self.x, self.y = old_x_y
			self.UpdateBlocksXY()
			self.MakeNewBlocksForShape()
		else:
			self.outline_num += 1
			if self.outline_num >= len(self.outlines):
				self.outline_num = 0
	
	def FitBlock(self):
		for block in self.blocks:
			while block.CollidesAt() == 'bottom':
				self.y -= 1
				self.UpdateBlocksXY()
			while block.CollidesAt() == 'right':
				self.x -= 1
				self.UpdateBlocksXY()
			if block.CollidesAt() == 'block':
				return False
	
	def ReverseRotate(self):
		num_rows, num_cols = self.GetNewShapeSize()
		new_shape= [[0 for i in range(num_cols)] for j in range(num_rows)]
		
		old_shape = self.shape

		for i, array in enumerate(self.shape):
			for j, slot in enumerate(reversed(array)):
				new_shape[j][i] = slot

		self.shape = new_shape
		self.MakeNewBlocksForShape()
		
		for block in self.blocks:
			block.UpdateXY()
		
		if self.FitBlock() == False:
			self.shape = old_shape
			self.MakeNewBlocksForShape()
		else:
			self.outline_num -= 1
			if self.outline_num < 0:
				self.outline_num = len(self.outlines) - 1
				
	

	"""
	===========================================================================
	-----CREATION--------------------------------------------------------------
	===========================================================================
	"""		
	def MakeNewBlocksForShape(self):
		self.DeleteAnyOldBlocks()
		
		global possible_blocks
		global block_types
		num_options = len(possible_blocks)
		
		for outside, array in enumerate(self.shape):
			for inside, slot in enumerate(array):
				if slot != 0:
					x = self.x
					x_offset = inside
					y = self.y + outside
					y_offset = outside
					
					if slot == 1:		#doesn't have a type
						rand_num = ika.Random(0, num_options)
						type = block_types[rand_num]
						slot = type		#this only lasts for duration of for statement
						self.shape[outside][inside] = type	#saves type to shape
						
					self.MakeMiniBlock(slot,x, y, x_offset, y_offset)
	
	def MakeMiniBlock(self, type, x, y, x_offset, y_offset):
		block = possible_blocks[type](x, y, x_offset, y_offset, self)
		self.blocks.append(block)
		
	def DeleteAnyOldBlocks(self):
		self.blocks = []
	
	def GetNewShapeSize(self):
		num_old_rows = len(self.shape)
		num_old_cols = len(self.shape[0])
		return num_old_cols, num_old_rows	 #return reverse, since that's all it is
		
	
	"""
	===========================================================================
	-----MOVEMENT----------------------------------------------------------
	===========================================================================
	"""	

	def MoveLeft(self):
		if data.sounds_enabled:
			data.Sounds['move'].Play()
		
		self.x -= 1
		col = self.CheckIfBlocksCollide()
		if col:
			self.x += 1
			return False
				
		return True
		
	def MoveUp(self):
		self.y -= 1
		self.UpdateBlocksXY()
		return True
	def MoveDown(self):
		self.y += 1
		col = self.CheckIfBlocksCollide()
		if col:
			self.y -= 1
			self.Stop()
			
	def MoveRight(self):
		if data.sounds_enabled:
			data.Sounds['move'].Play()
		self.x += 1
		col = self.CheckIfBlocksCollide()
		if col:
			self.x -= 1
			return False
			
		return True
	
	def Fall(self):
		while self.moving is True:
			self.MoveDown()
			
	
		
	"""
	===========================================================================
	-----UPDATING POSITIONS----------------------------------------------------
	===========================================================================
	"""	
	def SetXY(self,x,y):
		self.x = x
		self.y = y
		self.UpdateBlocksXY()
	
	def UpdateBlocks(self):
		for block in self.blocks:
			block.Update()
	def UpdateBlocksX(self):
		for block in self.blocks:
			block.UpdateX()
	def UpdateBlocksY(self):
		for block in self.blocks:
			block.UpdateY()
	def UpdateBlocksXY(self):
		for block in self.blocks:
			block.UpdateXY()