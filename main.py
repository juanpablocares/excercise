#!/usr/bin/python

import sys
#own module that do main tasks
import supermarket
import itertools
import collections
import Tree

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
	intersections = list()
	for i in range(len(transactions)):
		intersections.append(set())
		#for j in range(len(transactions)):
			#if len(transactions[i]) < len(transactions[j]):
				#tmpTransaction = transactions[i]
				#transactions[i] = transactions[j]
				#transactions[j] = tmpTransaction
	
	for i in range(len(transactions)):
		intersections[i].add(i)
		for j in range(i + 1, len(transactions)):
			if len(transactions[i] & transactions[j]) >= 3:
				#print str(i) + ' ' + str(j)
				intersections[i].add(j)
	
	list_transactions = list(range(0, len(transactions)))
	
	general_tree = Tree.Node(-1)

	for i in intersections:
		min = list(set(i))
		min.sort()
		value = min.pop(0)
		for it in itertools.combinations(min, sigma - 1):
			intersection = transactions[value]
			for t in it:
				if len(intersection) >= 3:
					intersection = intersection & set(transactions[t])
				else:
					break
			if len(intersection) >= 3:
				for large in range(3, len(intersection) + 1):
					for inter in itertools.combinations(intersection, large):
						values = set()
						values.add(value)
						values = values | set(it)
						general_tree.add_combination(set(inter), values)
	general_tree.print_values(file, sigma)
	file.close()
	
else:
	supermarket.Exception(1)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	