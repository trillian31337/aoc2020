import numpy as np
import re
import sys
import copy
import itertools

def read_tiles(f):
	tiles = {}
	current_tile = -1
	row = 0
	tile = []
	for line in f:
		if line.rstrip() == "":
			# new tile coming in next line
			tiles[int(current_tile)] = np.array(tile)
			continue
		elif re.match(r'^Tile',line.rstrip()) != None: 
			m = re.match(r'Tile (\d+)',line.rstrip())
			current_tile = m.group(1)
			tile = []
			row = 0
		else:
			tile.append(list(line.rstrip()))
			row += 1
	# add last tile
	tiles[int(current_tile)] = np.array(tile)
	return tiles

def print_tile(tile):
	for y in range(10):
		for x in range(10):
			sys.stdout.write(tile[y][x])
		sys.stdout.write('\n')
	sys.stdout.write('\n')				

def print_grid(grid):
	# set to one to print picture with tile spaces
	with_spaces = 0
	for y in range(dim*8):
		if with_spaces and y % 8 == 0:
			sys.stdout.write('\n') 
		for x in range(dim*8):
			if with_spaces and x % 8 == 0:
				sys.stdout.write("  ")
			sys.stdout.write(grid[y][x])
			sys.stdout.write(" ")
		sys.stdout.write('\n')


def flip_tile(tile,dim):
	if dim == 'x':
		return np.flip(tile,1)
	elif dim == 'y':
		return np.flip(tile,0)
	else:
		print("Error in flip: wrong dimension {}".format(dim))

def rotate_tile(tile,steps):
	# rotate steps (counter clockwise)
	rot_tile = np.rot90(tile,steps)
	return rot_tile


def check_border(tile1,tile2,dim):
	if dim == 'x':
		# tile2 is to the right of tile1	
		for y in range(10):
			if tile1[y][-1] != tile2[y][0]:
				return False
		return True
	if dim == 'y':
		# tile2 is beneath tile2
		for x in range(10):
			if tile1[-1][x] != tile2[0][x]:
				return False
		return True


def get_variants(tile):
	# get all unique variants of rot/flip of tile
	tile_poslist = []
	tile_poslist.append(tile) 	
	tile_poslist.append(flip_tile(tile,'x')) 	
	tile_poslist.append(rotate_tile(tile,1))
	tile_poslist.append(flip_tile(rotate_tile(tile,1),'x')) 	
	tile_poslist.append(rotate_tile(tile,2))
	tile_poslist.append(flip_tile(rotate_tile(tile,2),'x')) 	
	tile_poslist.append(rotate_tile(tile,3))
	tile_poslist.append(flip_tile(rotate_tile(tile,3),'x')) 	

	return tile_poslist

def check_order(dim,current, order, tiles, fixed_tiles):
	# check if finished - fixed tiles array is filled
	if len(fixed_tiles) == len(tiles):
		# finished 
		return True,fixed_tiles
	
	tile = tiles[order[current]]
	max_pos = dim*dim
	possible_pos = []
	(x,y) = (current % dim,int(current/dim))
	# find fixed tiles with borders to current tile
	# translate current to x and y pos
	# left and above
	(x_left,y_left) = (x-1,y)
	if x_left == -1:
		left = max_pos
	else:
		left = y_left*dim+x_left
	(x_above,y_above) = (x,y-1)
	if y_above == -1:
		above = max_pos
	else:
		above = y_above*dim+x_above

	for pos in get_variants(tile):
		# check borders to tiles to the left and above
		result = True
		if len(fixed_tiles) > left:
			left_tile = fixed_tiles[left]
			result = check_border(left_tile,pos,'x')
		if result and (len(fixed_tiles) > above):
			above_tile = fixed_tiles[above]
			result = check_border(above_tile,pos,'y')
		if result:
			# position is valid
			possible_pos.append(pos)
	# if no possible positions
	if len(possible_pos) == 0:	
		return False, fixed_tiles
				
	current += 1
	possible_tile = False
	# recursively check each possible position
	for pos in possible_pos:
		new_fixed_tiles = copy.deepcopy(fixed_tiles)
		new_fixed_tiles.append(pos)
		result,res_fixed_tiles = check_order(dim,current,order,tiles,new_fixed_tiles)
		possible_tile = possible_tile or result
		if result == True:
			return True,res_fixed_tiles
	# if we get here, we did not have any possible positions, return false
	return False, fixed_tiles

# brute force solver - does not check for matching edges
# works for 9 tiles but not for 144 tiles
def find_arrangement(tiles):
	# test with fixed order first
	#tile_order = [1951,2311,3079,2729,1427,2473,2971,1489,1171]	
	# get all permutations of the tiles
	for tile_order in itertools.permutations(tiles.keys()):
		#print("Testing tile order: {}".format(tile_order))
		current = 0
		result,fixed_tiles = check_order(current,tile_order,tiles,[])
		#print("Result: {} for tile order:\n{}".format(result,tile_order))
		if result == True:
			print("Result: {} for tile order:\n{}".format(result,tile_order))
			for fixed in fixed_tiles:
				print_tile(fixed)
			break	
	return tile_order

def get_edges(tile):
	edges = []
	for e in range(4):
		# get top edge
		top_row = tuple(tile[0])
		edges.append(top_row) 
		edges.append(top_row[::-1])
		tile = rotate_tile(tile,1)
	return edges	

def find_unique_edges(tiles):
	edges = {}
	for tile_id in tiles:
		tile = tiles[tile_id]
		tile_edges = get_edges(tile)
		for edge in tile_edges:
			if edge in edges:
				edges[edge].append(tile_id)
			else:
				edges[edge] = [tile_id]
	return edges

def find_corner_pieces(tiles, edges):
	# find pieces with two unique edges
	corner_pieces = []
	for tile_id in tiles:
		tile = tiles[tile_id]
		tile_edges = get_edges(tile)
		count_unique = 0
		for edge in tile_edges:
			if len(edges[edge]) == 1:
				count_unique += 1
		#print("Tile {} has {} unique edges".format(tile_id,count_unique))
		if count_unique == 4:
			corner_pieces.append(tile_id)
	return corner_pieces

def find_matching_tile(pos,puzzle_order,tiles):
	tile_edges = get_edges(tiles[puzzle_order[pos]])
	# find matching tiles
	matching_tiles = set()
	for edge in tile_edges:
		for tile_id in edges[edge]:
			matching_tiles.add(tile_id)
	matching_tiles.remove(puzzle_order[pos])
	return matching_tiles	

def check_edge_piece(tile_id,tiles,edges):
	tile_edges = get_edges(tiles[tile_id])
	count_unique = 0
	for edge in tile_edges:
		if len(edges[edge]) == 1:
			count_unique += 1
	if count_unique == 2 or count_unique == 4:
		return True
	else:
		return False	


def do_puzzle(dim,tiles,corner_pieces):
	edges = find_unique_edges(tiles)
	corner_pieces = find_corner_pieces(tiles, edges)
	# start with one corner piece
	# for each position after corner: find piece with maching edge
   # - need data structure: edges[edge] = tile_id
	# call check_order() on the list of pieces to get correct puzzle
	puzzle_order = []
	tile = corner_pieces[0]
	#print("first corner piece: {}".format(tile))
	puzzle_order.append(tile)
	for pos in range(1,len(tiles)):
		#print("pos: {}".format(pos))
		#print("puzzle_order: {}".format(puzzle_order))
		# get coordinates for current position
		x = pos % dim
		y = int(pos / dim)
		#print("pos: ({},{})".format(x,y))
		# get coordinates for tile to the left and tile above
		x_left = x-1
		y_left = y
		if x_left == -1:
			pos_left = -1
		else:
			pos_left = y_left*dim+x_left
		x_above = x
		y_above = y-1
		if y_above == -1:
			pos_above = -1
		else:
			pos_above = y_above*dim+x_above
		edge_piece_left = 0
		edge_piece_above = 0
		# get matching tiles for tile to the left and above
		#print("pos_left: {}".format(pos_left))
		if (-1 < pos_left) and (pos_left < len(puzzle_order)):
			matching_tiles_left = find_matching_tile(pos_left,puzzle_order,tiles)
		else:
			edge_piece_left = 1
		#print("pos_above: {}".format(pos_above))
		if (-1 < pos_above) and (pos_above < len(puzzle_order)):
			matching_tiles_above = find_matching_tile(pos_above,puzzle_order,tiles)
		else:
			edge_piece_above = 1
		if edge_piece_left:
			matching_tiles = matching_tiles_above
		elif edge_piece_above:
			matching_tiles = matching_tiles_left
		else:
			matching_tiles = matching_tiles_left.intersection(matching_tiles_above)
		# remove tiles already in puzzle_order
		matching_tiles -= set(puzzle_order)
		if edge_piece_left or edge_piece_above:
			# throw away matching tiles which are not edge pieces
			not_edge = set()
			for tile_id in matching_tiles:
				if not check_edge_piece(tile_id,tiles,edges):
					not_edge.add(tile_id)
			matching_tiles -= not_edge
		
		#print("matching tiles after checking if edge piece: {}".format(matching_tiles))
		# can be more than one matching tile, select one
		puzzle_order.append(list(matching_tiles)[0])
	print("puzzle order:",str(puzzle_order))
	
	# debug - test puzzle order to get same picture as in example:
	#puzzle_order = [1951,2311,3079,2729,1427,2473,2971,1489,1171]

	# set correct positions for all tiles	
	current = 0
	result,fixed_tiles = check_order(dim,current,puzzle_order,tiles,[])
	if result == False:
		print("do_puzzle: Error. Order did not work.")
	return fixed_tiles

def assemble_picture(dim,assembled_tiles):
	# initialize grid of correct size
	grid = ['.']*dim*8
	for y in range(dim*8):
		grid[y] = ['.']*dim*8
	for i in range(len(assembled_tiles)):
		# determine which pixels to set for current tile - x and y offset
		tile = assembled_tiles[i]
		x_offset = (i % dim)*8
		y_offset = int(i/dim)*8
		for y in range(8):
			for x in range(8):
				# set pixel
				grid[y+y_offset][x+x_offset] = tile[y+1][x+1]
	return grid

def check_for_seamonster(grid,seamonster):
	seamonster_positions = []
	for y in range(dim*8-3):
		for x in range(dim*8-20):
			#print("testing position: ({},{})".format(x,y))	
			result = True
			for s_y in range(3):
				for s_x in range(20):	
					if seamonster[s_y][s_x] == '#' and grid[y+s_y][x+s_x] == '.':
						result = False
						break
				if result == False:
					break
			if result == True:
				seamonster_positions.append((x,y))
	# mark seamonster in grid
	for s in seamonster_positions:
		(x_offset,y_offset) = s
		for s_y in range(3):
			for s_x in range(20):
				if seamonster[s_y][s_x] == '#':
					grid[y_offset+s_y][x_offset+s_x] = 'o'	

	return grid,seamonster_positions


def count_waves(grid):
	count = 0
	for y in range(dim*8):
		for x in range(dim*8):
			if grid[y][x] == '#':
				count += 1
	return count

##### main ######

infile = 'input'
#infile = 'input_test'
outfile = 'output'
f = open(infile,'r')
fout = open(outfile,'w')
tiles = read_tiles(f)

print("Number of tiles:")
print(len(tiles))
if len(tiles) == 144:
	dim = 12
else:
	dim = 3

edges = find_unique_edges(tiles)
#print("Number of unique edges: ",str(len(edges)))
#for edge in edges:
#	print("tiles: {} for edge {}".format(edges[edge],edge))
# seems that all edges are only one or two of
corner_pieces = find_corner_pieces(tiles, edges)
print("corner_pieces: {}".format(corner_pieces))

product = corner_pieces[0] * corner_pieces[1] * corner_pieces[2] * corner_pieces[3]

print("The product of the corner pieces ID's is: ",str(product))

assembled_tiles = do_puzzle(dim,tiles,corner_pieces)

#for tile in assembled_tiles:
#	print_tile(tile)

grid = assemble_picture(dim,assembled_tiles)
print("Assembled picture:")
print_grid(grid)

# seamonster size: 20 x 3
seamonster = []
seamonster.append(list("                  # "))
seamonster.append(list("#    ##    ##    ###"))
seamonster.append(list(" #  #  #  #  #  #   "))

seamonsters = []

grids = get_variants(grid)

print("")
print("Searching for sea monsters...")
for grid in grids:
	grid,seamonster_positions = check_for_seamonster(grid,seamonster)
	# print grid with seamonster
	if len(seamonster_positions) > 0:
		print("sea monster positions: {}".format(seamonster_positions))
		print_grid(grid)
		break

# count non-seamonster waves
roughness = count_waves(grid)
print("roughness = {}".format(roughness))
