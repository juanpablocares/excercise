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

def SetToString(data):
	line = ''
	for it in data:
		line += str(it) + ' '
	return line
		
def GetFrequentItems(transaction1, transaction2, ocurrences, tabu):
	inter = transaction1 & transaction2
	strIt = ''
	for large in range(3, len(inter)):
		for it in itertools.combinations(inter, large):
			strIt = SetToString(it)
			if strIt not in tabu:
				if strIt not in ocurrences:
					ocurrences[strIt] = 2
				else:
					ocurrences[strIt] = ocurrences[strIt] + 1
	return ocurrences

def AppendFrequentItems(all, other):
	for combination, value in other.items():
		if combination not in all:
			all[combination] = value
		else:
			print 'error'
	return all

def WriteOutput(sigma, data):
	file = open('out.txt', 'w')
	
	for key, value in data.items():
		if value >= sigma:
			combination = key.split(' ')
			line = str(len(combination) - 1) + ', '
			line += str(value) + ', '
			listComb = list(combination)
			for i in range(len(listComb) - 2):
				line += str(listComb[i]) + ', '
			line += str(listComb[len(listComb) - 2])
			file.write(line + '\n')
	file.close()
	
def Exception(value):
	if value == 1:
		print 'Error: path file doesn\'t exist'