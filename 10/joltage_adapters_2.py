import networkx as nx
from networkx.algorithms.simple_paths import all_simple_paths
from itertools import tee


def pairwise(iterable):
	a,b = tee(iterable)
	next(b, None)
	return zip(a,b)

# count joltage differences in configuration where all adapters are used
# part 1 problem
def count_differences(sortedadapters):
	# count differences
	diff1_count = 0
	diff3_count = 0
	for current, next_ in pairwise(sortedadapters):
		diff = next_-current
		if diff == 1:
			diff1_count += 1
		elif diff == 3:
			diff3_count += 1
		else:
			print("diff is not 1 or 3: {}".format(diff))
	print("Number of differences of 1 joltage: {}".format(diff1_count))
	print("Number of differences of 3 joltage: {}".format(diff3_count))
	print("Product: {}".format(diff1_count*diff3_count))


# get differences and create interval data structure
def get_intervals(sortedadapters):
	intervals_ = [0]
	for current, next_ in pairwise(sortedadapters):
		diff = next_-current
		if diff == 3:
			intervals_.append(current)
			intervals_.append(next_)
	# create list of tuples for intervals which need to be tested
	intervals = {}
	for current, next_ in pairwise(intervals_):
		intervals[(current,next_)] = 0
	return intervals

def get_number_of_paths(intervals,adapters):
	for (start,stop) in intervals:
		# get adapters in interval
		interval_adapters = adapters[adapters.index(start):adapters.index(stop)+1]
		print("adapters for interval ({},{}): {}".format(start,stop,interval_adapters))
		# create graph
		# create graph with all possible connections
		G = nx.DiGraph()
		for a in interval_adapters:
			G.add_node(a)
			# find adapters with value a+1, a+2, a+3
			if a+1 in adapters:
				G.add_node(a+1)
				G.add_edge(a,(a+1),weight=1)
			if a+2 in adapters:
				G.add_node(a+2)
				G.add_edge(a,(a+2),weight=2)
			if a+3 in adapters:
				G.add_node(a+3)
				G.add_edge(a,(a+3),weight=3)	
		# calculate number of paths
		path_count = 0
		print("paths:")
		for path in all_simple_paths(G, start, stop):
			print (path)
			path_count += 1
		print("path count for interval ({},{}): {}".format(start,stop,path_count))
		intervals[(start,stop)] = path_count		
	return intervals


######### main ###########3
#infile = 'input_test_0'
#infile = 'input_test'
infile = 'input'
f = open(infile,'r')

adapters = []
for line in f:
	adapters.append(int(line.rstrip()))

# add 0 and highest+3 to list to get all differences
adapters.append(0)
max_adapter = max(adapters)+3
adapters.append(max_adapter)
print("Max adapter: {}".format(max_adapter))

# part 1 problem - count differences
print("Part 1 problem:")
count_differences(sorted(adapters))

# part 2 problem - count paths
# 1. get the intervals between adapters which have distance 3 -> only one possible path between these 
# 2. count possible paths for each interval
# 3. calculate the product of paths for each interval to get total number of possible paths
print()
print("Part 2 problem:")
intervals = get_intervals(sorted(adapters))

# get number of paths for each interval
intervals = get_number_of_paths(intervals,sorted(adapters))

# calculate number of possible paths
product = 1
for start,stop in intervals:
	if intervals[(start,stop)] != 0:
		product *= intervals[(start,stop)]
print("The number of paths is: {}".format(product))


