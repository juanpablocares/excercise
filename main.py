#!/usr/bin/python

import sys
#own module that do main tasks
import supermarket
import itertools
import collections
import Tree
import operator

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
size_group = 3

if supermarket.FileExist(fileName):
	#counts the frequencies of each combination
	allFrequentItems = {}
	#list of transactions (sets)
	transactions = []
	
	file = open(fileName)
	set_sku = set()
	skus_counter = {}
	
	#read file
	for line in file:
		skus = supermarket.get_skus(line.strip().split(' '), size_group)
		
		for s in skus:
			if s not in skus_counter:
				skus_counter[s] = 1
			else:
				skus_counter[s] = skus_counter[s] + 1

		set_sku = set_sku | skus
		if len(skus) != 0:
			transactions.append(skus)
	
	transactions = supermarket.reduce_transactions_using_sigma(transactions, skus_counter, sigma)
	skus_order = sorted(skus_counter, key=skus_counter.__getitem__, reverse=True)

	#open write file
	file = open(fileName.split('.')[0] + '.out', 'w')
	
	#generate all possible combinations that contain each
	#SKU in order to reduce the search space
	for sku in skus_order:
		#create a local lista where sku exist
		sku_list = list()
		for i in range(len(transactions)):
			if sku in transactions[i]:
				sku_list.append(i)
		sku_list.sort()
		#at least the length of transaction that contain this
		#SKU has to be sigma, other way it does not respect
		#the minimum support level
		if len(sku_list) >= sigma:
			general_tree = Tree.Node(-1)
			intersection = set()
			for index_1 in range(len(sku_list)):
				i = sku_list[index_1]
				prev_intersection = set(transactions[i])
				for index_2 in range(index_1 + 1, len(sku_list)):
					j = sku_list[index_2]
					intersection = set(transactions[j]) & prev_intersection
				
					if len(intersection) >= size_group:
						size_intersection = len(intersection)
						intersection.remove(sku)
						for sku_combination_size in range(size_group - 1, size_intersection):
							for inter in itertools.combinations(intersection, sku_combination_size):
								tmp = set()
								tmp.add(sku)
								tmp = tmp | set(inter)
								trans = set()
								trans.add(i)
								trans.add(j)
								general_tree.add_combination(tmp, trans)

			general_tree.print_values(file, sigma)
			
		#remove sku in order to reduce search space
		for t in sku_list:
			transactions[t].remove(sku)
	file.close()
	
else:
	supermarket.Exception(1)