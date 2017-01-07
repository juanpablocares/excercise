#!/usr/bin/python

import sys
import supermarket

fileName = sys.argv[1]
sigma    = int(sys.argv[2])

if supermarket.FileExist(fileName):
	allFrequentItems = {}
	freq = {}
	transactions = []
	
	file = open(fileName)
	for line in file:
		skus = supermarket.GetSkus(line.strip().split(' '))
		if len(skus) != 0:
			transactions.append(skus)
	
	for i in range(len(transactions)):
		ocurrences = {}
		for j in range(i + 1, len(transactions)):
			ocurrences = supermarket.GetFrequentItems(transactions[i], transactions[j], ocurrences, allFrequentItems)
		allFrequentItems = supermarket.AppendFrequentItems(allFrequentItems, ocurrences)

	supermarket.WriteOutput(sigma, allFrequentItems)
else:
	supermarket.Exception(1)