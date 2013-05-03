import ika
import manager
from data import data
import game

last_fps = 0

Backgrounds = {
			'plain': ika.Image("images\\background3.png")
			}
		
current_background = Backgrounds['plain']		
		
		
Music = {
		}
		
m = ""		
mname = ""

def PlayMusic(mus):
	global m, mname
	
	mname = mus
	m = ika.Music(Music[mus])
	m.Play()
	m.loop = 1
	
def UpdateObjects():
	global data
	"""
	Note:
	Occassionally this 'for... objects' loop will completely skip the block that is falling.
	This means that it does not see it to test that it is falling, despite the block clearly existing in 
	'objects' both before and after the loop.  Therefore, the game tells a second block to start falling.
	"""
	
	if data.gains_control != []:
		data.gains_control[0].Update()
	else:
		num_blocks_falling = 0
		for i, obj in enumerate(data.objects):
			if hasattr(obj, "blocks") and obj.IsMoving():
				num_blocks_falling += 1
				if num_blocks_falling > 1:		#this shouldn't happen ever... but it does.
					data.objects.pop(i)
			if hasattr(obj,"dead") and obj.dead:
				if hasattr(obj, "RemoveFromBoard"):
					obj.RemoveFromBoard()
				data.objects.pop(i)
			
		if num_blocks_falling is 0 and data.game_over is False:
			game.GetNextBigBlock()
			game.MakeNewBigBlock()
			data.interface_objects['block queue'].UpdateQueueBlocks()
	
		for obj in data.objects:
			obj.Update()
	
def RenderObjects():
	global current_background
	ika.Video.Blit(current_background, 0, 0)
	
	if data.gains_control != []:
		data.gains_control[0].Render()
	else:
		for obj in data.interface_objects.values():
			obj.Render()
		for obj in data.objects:
			obj.Render() 
		
	
	
def MainLoop():
	last_update = 0
	
	while 1:
		if ika.GetTime() > last_update + 1:
			last_update = ika.GetTime()            

			global last_fps

			if last_fps != ika.GetFrameRate():
				ika.SetCaption( str("BlockHaus 0.9    FPS(" + str(last_fps) + ")"))
				last_fps = ika.GetFrameRate()

			ika.Input.Update()
			manager.ExecuteUpdateList()
			
			last_update = ika.GetTime()+1
			
		manager.ExecuteRenderList()

		ika.Video.ShowPage()
