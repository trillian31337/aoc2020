import sys
import numpy as np
import copy

def create_grid(f):
	grid = []
	plane = []
	for line in f:
		plane.append(list(line.rstrip()))
	grid.append(plane)
	return np.array(grid)

def print_grid(grid):
	for z in range(len(grid)):	
		for y in range(len(grid[0])):
			for x in range(len(grid[0][0])):
				sys.stdout.write(grid[z][y][x])
				sys.stdout.write(" ")
			sys.stdout.write('\n')
		sys.stdout.write('\n')

def expand_grid(grid):
	# add an empty z plane first and last

	plane = np.array([[['.']*len(grid[0][0])]*len(grid[0])])
	grid = np.vstack((plane,grid))
	grid = np.vstack((grid,plane))

	# add row first and last in each plane
	row = np.array([[['.']*len(grid[0][0])]]*len(grid))
	grid = np.hstack((row,grid))
	grid = np.hstack((grid,row))

	# add column first and last in each plane
	column = np.array([[['.']]*len(grid[0])]*len(grid))
	grid = np.dstack((column,grid))
	grid = np.dstack((grid,column))

	return grid

def count_active_neighbours(coord,grid):
	# check pixels in 3d cube with sides 3 x 3
	# exclude the pixel itself from the count
	z_offset = coord[0]
	y_offset = coord[1]
	x_offset = coord[2]	
	count = 0
	for z in range(z_offset-1,z_offset+2):
		if (z < 0 or z >= len(grid)):
			continue
		for y in range(y_offset-1,y_offset+2):
			if (y < 0 or y >= len(grid[0])):
				continue
			for x in range(x_offset-1,x_offset+2):
				if (x < 0 or x >= len(grid[0][0])):
					continue
				if x == x_offset and y == y_offset and z == z_offset:
					continue
				if grid[z][y][x] == '#':
					count += 1
	return count

def count_all_active(grid):
	count = 0
	for z in range(len(grid)):
		for y in range(len(grid[0])):
			for x in range(len(grid[0][0])):
				if grid[z][y][x] == '#':
					count += 1
	return count

def cycle(grid):
	grid = expand_grid(grid)
	newgrid = copy.deepcopy(grid)
	#print_grid(newgrid)
	
	for z in range(len(grid)):
		for y in range(len(grid[0])):
			for x in range(len(grid[0][0])):
				count = count_active_neighbours((z,y,x),grid)
				if (grid[z][y][x] == '.' and count == 3):
					newgrid[z][y][x] = '#'
				elif (grid[z][y][x] == '#' and (count != 2 and count != 3)):
					newgrid[z][y][x] = '.'

	return newgrid


######## main ########
infile = 'input'
#infile = 'input_test'
f = open(infile,'r')

grid = create_grid(f)
print("Initial state:")
print_grid(grid)

for i in range(6):
	grid = cycle(grid)
	print("After cycle {}:".format(i+1))
	print_grid(grid)
	# count active
	count = count_all_active(grid)
	print("Number of active pixels after round {}: {}".format(i+1,count))

