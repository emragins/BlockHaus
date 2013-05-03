import ika


#holds data for each spot on the playing board
class BoardInfo(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.block = None
	
	def __str__(self):
		string = 'x, y, block: ' +str(self.x/16)+' ' + str(self.y/16)+ ' ' + str(self.block)
		return string

#holds data for various aspects of the game (most to be shared with all)
class Data(object):
	def __init__(self):
		self.tile_size = 16
		self.map_height = 480
		self.map_width = 600
		self.board_width = 10
		self.board_height = 20
		self.sounds_enabled = True
		
		self.InitGameData()
		
		self.win_block_count = {'wood': 0, 'fur': 0, 'hammer': 0, 'stone':0}
	
		self.Fonts =	 {
			"Interface" : ika.Font("ocr_grey.fnt"),
			"Interface Green" : ika.Font("ocr_green.fnt"),
			"Interface Yellow" : ika.Font("ocr_yellow.fnt"),
			"Interface Red" : ika.Font("ocr_red.fnt"),
			}
	
		self.color = {
			'white': ika.RGB(255,255,255),
			'black': ika.RGB(0,0,0)
			}
	
		self.Sounds = {
			'move': ika.Sound("sounds\\move.wav"),
			'pop': ika.Sound("sounds\\pop.wav"),
			'fall': ika.Sound("sounds\\drop.wav"),
			}
			
					
	def InitGameData(self):
		board_dist_from_edge = self.tile_size*2
		self.board = [[BoardInfo(j*self.tile_size + board_dist_from_edge, i*self.tile_size+ board_dist_from_edge) \
						for i in range(self.board_height)] for j in range(self.board_width)]
		
		self.gains_control = []
		self.interface_objects = {}
		self.objects = []
		self.bigblock_queue = []
		self.game_over = True
		self.block_speed = 16
		self.built_block_count = {'wood': 0, 'fur': 0, 'hammer': 0, 'stone':0}
		
	def PrintBoard(self):
		for i, row in enumerate(self.board):
			for j in row:
				print j
				
	def Reset(self):
		self.InitGameData()
		
import shelf

class Score(object):
	def __init__(self):
		self.Reset()
		
		self.shelf = shelf.Shelf("scores.pydat")
		
		self.scores = []
		self.LoadScores()
	
	def Reset(self):
		self.speed = ''
		self.size = ''
		self.blocks = 0
		self.total = 0
		self.game_won = False
		
	def __str__(self):
		str = ''
		for score in self.scores:
			str += score + '\n'
		if str == '':
			str = "No scores here!"
		return str
		
	def ComputeTotal(self):
		size_multiplier = {'Leanto': 1,
						'Shed    ': 2,
						'House   ': 3,
						'Mansion': 4,
						'': 0}
		speed_multiplier = {'Slow': 1,
			'Medium': 2,
			'Fast': 3,
			'Very Fast': 4,
			'': 0
			}
			
		self.total = self.blocks * size_multiplier[self.size] * speed_multiplier[self.speed]
		if self.game_won:
			self.total = self.total * 2
		self.total = str(self.total)
		##bad code here
		while len(self.total) < 4:
			self.total = '0' + self.total
		
	def SaveScore(self):
		self.ComputeTotal()
		score_str = str(self.total) +'\t\t' + self.size + '\t\t' + self.speed
		self.scores.append(score_str)
		self.scores.sort(reverse = True)
		if len(self.scores) > 17:
			self.scores.pop()
		self.Save()
		
	def LoadScores(self):
		self.scores = self.shelf.Read()
		
	def Save(self):
		self.shelf.Write(self.scores)
		
	def Clear(self):
		self.scores = []
		self.Save()
	
data = Data()
score = Score()

