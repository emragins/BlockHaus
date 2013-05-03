import ika
import copy
#note: these MUST be 2d arrays or else block building messes up

a = [[1,1,1],
	[1,0,0]]
	
b = [[1,1],
	[1,1]]
	
c = [[1,1,1,1]]
	
d = [[0,1,1],
	[1,1,0]]

e = [[0,1],
	[1,1]]
	
f = [[1,1,1]]

g = [[1,1,0],
	[0,1,1]]

h = [[1,0,0],
	[1,1,1]]

i = [[1,0],
	[1,1]]
	
possible_shapes = [a,b,c,d,e,f,g,h,i]

outline_sources = ["images\\a-outline.png",
		"images\\b-outline.png",
		"images\\c-outline.png",
		"images\\d-outline.png",
		"images\\e-outline.png",
		"images\\f-outline.png",
		"images\\g-outline.png",
		"images\\h-outline.png",
		"images\\i-outline.png"
		]

outlines = {}

def GetShape():
	global	 possible_shapes
	num = ika.Random(0,len(possible_shapes))
	shape = copy.deepcopy(possible_shapes[num])
	outline = ProcessOutline(outline_sources[num])
	return shape, outline
	
def ProcessOutline(outline):
	canvas = ika.Canvas(outline)
	outlines = []
	for i in range(canvas.width/64):
		canvas.Clip(i*64, 0, 64, 64)	#set region
		blank = ika.Canvas(64,64)
		canvas.Blit(blank,0,0)
		a = ika.Image(blank)
		outlines.append(a)
		canvas.Clip()		#reset to whole image
	
	return outlines
			