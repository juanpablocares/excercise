import os
import itertools

from collections import defaultdict

def FileExist(filePath):
	return os.path.isfile(filePath)

def GetSkus(data):
	skus = set()
	for sku in data:
		skus.add(sku)
	if len(skus) >= 3:
		return skus
	else:
		return set()

def GetFrequentItems(transaction1, transaction2, ocurrences, tabu):
	inter = transaction1 & transaction2
	for it in itertools.combinations(inter, 3):
		if str(set(it)) not in tabu:
			if str(set(it)) not in ocurrences:
				ocurrences[str(set(it))] = 2
			else:
				ocurrences[str(set(it))] = ocurrences[str(set(it))] + 1
	return ocurrences

def AppendFrequentItems(all, other):
	for combination, value in other.items():
		if combination not in all:
			all[combination] = value
		else:
			print 'error'
	return all
	
def Exception(value):
	if value == 1:
		print 'Error: path file doesn\'t exist'