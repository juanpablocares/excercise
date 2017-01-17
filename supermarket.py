import os
import itertools

from collections import defaultdict

def reduce_transactions_using_sigma(transactions, skus_counter, sigma):
	for sku, count in skus_counter.items():
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
	return transactions

def create_intersection_matrix(transactions):
	intersections = dict()
	for i in range(len(transactions)):
		intersections[i] = dict()
		for j in range(i + 1, len(transactions)):
			local_intersection = transactions[i] & transactions[j]
			if len(local_intersection) >= 3:
				intersections[i][j] = local_intersection
	return intersections

def get_all_set(transactions):
	all_set = set()
	intersections = {}
	for i in range(len(transactions)):
		intersections[i] = {}
		for j in range(len(transactions)):
			intersection = transactions[i] & transactions[j]
			intersections[i][j] = intersection
			all_set = all_set | intersection
	return intersections, all_set
	
def Combinations(candidates, combination, large, all):
	"""
	Recursive algorithm to generate all combinations of
	a given combination
	
	Parameters
	----------
	candidates : set
		values that are not in the set combination
	combination : set
		previous node combination
	large : int
		large of the combination to generate
	all : dictionary
		stores all values of the generated combinations
	Returns
	-------
	dictionary
		all combinations founds until the moment
	"""
	#it is needed to setore the initial combination to
	#restart values of a variable
	initialCombination = set(combination)
	if len(combination) + 1 > large:
		return all

	for c in candidates:
		localCandidates = set(candidates)
		#remove the candidate that will be added to the
		#local combination
		localCandidates.remove(c)
		#restart local set of candidates
		combination = set(initialCombination)
		combination.add(c)
		if len(combination) == large:
			if SetToString(combination) not in all:
				all[SetToString(combination)] = 1
		else:
			all = Combinations(localCandidates, combination, large, all)
	return all

def GenerateCombinations(values, large):
	"""
	Call the recursive algorithm to find all combination of size large of
	a given transaction
	
	Parameters
	----------
	values : set
		Set of a transaction
	large : set
		Large of combinations to create
	Returns
	-------
	list
		list of sets combination of size 'large'
	"""
	combination = set()
	all = {}
	candidates = set(values)
	for c in candidates:
		combination = set()
		combination.add(c)
		candidates = set(values)
		candidates.remove(c)
		#start calling the recursive algorithm
		all = Combinations(candidates, combination, large, all)
	
	combinations = []
	#translate the dictionary to a list of sets
	for a, v in all.items():
		s = set()
		for i in range(large):
			s.add(int(a.split(' ')[i]))
		combinations.append(s)
	return combinations
		
def GetFrequentItems(transaction1, transaction2, ocurrences):
	"""
	Given two transactions this function 
	
	Parameters
	----------
	transaction1 : set
		Set of the a first transaction
	transaction2 : set
		Set of a second transaction
	ocurrences : dictionary
		Dictionary of combinations (key) of the first transaction
		and its counts
	tabu : dictionary
		Dictionary of all combinations given until this moment
		and its counts
	Returns
	-------
	dictionary
		dictionary with previous and actual combinations created
		between both transactions
	"""
	#find the intersection between both transactions
	inter = transaction1 & transaction2

	if len(inter) >= 3:
		#I tried to make this function work for "item sets
		#of size 3 or more" but in some cases it has issues (aprox 9) :(
		#for large in range(3, inter):
		for large in range(3, len(inter) + 1):
			#Create all the combinations of the intersection starting in 3
			#here are two version to get the combinations, my own one and 
			#itertools.combinations. If it is needed to activate the second one
			#it has to be commented lines 77,78,80 and uncomment 79
			#comb = []
			#comb = GenerateCombinations(inter, large)
			for it in itertools.combinations(inter, large):
			#for it in comb:
				#transform the combination into a string to store it in
				#a dictionary
				#if the combination is not yet in dictionary that store
				#all the combinations, it can continue. Otherwise it means
				#that this single combination has been already count
				strIt = SetToString(it)
				if strIt in ocurrences:
					#if enter here means that this combination has to be count
					#as a new one (first case) or just add one counter. The first
					#case start with 2 because it count the first combination
					#of the first transaction and the second one.
					ocurrences[strIt] = ocurrences[strIt] + 1
				else:
					ocurrences[strIt] = 2
	return ocurrences

def AppendFrequentItems(all, other):
	"""
	Store all the keys and values of the second parameter
	into the first paramter
	
	Parameters
	----------
	all : dictionary
		store all the combinations and its counts
	other : dictionary
		store the combinations and its counts of a single transaction
	Returns
	-------
	dictionary
		combination of the second dict and the first one
	"""
	for combination, value in other.items():
		if combination not in all:
			all[combination] = value
	return all

def WriteOutput(fileName, sigma, data):
	"""
	Write all data on the output file and filter it using sigma value
	
	Parameters
	----------
	sigma : int
		minimum frequency to be written on the file 
	data : dictionary
		store the combinations and its counts of the
		complete transaction log
	"""
	file = open(fileName.split('.')[0] + '.out', 'w')
	
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
	
def FileExist(filePath):
	"""
	Check if the input file exist
	
	Parameters
	----------
	fileName : string
		Name of the file

	Returns
	-------
	bool
		True if it exists, otherwise False
	"""
	return os.path.isfile(filePath)

def get_skus(data, size_group):
	"""
	Given an splitted data of skus, this
	function transform it in a set
	
	Parameters
	----------
	data : list
		list of sku's of a single transaction

	Returns
	-------
	set
		set of skus of a single transaction
	"""
	skus = set()
	for sku in data:
		skus.add(int(sku))
	#I discard a transaction if it has less
	#than 3 skus because there is no way that
	#this case can have 3 or more combinations
	if len(skus) >= size_group:
		return skus
	else:
		return set()

def SetToString(data):
	"""
	Transform a set to a string. This function
	is needed to the output format and to
	store in dictionaries
	
	Parameters
	----------
	data : set
		the set to transform

	Returns
	-------
	string
		string format of sets
	"""
	line = ''
	s = sorted(list(data))
	for it in range(len(s)-1):
		line += str(s[it]) + ' '
	line += str(s[len(s)-1])
	return line

def Exception(value):
	if value == 1:
		print 'Error: path file doesn\'t exist'