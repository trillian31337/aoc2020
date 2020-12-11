import sys

def read_grid(f):
   grid = {}
   xmin = 0
   ymin = 0
   y = int(ymin)
   for line in f:
      row = list(line[:-1])
      x = int(xmin)
      for tile in row:
         grid[(x,y)] = tile
         x += 1
      y += 1
   xmax = len(row)
   ymax = y

   return grid,xmin,xmax,ymin,ymax

def print_grid(grid,xmin,xmax,ymin,ymax):
   #debug("print_grid: xmin %d,xmax %d,ymin %d,ymax %d" % (xmin,xmax,ymin,ymax))
   sys.stdout.write("     00000000001111111111222222222233333333333444444444\n")
   sys.stdout.write("     01234567890123456789012345678901234567890123456789\n")
   for y in range(ymin,ymax):
      sys.stdout.write("%3d: " % y),
      for x in range(xmin,xmax):
         pos = (x,y)
         sys.stdout.write("%s" % (grid[(x,y)])),
      sys.stdout.write("\n")
	
def count_adjacent(grid,pos):
	# 8 positions
	(x,y) = pos
	count = 0
	adjlist = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]
	for a in adjlist:
		if a in grid and grid[a] == '#':
			count += 1
	return count

def count_occupied(grid,xmin,xmax,ymin,ymax):
	count = 0
	for y in range(ymin,ymax):
		for x in range(xmin,xmax):
			pos = (x,y)
			if grid[pos] == '#':
				count += 1
	return count
	

def update_grid(grid,xmin,xmax,ymin,ymax):
	new_grid = grid.copy()
	for y in range(ymin,ymax):
		for x in range(xmin,xmax):
			pos = (x,y)
			if grid[pos] == '.':
				new_grid[pos] = '.'
			elif grid[pos] == 'L' and count_adjacent(grid,pos) == 0:
				new_grid[pos] = '#'
			elif grid[pos] == '#' and count_adjacent(grid,pos) >= 4:
				new_grid[pos] = 'L'
	return new_grid
	

##### main #######
#inputfile = 'input_test'
inputfile = 'input'
f = open(inputfile, 'r')
grid,xmin,xmax,ymin,ymax = read_grid(f)
print_grid(grid,xmin,xmax,ymin,ymax)

old_grid = grid.copy()
while(True):
	grid = update_grid(grid,xmin,xmax,ymin,ymax)
	print_grid(grid,xmin,xmax,ymin,ymax)
	if grid == old_grid:
		break
	old_grid = grid.copy()

# count occupied seats
print("Number of occupied seats: " + str(count_occupied(grid,xmin,xmax,ymin,ymax)))
