import numpy as np

def print_grid(grid):
	# find min and max for x and y
	for coord in grid:
		print("{}: {}".format(coord,grid[coord]))

def move(flipcount,grid,path):
	directions = {'e':(1,0),'w':(-1,0),'se':(1,1),'ne':(0,-1),'sw':(0,1),'nw':(-1,-1)}	
	coord = (0,0)
	for instr in path:
		coord = tuple(np.add(np.array(coord),np.array(directions[instr])))
		print(instr,coord)
	# debug
	print_grid(grid)
	prev_colour = 'white'
	if (coord in grid) and (grid[coord] == 'black'):
		prev_colour = 'black'
		grid[coord] = 'white'
		print("##########Does this ever happen??")
	else:
		prev_colour = 'white'
		grid[coord] = 'black'
	if coord in flipcount:
		flipcount[coord] += 1
	else:
		flipcount[coord] = 1
	print("flipping coord {} from {} to {}".format(coord,prev_colour,grid[coord]))
	return flipcount,grid

def parse_direction(path):
	tile_dir = []
	i = 0
	while i < len(path):
		if path[i] in ['e','w']:
			tile_dir.append(path[i])
			i += 1
		else:
			tile_dir.append(path[i:i+2])
			i += 2
	return tile_dir

###### main ######

infile = 'input'
#infile = 'input_test'
#infile = 'input_test2'
f = open(infile,'r')
paths = []
for line in f:
	paths.append(parse_direction(line.rstrip()))

grid = {}
flipcount = {}
for path in paths:
	flipcount,grid = move(flipcount,grid,path)
print_grid(grid)
#print(flipcount)
count_black = 0
for coord in grid:
	if grid[coord] == 'black':
		count_black += 1
print("{} tiles are black".format(count_black)) 

