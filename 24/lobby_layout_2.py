import numpy as np
import copy

def print_grid(grid):
	# find min and max for x and y
	for coord in grid:
		print("{}: {}".format(coord,grid[coord]))

def move(flipcount,grid,path):
	directions = {'e':(1,0),'w':(-1,0),'se':(1,1),'ne':(0,-1),'sw':(0,1),'nw':(-1,-1)}	
	print("directions:")
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
	#print(tile_dir)
	return tile_dir

def add_neighbours(coord, grid):
	x_offset = coord[0]
	y_offset = coord[1]
	directions = {'e':(1,0),'w':(-1,0),'se':(1,1),'ne':(0,-1),'sw':(0,1),'nw':(-1,-1)}
	for d in directions:
		x = x_offset + directions[d][0]
		y = y_offset + directions[d][1]
		if (x,y) not in grid:
			grid[(x,y)] = 'white'
			#print("added coord: ({},{})".format(x,y))
	return grid

def count_black(coord,grid):
	x_offset = coord[0]
	y_offset = coord[1]
	directions = {'e':(1,0),'w':(-1,0),'se':(1,1),'ne':(0,-1),'sw':(0,1),'nw':(-1,-1)}
	count = 0
	for d in directions:
		x = x_offset + directions[d][0]
		y = y_offset + directions[d][1]
		if (x,y) in grid and grid[(x,y)] == 'black':
			count += 1
	return count

def change_pattern(grid):
	newgrid = copy.deepcopy(grid) 
	# for every black tile in grid
	# - get all neighbours
	# - add to grid
	for coord in grid:
		if grid[coord] == 'black':
			newgrid = add_neighbours(coord,newgrid)
	# for all coordinates in grid
	# - apply rules for flipping
	for coord in newgrid:
		# count black neighbours in old grid
		count = count_black(coord,grid)
		#print("count = {} for coord {}".format(count,coord))
		# set the coordinates properly in new grid
		if newgrid[coord] == 'black' and (count == 1 or count == 2):
			newgrid[coord] == 'black'
		if newgrid[coord] == 'black' and (count < 1 or count > 2):
			newgrid[coord] = 'white'
		elif newgrid[coord] == 'white' and count == 2: 
			newgrid[coord] = 'black'

	return newgrid

###### main ######

infile = 'input'
#infile = 'input_test'
#infile = 'input_test2'
f = open(infile,'r')
paths = []
for line in f:
	#print(line.rstrip())
	paths.append(parse_direction(line.rstrip()))

grid = {}
flipcount = {}
for path in paths:
	flipcount,grid = move(flipcount,grid,path)
print("initial grid:")
print_grid(grid)
#print(flipcount)
count_black = 0
for coord in grid:
	if grid[coord] == 'black':
		count_black += 1
print("{} tiles are black".format(count_black)) 

for i in range(100):
	grid = change_pattern(grid)
	count = 0
	#print("black tiles:")
	for c in grid:
		if grid[c] == 'black':
			#print(c)
			count += 1
	print("{} black tiles after {} days".format(count,i+1))
