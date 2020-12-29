import sys
import numpy as np
import copy

def create_grid(f):
	grid = []
	cube = []
	plane = []
	for line in f:
		plane.append(list(line.rstrip()))
	cube.append(plane)
	grid.append(cube)
	return np.array(grid)

def print_grid(grid):
	for w in range(len(grid)):	
		for z in range(len(grid[0])):
			print("w = {}, z = {}".format(w,z))
			for y in range(len(grid[0][0])):
				for x in range(len(grid[0][0][0])):
					sys.stdout.write(grid[w][z][y][x])
					sys.stdout.write(" ")
				sys.stdout.write('\n')
			sys.stdout.write('\n')
		sys.stdout.write('\n')

def expand_grid(grid):

	print("expand_grid: dimensions: {},{},{},{}".format(len(grid),len(grid[0]),len(grid[0][0]),len(grid[0][0][0])))

	# add column first and last in each plane (x axis)
	hyper_column = np.reshape(np.array(['.']*len(grid[0][0])*len(grid[0])*len(grid)),(len(grid),len(grid[0]),len(grid[0][0]),1))
	grid = np.concatenate((hyper_column,grid,hyper_column),axis=3)
	
	# add row first and last in each plane (y axis)
	hyper_row = np.reshape(np.array(['.']*len(grid[0][0][0])*len(grid[0])*len(grid)),(len(grid),len(grid[0]),1,len(grid[0][0][0])))
	grid = np.concatenate((hyper_row,grid,hyper_row),axis=2)

	# add an empty plane first and last in cube (z axis)
	hyper_plane = np.reshape(np.array(['.']*len(grid[0][0][0])*len(grid[0][0])*len(grid)),(len(grid),1,len(grid[0][0]),len(grid[0][0][0])))
	grid = np.concatenate((hyper_plane,grid,hyper_plane),axis=1)

	# add an empty cube first and last in hypercube (w axis)
	hyper_cube = np.reshape(np.array(['.']*len(grid[0][0][0])*len(grid[0][0])*len(grid[0])),(1,len(grid[0]),len(grid[0][0]),len(grid[0][0][0]))) 
	grid = np.concatenate((hyper_cube,grid,hyper_cube),axis=0)

	return grid

def count_active_neighbours(coord,grid):
	# check pixels in 3d cube with sides 3 x 3
	# exclude the pixel itself from the count
	w_offset = coord[0]
	z_offset = coord[1]
	y_offset = coord[2]	
	x_offset = coord[3]	
	count = 0
	for w in range(w_offset-1,w_offset+2):
		if (w < 0 or w >= len(grid)):
			continue
		for z in range(z_offset-1,z_offset+2):
			if (z < 0 or z >= len(grid[0])):
				continue
			for y in range(y_offset-1,y_offset+2):
				if (y < 0 or y >= len(grid[0][0])):
					continue
				for x in range(x_offset-1,x_offset+2):
					if (x < 0 or x >= len(grid[0][0][0])):
						continue
					if x == x_offset and y == y_offset and z == z_offset and w == w_offset:
						continue
					if grid[w][z][y][x] == '#':
						count += 1
	return count

def count_all_active(grid):
	count = 0
	for w in range(len(grid)):
		for z in range(len(grid[0])):
			for y in range(len(grid[0][0])):
				for x in range(len(grid[0][0][0])):
					if grid[w][z][y][x] == '#':
						count += 1
	return count

def cycle(grid):
	grid = expand_grid(grid)
	newgrid = copy.deepcopy(grid)
	
	for w in range(len(grid)):
		for z in range(len(grid[0])):
			for y in range(len(grid[0][0])):
				for x in range(len(grid[0][0][0])):
					count = count_active_neighbours((w,z,y,x),grid)
					#print("coordinate ({},{},{}): {} active neighbours".format(z,y,x,count))
					if (grid[w][z][y][x] == '.' and count == 3):
						newgrid[w][z][y][x] = '#'
					elif (grid[w][z][y][x] == '#' and (count != 2 and count != 3)):
						newgrid[w][z][y][x] = '.'

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

