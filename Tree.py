"""
Node class. This class is used to create a tree
of combinations to store efficiently each one
"""

class Node(object):

	def __init__(self, number):
		"""
		initializer

		Parameters
		----------
		number : int
			number to initiate this node
		"""
		self.count = 0
		self.number = number
		#self.children_numbers = []
		self.children = []

	
	def increase_count(self):
		"""
		increase count of this object
		"""
		self.count += 1
	

	def has_children(self, number):
		"""
		check if this object has the given children

		Parameters
		----------
		number : int
			value to compare
		Returns
		-------
		int
			return the index of the number given. In
			other case just return -1
		"""
		for i in range(len(self.children)):
			if number == self.children[i].number:
				return i
		return -1
	
	

	def find_combination(self, combination):
		"""
		find a given combination on the tree

		Parameters
		----------
		combination : set
			combination to find
		Returns
		-------
		bool
			return true if it exist on the tree,
			false other way
		"""
		comb = list(combination)
		comb.sort()
		
		if len(comb) == 0:
			return True
	
		for child in self.children:
			if child.number == comb[0]:
				comb.pop(0)
				return child.find_combination(comb)
		return False
	
	
	def insert_combination(self, combination, count):
		"""
		insert a given combination to the tree with
		its counter

		Parameters
		----------
		combination : set
			combination to insert
		count : int
			counter of the combination
		"""
		comb = list(combination)
		comb.sort()
		value = comb.pop(0)
		index = self.has_children(value)
		if len(comb) > 0:
			if index >= 0:
				self.children[index].insert_combination(set(comb), count)
			else:
				new_value = Node(value)
				self.children.append(new_value)
				#self.children_numbers.append(value)
				self.children[-1].insert_combination(set(comb), count)
		else:
			if index >= 0:
				self.children[index].count += count
			else:
				new_value = Node(value)
				self.children.append(new_value)
				self.children[-1].count = count
	
	

	def add_combination(self, combination):
		"""
		add a given combination to the tree. Additionaly if it already
		exist, it increase the counter

		Parameters
		----------
		combination : set
			combination to insert
		"""
		comb = list(combination)
		comb.sort()
		value = comb.pop(0)
		index = self.has_children(value)
		if len(comb) > 0:
			if index >= 0:
				self.children[index].add_combination(set(comb))
			else:
				new_value = Node(value)
				self.children.append(new_value)
				self.children[-1].add_combination(set(comb))
		else:
			if index >= 0:
				self.children[index].increase_count()
			else:
				new_value = Node(value)
				self.children.append(new_value)
				self.children[-1].increase_count()
				self.children[-1].increase_count()

				
	
	def has_values(self):
		"""
		check if the node has childrens
		"""
		if len(self.children) > 0:
			return True
		return False
	

	def print_nodes(self, combination, file, sku, sigma):
		"""
		print the tree to the given file reference

		Parameters
		----------
		combination : set
			combination to use in each level
		file : input file
			file reference to write
		sku : int
			sku added to each combination
		sigma : int
			minimum frequency to be written on the file
			
		"""
		comb = set(combination)
		comb.add(self.number)
		
		if self.count >= sigma:
			line = str(len(comb) + 1) + ', '
			line += str(self.count) + ', '
			line += str(sku) + ', '
			listComb = list(comb)
			for i in range(len(listComb) - 1):
				line += str(listComb[i]) + ', '
			line += str(listComb[-1])
			file.write(line + '\n')
		
		if len(self.children) > 0:
			for child in self.children:
				child.print_nodes(comb, file, sku, sigma)
	
	def print_values(self, file, sku, sigma):
		"""
		entry point to print into the file

		Parameters
		----------
		file : input file
			file reference to write
		sku : int
			sku added to each combination
		sigma : int
			minimum frequency to be written on the file
			
		"""
		for child in self.children:
			combination = set()
			child.print_nodes(combination, file, sku, sigma)

	def create_combinations(self, other, combination):
		"""
		create combinations to be use in append

		Parameters
		----------
		other : Node
			other Node tree to be inserted on self
		combination : set
			combination to create in each level			
		"""
		if other.count > 0:
			#if count > 0 the algorithm is in a combination
			#so it has to insert it into self
			self.insert_combination(combination, other.count)
		#iterate in childrens of the other Node and call itself
		for child in other.children:
			comb = set(combination)
			comb.add(child.number)
			self.create_combinations(child, comb)
	
	def append(self, other):
		"""
		append other Node tree into self

		Parameters
		----------
		other : Node
			other Node tree to be inserted on self		
		"""
		for child in other.children:
			#reset each combination to be created
			combination = set()
			self.create_combinations(other, combination)