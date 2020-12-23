import sys

# linked list implementation of 
class Element:
	def __init__(self):
		self.prev = None
		self.next = None

class Ring:
	def __init__(self,length):
		self.current = 1
		self._elementlist = []
		# add an extra element which will have index 0 - but not used in list
		self._elementlist.append(Element())
		self._elementlist.append(Element())
		self._elementlist[1].prev = length
		self._elementlist[1].next = 2
		for i in range(2,length):
			self._elementlist.append(Element())
			self._elementlist[i].prev = i-1
			self._elementlist[i].next = i+1
		self._elementlist.append(Element())
		self._elementlist[-1].prev = length-1
		self._elementlist[-1].next = 1

	def __repr__(self):
		return repr(self._elementlist)

	def __len__(self):
		return len(self._elementlist)

	def __getitem__(self, i):
		return self._elementlist[i]

	def __get_next_index(self,index):
		if index == len(self._elementlist)-1:
			next_index = 0
		else:
			next_index = index + 1
		return next_index

	# move current pointer
	def step(self):
		self.current = self._elementlist[self.current].next

	def pop_after_current(self):
		# get prev elem
		prev_elem = self.current
		# get elem to pop
		pop = self._elementlist[self.current].next
		# get next elem after popped
		next_elem = self._elementlist[pop].next
		# relink prev elem
		self._elementlist[prev_elem].next = next_elem	
		# relink next elem
		self._elementlist[next_elem].prev = prev_elem
		# reset links for popped elem
		self._elementlist[pop].prev = None
		self._elementlist[pop].next = None
		return pop

	def pop_element(self,elem):
		# get prev elem
		prev_elem = self._elementlist[elem].prev
		# get next elem after popped
		next_elem = self._elementlist[elem].next
		# relink prev elem
		self._elementlist[prev_elem].next = next_elem	
		# relink next elem
		self._elementlist[next_elem].prev = prev_elem
		# reset links for popped elem
		self._elementlist[elem].prev = None
		self._elementlist[elem].next = None
		return elem
				
	# insert element at (after) element with a certain value
	def insert_after(self,elem,at):
		# get next element to be able to re-link them
		next_elem = self._elementlist[at].next
		# relink prev element to input elem
		self._elementlist[at].next = elem
		# relink next element to this
		self._elementlist[next_elem].prev = elem
		# link current elem
		self._elementlist[elem].prev = at
		self._elementlist[elem].next = next_elem
	
	# find a smaller element (-1 from element value if it exists)
	def find_smaller(self,element):
		smaller = -1
		for i in range(1,4):
			smaller = element-i
			if smaller <= 0:
				smaller = len(self._elementlist)-i
			if self._elementlist[smaller].next != None:
				break
		return smaller

	# print next <number> cups after current elem 
	def print_ring(self,number):
		output = "cups: "
		e = self.current
		output += '({}),'.format(e)
		for i in range(1,number):
			e = self._elementlist[e].next
			output += '{},'.format(e)
		output = output[:-1]
		print(output)

	def print_product(self):
		cup1 = self._elementlist[1].next
		cup2 = self._elementlist[cup1].next
		print("product of {} and {} is {}".format(cup1,cup2,cup1*cup2))


def move(r):
	# pick up three cups
	cup1 = r.pop_after_current() 
	cup2 = r.pop_after_current()
	cup3 = r.pop_after_current()
	# place them after element with current cup value-1	
	smaller = r.find_smaller(r.current)
	r.insert_after(cup1,smaller)
	r.insert_after(cup2,cup1)
	r.insert_after(cup3,cup2)
	# move current cup to next
	r.step()
	return r

def arrange_cups(l,num):
	r = Ring(num)
	r.current = l[0]
	prev = len(r)-1
	for e in l:
		r.pop_element(e)
		r.insert_after(e,prev)
		prev = e
	return r
	
######## main #########
inputfile = 'input'
f = open(inputfile,'r')
l = list(map(int,f.readline().rstrip()))
print(l)

# create data structure and add input list
r = arrange_cups(l,1000000)

for i in range(10000000):
	r = move(r)

# print product of the two elements after element with value 1
r.print_product()

