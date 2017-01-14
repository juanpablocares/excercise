#!/usr/bin/python

import sys
#own module that do main tasks
import supermarket
import itertools
import collections

"""
	Main program
	
	Parameters
	----------
	fileName : string
		Name of the file to run the algorithm
	sigma : int
		minimum frequency to count a combination
	Returns
	-------
	file
		file with items size, frequency and combiations
	"""

class Node(object):
	def __init__(self, number):
		self.count = 0
		self.number = number
		#self.children_numbers = []
		self.children = []
		
	def add_child(self, obj):
		self.children.append(obj)
	
	def increase_count(self):
		self.count += 1
	
	def has_children(self, number):
		for i in range(len(self.children)):
			if number == self.children[i].number:
				return i
		return -1
	
	def add_combination(self, combination):
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
				#self.children_numbers.append(value)
				self.children[-1].add_combination(set(comb))
		else:
			if index >= 0:
				self.children[index].increase_count()
			else:
				new_value = Node(value)
				self.children.append(new_value)
				#self.children_numbers.append(value)
				self.children[-1].increase_count()

	def has_values(self):
		if len(self.children) > 0:
			return True
		return False
	
	def print_nodes(self, combination, file, sku, sigma):
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
		for child in self.children:
			combination = set()
			child.print_nodes(combination, file, sku, sigma)
		
fileName = sys.argv[1]
sigma    = int(sys.argv[2])

if supermarket.FileExist(fileName):
	#counts the frequencies of each combination
	allFrequentItems = {}
	#list of transactions (sets)
	transactions = []
	
	allSkus = set()
	file = open(fileName)
	all = set()

	algo = {}
	larger = 0
	for line in file:
		skus = supermarket.GetSkus(line.strip().split(' '))
		for s in skus:
			if s not in algo:
				algo[s] = 1
			else:
				algo[s] = algo[s] + 1
		all = all|skus
		if len(skus) != 0:
			transactions.append(skus)
			if len(skus) > larger:
				larger = len(skus)
	
	for sku, count in algo.items():
		if count < sigma:
			i = 0
			while i < len(transactions):
				if sku in transactions[i]:
					transactions[i].remove(int(sku))
					if len(transactions[i]) < sigma:
						del transactions[i]
					else:
						i = i + 1
				else:
					i = i + 1
	
	file = open(fileName.split('.')[0] + '.out', 'w')

	tmpTransaction = set()
	for i in range(len(transactions)):
		for j in range(len(transactions)):
			if len(transactions[i]) < len(transactions[j]):
				tmpTransaction = transactions[i]
				transactions[i] = transactions[j]
				transactions[j] = tmpTransaction

	for sku in all:
		#print sku
		for large in range(2, 3):
			arbol = Node(-1)
			for transaction in transactions:
				if sku in transaction:
					tmp = set(transaction)
					tmp.remove(sku)
					for it in itertools.combinations(tmp, large):
						local = set(it)
						#print str(sku) + ' ' + str(local)
						arbol.add_combination(local)
						local.clear()
					tmp.clear()
			#print arbol.children[0].children[1].count
			#print ''
			arbol.print_values(file, sku, sigma)

		for i in range(len(transactions)):
			if sku in transactions[i]:
				transactions[i].remove(sku)
	file.close()
else:
	supermarket.Exception(1)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	