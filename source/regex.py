import re

#for square (3x3)
top_left = re.compile('\[\[1, 1, .\], \[1, 1, .\], \[., ., .\]\]')
top_right = re.compile('\[\[., 1, 1\], \[., 1, 1\], \[., ., .\]\]')
bottom_left = re.compile('\[\[., ., .\], \[1, 1, .\], \[1, 1, .\]\]')
bottom_right = re.compile('\[\[., ., .\], \[., 1, 1\], \[., 1, 1\]\]')

#for line up/down
a = re.compile('\[1, 1, 1, 1, ., ., .\]')
b = re.compile('\[., 1, 1, 1, 1, ., .\]')
c = re.compile('\[., ., 1, 1, 1, 1, .\]')
d = re.compile('\[., ., ., 1, 1, 1, 1\]')

def CheckForSquare(list):
	str_list = str(list)
	square_at = []
	if top_left.match(str_list):
		square_at.append('top_left')
	if top_right.match(str_list):
		square_at.append('top_right')
	if bottom_left.match(str_list):
		square_at.append('bottom_left')
	if bottom_right.match(str_list):
		square_at.append('bottom_right')
	return square_at
	
def CheckForLine(list):
	str_list = str(list)
	line_at = []
	if a.match(str_list):
		line_at.append('a')
	if b.match(str_list):
		line_at.append('b')
	if c.match(str_list):
		line_at.append('c')
	if d.match(str_list):
		line_at.append('d')
	return line_at