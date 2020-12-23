import sys

# Ring data structure
# - current pointer points at current element
# - move only current pointer 
# operations needed:
# pop elements (after current)
# insert elements (at random point
# next
# find element


class Ring:
	def __init__(self, l):
		if not len(l):
			raise "ring must have at least one element"
		self._data = l
		self.current = 0

	def __repr__(self):
		return repr(self._data)

	def __len__(self):
		return len(self._data)

	def __getitem__(self, i):
		return self._data[i]

	def get_current_index(self):
		return self.current

	def __get_next_index(self,index):
		if index+1 >= len(self._data):
			next_index = 0
		else:
			next_index = index+1
		return next_index

	def __find_element(self,element):
		return self._data.index(element)

	def get_current(self):
		return self._data[r.current]

	# move current pointer
	def step(self):
		index = self.__get_next_index(self.current)
		self.current = index
		# can remove return here when finished debugging
		return self.current

	def pop_after_current(self):
		index = self.__get_next_index(self.current)
		elem = self._data.pop(index)
		if index < r.current:
			r.current -= 1
		return elem

	# insert element at (after) element with a certain value
	# expensive operation for long lists?
	def insert_after(self,elem,at):
		index = self.__find_element(at)
		index += 1
		self._data.insert(index,elem)
		if self.current >= index:
			self.current += 1
	
	# find a smaller element (-1 from element value if it exists)
	# expensive operation for long list?
	def find_smaller(self,element):
		sortedlist = sorted(self._data)
		#print("sortedlist: {}".format(sortedlist))
		index = sortedlist.index(element)
		#print("index: {}".format(index))
		smaller_index = index-1 
		if smaller_index < 0: 
			smaller_index = len(sortedlist)-1
		#print(smaller_index)
		smaller = sortedlist[smaller_index]	
		return smaller

	def print_ring(self):
		output = "cups: "
		for e in self._data:
			if self._data[self.current] == e:
				output += '({}),'.format(e)
			else:
				output += '{},'.format(e)
		output = output[:-1]
		print(output)

	def get_after_1_list(self):
		output = []
		index = self.__find_element(1)
		for i in range(len(self._data)-1):
			index = self.__get_next_index(index)
			output.append(self._data[index])
		return output

def move(r):
	r.print_ring()
	# pick up three cups
	cup1 = r.pop_after_current() 
	cup2 = r.pop_after_current()
	cup3 = r.pop_after_current()
	print("pick up: {} {} {}".format(cup1,cup2,cup3))
	#print("current: {}".format(r.get_current()))
	#r.print_ring()
	# place them after element with current cup value-1	
	smaller = r.find_smaller(r.get_current())
	print("destination: {}".format(smaller))
	r.insert_after(cup1,smaller)
	r.insert_after(cup2,cup1)
	r.insert_after(cup3,cup2)
	
	#r.print_ring()

	# move current cup to next
	r.step()
	#print("after step: ",str(r.get_current()))

	return r

######## main #########
inputfile = 'input'
#inputfile = 'input_test'
f = open(inputfile,'r')
l = list(map(int,f.readline().rstrip()))
print(l)
r = Ring(l)
print(r.current)
r.print_ring()

for i in range(100):
	print("-- move {} --".format(i+1))
	r = move(r)

output = r.get_after_1_list()
print("Elements in order after element with value '1':")
for e in output:
	sys.stdout.write(str(e))
sys.stdout.write('\n')
