import ika
from data import data, score
import interface
import menu
import bigblock
import splash


def StartScreen():
	data.gains_control.append(menu.StartMenu())
	
	
	from engine import MainLoop
	MainLoop()

def PlayGame():
	splash.Instructions()
	SetDifficulty()
	data.interface_objects['play area'] = interface.PlayingArea(data.tile_size*2-1, data.tile_size*2-1)
	data.interface_objects['block count'] = interface.BlockCount(270, 198)
	
	data.gains_control.append(MakeInitialBigBlocks())
	data.interface_objects['block queue'] = interface.BigBlockQueue(270, 32)
	data.game_over = False
	


def StartSelection(code):
	
	options = {'play': PlayGame,
			'sound': SetSound,
			'scores': splash.Scores,
			'about': splash.About
			}
	options[code]()
	if code != 'play':
		StartScreen()
	
	
def SetSound():
	data.gains_control.append(menu.SoundMenu())
def SoundSelection(sound):
	sounds = {'on': True,
		'off': False
		}
		
	data.sounds_enabled = sounds[sound]
	
def SetDifficulty():
	data.gains_control.append(menu.SpeedMenu())
	data.gains_control.append(menu.CabinSizeMenu())

def SetCabinSize(size):
	
	sizes = {'small': {'wood': 2, 'fur': 2, 'hammer': 2, 'stone': 2},
			'medium': {'wood': 5, 'fur': 5, 'hammer': 5, 'stone': 5},
			'large': {'wood': 10, 'fur': 10, 'hammer': 10, 'stone': 10},
			'v. large': {'wood': 15, 'fur': 15, 'hammer': 15, 'stone': 15}
			}
	names = {'small': 'Leanto',
			'medium': 'Shed    ',
			'large': 'House   ',
			'v. large': 'Mansion'
			}
	data.win_block_count = sizes[size]
	
	score.size = names[size]
		
def GetNextBigBlock():
	nextblock = data.bigblock_queue[0]
	nextblock.Start()
	data.bigblock_queue.pop(0)
	
def MakeNewBigBlock():
	x = 1
	y = 1
	b = bigblock.BigBlock(x, y)
	data.bigblock_queue.append(b)
	data.objects.append(b)

	
def ScoreBlock(block_attribute):
	if data.sounds_enabled:
		data.Sounds['pop'].Play()
	data.built_block_count[block_attribute] += 1
	score.blocks += 1
	CheckWinConditions()
	
def CheckWinConditions():
	keys = ['wood', 'fur', 'hammer', 'stone']
	
	for key in keys:
		if data.built_block_count[key] < data.win_block_count[key]:
			return
	
	Win()

def Pause():
	splash.SplashText("Paused")
	
def Win():
	data.game_over = True
	score.game_won = True
	score.SaveScore()
	splash.Scores()
	splash.Notice("You Won")
	
def Lose():
	data.game_over = True
	score.SaveScore()
	splash.Scores()
	splash.Notice("You Lost")
	
def Restart():	
	score.Reset()
	data.Reset()
	PlayGame()

##this is a class to work around blocks being made before
##difficulty was set--very cheap, sloppy, and probably a better way
class MakeInitialBigBlocks:
	def __init__(self):
		pass
	def MakeInitialBigBlocks(self):	
		global MakeNewBigBlock
		MakeNewBigBlock()
		MakeNewBigBlock()
		MakeNewBigBlock()
	def Update(self):
		#does this first time it's seen--not before
		self.MakeInitialBigBlocks()
		data.gains_control.remove(self)
	def Render(self):
		pass