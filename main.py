#!/usr/bin/python

import sys
import supermarket

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
	
	file = open(fileName)
	for line in file:
		skus = supermarket.GetSkus(line.strip().split(' '))
		if len(skus) != 0:
			transactions.append(skus)
	
	#iterate over each transaction and all the next values
	#without returning to the previous one
	for i in range(len(transactions)):
		#this dictionary stores all the combinations that can be given
		#with the transaction i and all the rest
		ocurrences = {}
		for j in range(i + 1, len(transactions)):
			ocurrences = supermarket.GetFrequentItems(transactions[i],
			                                          transactions[j],
													  ocurrences,
													  allFrequentItems)
		allFrequentItems = supermarket.AppendFrequentItems(allFrequentItems, ocurrences)

	supermarket.WriteOutput(sigma, allFrequentItems)
else:
	supermarket.Exception(1)