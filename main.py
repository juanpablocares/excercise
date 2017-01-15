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
	for i in range(len(transactions)):
		for j in range(len(transactions)):
			if len(transactions[i]) < len(transactions[j]):
				tmpTransaction = transactions[i]
				transactions[i] = transactions[j]
				transactions[j] = tmpTransaction

	for sku in all:
		#print sku
		for large in reversed(range(2, larger)):
			general_tree = Tree.Node(-1)
			for i in range(len(transactions)):
				tmp_tree = Tree.Node(-1)
				if sku in transactions[i]:
					for j in range(i + 1, len(transactions)):
						if sku in transactions[j]:
							inter = transactions[i] & transactions[j]
							inter.remove(sku)
							for it in itertools.combinations(inter, large):
								local = set(it)
								if not general_tree.find_combination(local):
									tmp_tree.add_combination(local)
								local.clear()
					general_tree.append(tmp_tree)
			general_tree.print_values(file, sku, sigma)

		for i in range(len(transactions)):
			if sku in transactions[i]:
				transactions[i].remove(sku)
	file.close()
else:
	supermarket.Exception(1)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	