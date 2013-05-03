import ika
from data import data
import entity
import regex
import effects

images = {'default':ika.Image("images\\wood.png"), #change to something ugly
		'wood': ika.Image("images\\wood.png"), 
		'stone': ika.Image("images\\stone.png"),
		'fur': ika.Image("images\\fur.png"),
		'hammer': ika.Image("images\\hammer.png")
		}
		
class Block(entity.Entity):
	def __init__(self, x, y, x_offset, y_offset, parent):
		entity.Entity.__init__(self, x, y)
		global images
		
		self.x = x
		self.y = y
		self.x_offset = x_offset
		self.y_offset = y_offset
		
		self.attribute = 'default'		#I should never see this
		self.image = images[self.attribute]
		
		self.parent = parent
		self.parent_alive = True
		
		self.board = self.data.interface_objects['play area']
		self.moving = False
		speed_regulator = 0
		
		self.game_lost = False #this is needed to tell the parent to break the loop *as soon as* 
								#one of its children goes over.  If not done:
								#the game ends and the score  shows as it should
								#BUT... between the time the score shows and the end of the MainLoop,
								#the rest of the parent's children check for loss...
								#If these children also make a loss, game.Lose() is ran multiple times
								#and thus the score is recorded multiple times.
		
	def Update(self):
		if self.parent_alive:
			if self.parent.IsMoving():
				self.UpdateXY()
				
		elif self.moving == False:
			supported = False
			if self.y + 1 >= self.data.board_height:
				supported = True
			elif self.data.board[self.x][self.y+1].block != None:
				supported = True
			if supported == False:
				self.Start()
		
		if self.moving:
			self.speed_regulator += 1
			if self.speed_regulator == 6:
				self.RemoveFromBoard()
				self.speed_regulator = 0
				self.y += 1
				if data.sounds_enabled:
					data.Sounds['fall'].Play()
				if self.Collides():
					self.y -= 1
					self.Stop()
				self.AddToBoard()
			
	def UpdateX(self):
		if self.parent.waiting:
			self.x = self.parent.x + self.x_offset*self.data.tile_size
		else:
			self.x = self.parent.x + self.x_offset
	def UpdateY(self):
		if self.parent.waiting:
			self.y = self.parent.y + self.y_offset*self.data.tile_size
		else:
			self.y = self.parent.y + self.y_offset
	def	UpdateXY(self):
		self.UpdateX()
		self.UpdateY()
		
	"""
	===========================================================================
	-----COLLISIONS-------------------------------------------------
	===========================================================================
	"""
	def Collides(self):
		if self.y > self.data.board_height -1:
			return True
		
		if self.x == -1:
			return True
		
		if self.x > self.data.board_width - 1:
			return True
		
		if self.data.board[self.x][self.y].block != None:
			return True
			
		return False
		
	def CollidesAt(self):
		if self.y > self.data.board_height -1:
			return 'bottom'
		
		if self.x == -1:
			return 'left'
		
		if self.x > self.data.board_width - 1:
			return 'right'
		
		if self.data.board[self.x][self.y].block != None:
			return 'block'
			
		return 'none'
		
	def IsOutsideGameArea(self):
		if self.x >= self.data.board_width - 1:
			return True
		return False
	"""
	===========================================================================
	----LIFE---------------------------------
	===========================================================================
	"""
	
	def ParentDied(self):
		self.parent_alive = False
		if self.dead == False:
			self.Start()
	def ParentStopped(self):
		self.Stop()
		if self.game_lost:
			return True
	def Start(self):
		self.speed_regulator = 0
		self.moving = True
	def Stop(self):
		self.moving = False
		self.AddToBoard()
		was_shape = self.CheckForShapes()
		if was_shape == False:
			self.game_lost = self.CheckForLoss()
			
				
	def AddToBoard(self):
		self.data.board[self.x][self.y].block = self
	def RemoveFromBoard(self):
		self.data.board[self.x][self.y].block = None
	
	def Die(self):
		self.dead = True
		self.AnimateDeath()
		#self.RemoveFromBoard()		#Should now be taken care of in Engine
		if self.parent_alive:
			self.parent.ChildDied()
		
	def AnimateDeath(self):
		x = data.board[self.x][self.y].x
		y = data.board[self.x][self.y].y
		boom = effects.Explosion(x, y, 16)
		data.objects.append(boom)
	
	def CheckForLoss(self):
		if self.y == 0:
			return True

	"""
	===========================================================================
	-----BELOW HERE IS ALL CHECKING FOR SHAPES---------------------------------
	===========================================================================
	"""
	
	def CheckForShapes(self):
		from game import ScoreBlock
		
		v_used_objects = []
		h_used_objects = []
		square_used_objects = []
		
		v_num = self.CheckForVerticalLine(v_used_objects)
		h_num = self.CheckForHorizontalLine(h_used_objects)
		square_num = self.CheckForSquare(square_used_objects)
		
		
		if v_num > 0:
			self.KillBlocks(v_used_objects)
			for i in range(0, v_num):
				ScoreBlock(self.attribute)
				
		if h_num > 0:
			self.KillBlocks(h_used_objects)
			for i in range(0, h_num):
				ScoreBlock(self.attribute)
					
		if square_num > 0:
			self.KillBlocks(square_used_objects)
			for i in range(0, square_num):
				ScoreBlock(self.attribute)
			
		if h_num > 0 or v_num > 0 or square_num > 0:
			return True	
		return False
		
	def KillBlocks(self, used_objects):
		for obj in used_objects:
			if obj.IsAlive():
				obj.Die()
			
	def CheckForHorizontalLine(self, used_objects):
		shape_maker = [0,0,0,1,0,0,0]
		"""
		Positions:
			[0,1,2,3,4,5,6]
		"""
		temp_used_objects = {}
		temp_used_objects[3]= self
		
		
		for j, i in enumerate([-3, -2, -1, 1, 2, 3]):
			try:		
				if self.data.board[self.x + i][self.y].block != None:
					block = self.data.board[self.x + i][self.y].block
					if block.attribute == self.attribute:
						shape_maker[i + 3] = 1
						pos = i + 3
						temp_used_objects[pos] = block
			except:
				pass
		
		match_list = regex.CheckForLine(shape_maker)
		
		matches = {'a': [0,1,2,3],
					'b': [1,2,3,4],
					'c': [2,3,4,5],
					'd': [3,4,5,6]
					}
					
		num_matches = 0
		if match_list != []:		
			#for each line that exists
			for list in match_list:
				match_accounted_for = False	
				
				#for each object in that set
				for pos in matches[list]:
					temp_obj = temp_used_objects[pos]
					used_objects.append(temp_obj)
					if match_accounted_for is False:
						if temp_obj.IsAlive():
							num_matches +=1
							match_accounted_for = True
					
			
			#get rid of duplicates
			used_objects = set(used_objects)
			
		return num_matches
		
		
				
	def CheckForVerticalLine(self, used_objects):
		shape_maker = [0,0,0,1,0,0,0]
		"""
		Positions:
			[0,1,2,3,4,5,6]
		"""
		temp_used_objects = {}
		temp_used_objects[3]= self
		
		for j, i in enumerate([-3, -2, -1, 1, 2, 3]):
			try:
				if self.data.board[self.x][self.y + i].block != None:
					block = self.data.board[self.x][self.y + i].block
					if block.attribute == self.attribute:
						shape_maker[i + 3] = 1
						pos = i + 3
						temp_used_objects[pos] = block
			except:
				pass
				
				
		match_list = regex.CheckForLine(shape_maker)
		
		matches = {'a': [0,1,2,3],
					'b': [1,2,3,4],
					'c': [2,3,4,5],
					'd': [3,4,5,6]
					}
		
					
		num_matches = 0
		if match_list != []:		
			#for each line that exists
			for list in match_list:
				match_accounted_for = False	
				
				#for each object in that set
				for pos in matches[list]:
					temp_obj = temp_used_objects[pos]
					used_objects.append(temp_obj)
					if match_accounted_for is False:
						if temp_obj.IsAlive():
							num_matches +=1
							match_accounted_for = True
					
			
			#get rid of duplicates
			used_objects = set(used_objects)
			
		return num_matches
		
		
	def CheckForSquare(self, used_objects):
		"""
		Positions:
			[[1,2,3],
			[4,5,6],
			[7,8,9]]
		"""
		temp_used_objects = {}
		temp_used_objects[5] = self
		shape_maker = [[0,0,0],
						[0,1,0],
						[0,0,0]]
		
		matches = {'top_right': [2,3,5,6],
					'bottom_right': [5,6,8,9],
					'top_left': [1,2,4,5],
					'bottom_left': [4,5,7,8]
					}
		
		try:		
			if self.data.board[self.x-1][self.y-1].block != None:
				block = self.data.board[self.x-1][self.y-1].block
				if block.attribute == self.attribute:
					shape_maker[0][0] = 1
					pos = 1
					temp_used_objects[pos] = block
		except:
			pass
		try:		
			if self.data.board[self.x-1][self.y].block != None:
				block = self.data.board[self.x-1][self.y].block
				if block.attribute == self.attribute:
					shape_maker[1][0] = 1
					pos = 4
					temp_used_objects[pos] = block
		except:
			pass
		try:		
			if self.data.board[self.x-1][self.y+1].block != None:
				block = self.data.board[self.x-1][self.y+1].block
				if block.attribute == self.attribute:
					shape_maker[2][0] = 1
					pos = 7
					temp_used_objects[pos] = block
		except:
			pass
		try:		
			if self.data.board[self.x][self.y-1].block != None:
				block = self.data.board[self.x][self.y-1].block
				if block.attribute == self.attribute:
					shape_maker[0][1] = 1
					pos = 2
					temp_used_objects[pos] = block
		except:
			pass
		try:		
			if self.data.board[self.x][self.y+1].block != None:
				block = self.data.board[self.x][self.y+1].block
				if block.attribute == self.attribute:
					shape_maker[2][1] = 1
					pos = 8
					temp_used_objects[pos] = block
		except:
			pass
		try:		
			if self.data.board[self.x+1][self.y-1].block != None:
				block = self.data.board[self.x+1][self.y-1].block
				if block.attribute == self.attribute:
					shape_maker[0][2] = 1
					pos = 3
					temp_used_objects[pos] = block
		except:
			pass
		try:		
			if self.data.board[self.x+1][self.y].block != None:
				block = self.data.board[self.x+1][self.y].block
				if block.attribute == self.attribute:
					shape_maker[1][2] = 1
					pos = 6
					temp_used_objects[pos] = block
		except:
			pass
		try:		
			if self.data.board[self.x+1][self.y+1].block != None:
				block = self.data.board[self.x+1][self.y+1].block
				if block.attribute == self.attribute:
					shape_maker[2][2] = 1
					pos = 9
					temp_used_objects[pos] = block
		except:
			pass

		match_list = regex.CheckForSquare(shape_maker)
		
					
		num_matches = 0
		if match_list != []:		
			#for each line that exists
			for list in match_list:
				match_accounted_for = False	
				
				#for each object in that set
				for pos in matches[list]:
					temp_obj = temp_used_objects[pos]
					used_objects.append(temp_obj)
					if match_accounted_for is False:
						if temp_obj.IsAlive():
							num_matches +=1
							match_accounted_for = True
					
			#get rid of duplicates
			used_objects = set(used_objects)
			
		return num_matches
		
		
	def Render(self):
		if self.parent.waiting:
			self.image.Blit(self.x, self.y)
		else:
			try:
				self.image.Blit(self.data.board[self.x][self.y].x, self.data.board[self.x][self.y].y)
			except:
				print 'block', self,'out of range in x, y'
				print 'block', self,'x, y:', self.x, self.y
				#Cannot set block to die, because it tries to remove from board... = error.
				#this somehow seems to take care of itself
				#print 'killing block', self
				#self.Die()
				
class Stone(Block):
	def __init__(self, x, y, x_offset, y_offset, parent):
		Block.__init__(self, x, y, x_offset, y_offset, parent)
		self.attribute = 'stone'
		self.image = images[self.attribute]
class Fur(Block):
	def __init__(self, x, y, x_offset, y_offset, parent):
		Block.__init__(self, x, y, x_offset, y_offset, parent)
		self.attribute = 'fur'
		self.image = images[self.attribute]
class Wood(Block):
	def __init__(self, x, y, x_offset, y_offset, parent):
		Block.__init__(self, x, y, x_offset, y_offset, parent)
		self.attribute = 'wood'
		self.image = images[self.attribute]
class Hammer(Block):
	def __init__(self, x, y, x_offset, y_offset, parent):
		Block.__init__(self, x, y, x_offset, y_offset, parent)
		self.attribute = 'hammer'
		self.image = images[self.attribute]