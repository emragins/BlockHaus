
class Box:
	"A class that defines a rectangular region. Mainly used for collision."
	
	def __init__ (self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		
	def CollidesWithAt (self, box):
		x_hits = self.x + self.width >= box.x and self.x <= box.x + box.width
		y_hits = self.y + self.height >= box.y and self.y <= box.y + box.height
		
		if x_hits is False or y_hits is False:
			return 'none'
		if self.y + self.height >= box.y and self.y < box.y:
			if x_hits:
				return 'bottom'
		if x_hits and y_hits:
			return 'other'
		if self.x == box.x + box.width or box.x == self.x + self.width:
			return 'on edge'
		return 'none'
	
	def CollidesWithHollowAt(self, hollow):
		return hollow.CollidesWith(self)
		
	
class HollowBox(Box):
	def __init__(self, x, y, width, height):
		Box.__init__(self, x, y, width, height)
		self.left_edge = self.x
		self.right_edge = self.x + self.width
		self.top_edge = self.y
		self.bottom_edge = self.y + self.height
	
	##Warning, this WILL NOT test if it is actually on the line.
	##For that, I need to add restrictions to ends of edges
	def CollidesWith(self, box):
		#Returns a boolean evaluation of whether this box's *edges*
		#collides with the box object passed
		
		if (self.left_edge >= box.x
					and self.left_edge <= box.x + box.width):
			return 'left'
		elif (self.right_edge >= box.x
					and self.right_edge <= box.x + box.width):
			return 'right'
		elif (self.top_edge >= box.y
					and self.top_edge <= box.y + box.height):
			return 'top'
		elif (self.bottom_edge >= box.y
					and self.bottom_edge <= box.y + box.height):
			return 'bottom'
		return 'none'
'''
		
def CollidesWithHollowSides(box, hollow):
	if (hollow.left_edge >= box.x
				and hollow.left_edge <= box.x + box.width):
		return True
	elif (hollow.right_edge >= box.x
				and hollow.right_edge <= box.x + box.width):
		return True
	return False
	
def CollidesWithHollowBottom(solid, hollow):
	if (hollow.bottom_edge >= solid.y
				and hollow.bottom_edge <= solid.y + solid.height):
		return True
	return False
		
def DetectCollision (box1, box2):
	"Returns a boolean evaluation of whether two boxes collide"
	if (box1.x  + box1.width >= box2.x
		and box1.x <= box2.x + box2.width
		and box1.y + box1.height >= box2.y
		and box1.y <= box2.y + box2.height):
			return True
	return False
	
	
'''