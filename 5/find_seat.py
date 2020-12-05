import re

# convert F,B,R,L to 0 and 1
# sort input numerically
# find the missing number(s)

def convert(data):
	dlist = []
	for c in data:
		if c == 'F' or c == 'L':
			dlist.append(0)
		else:
			dlist.append(1)
	# binary list to integer conversion
	result = 0
	for d in dlist:
		result = (result << 1) | d
	#print(dlist)		
	#print(result)		
	return result

def find_missing(sorted_boarding_passes):
	missing = []
	#prev = -1
	prev = sorted_boarding_passes[0]
	for b in sorted_boarding_passes:
		if b-prev > 1:
			missing.extend(list(range(prev+1,b)))
		prev = b
	return missing


### main ###
#infile = 'input_test'
infile = 'input'
f = open(infile,'r')

boarding_list = []
for line in f:
	boarding_list.append(convert(line.rstrip()))
#print(sorted(boarding_list))
missing = find_missing(sorted(boarding_list))
print("The missing seats are:")
print(missing)

