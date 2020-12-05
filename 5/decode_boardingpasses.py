import re

def decode(space,data):
	dlist = list(data)	
	
	if len(dlist) == 1:
		if dlist[0] == 'L' or dlist[0] == 'F':
			return space[0]
		else:
			return space[1]
	else:
		if dlist[0] == 'L' or dlist[0] == 'F':
			lo = space[0]
			hi = space[0] + int((space[1] - space[0]) / 2)
		else:
			lo = space[0] + int((space[1] - space[0] + 1) / 2)
			hi = space[1]
		dlist.pop(0)

		return decode((lo,hi),dlist)


### main ###
#infile = 'input_test'
infile = 'input'
f = open(infile,'r')

count_valid = 0
row = 0
col = 0
highest_seatID = 0
for line in f:
	pattern = re.compile("([FB]{7})([RL]{3})")
	m = pattern.match(line)
	print(line.rstrip())
	if m == None:
		print("Error parsing input row")
		exit(1)
	row = m.group(1)
	col = m.group(2)
	print(row)
	print(col)
	row_decoded = decode((0,127),list(row))	
	print("Decoded row: " + str(row_decoded))
	col_decoded = decode((0,7),list(col))	
	print("Decoded column: " + str(col_decoded))
	if (row_decoded * 8 + col_decoded) > highest_seatID:
		highest_seatID = row_decoded * 8 + col_decoded

print("Highest seat ID: " + str(highest_seatID))
