'''
import sys
sys.path.insert(0, './my_functions')

from my_algorithms__best_permute import (get_best_words_permut_cos_sim, 
										 get_best_words_permut_euclid_dist,
										 get_best_n_worst_words_permut_euclid_dist,
										 merge_
										 )
'''


import itertools
from my_functions__distance import (get_cosine_similarity, 
								    get_euclidian_distance, 
								    get_euclidian_distance_2, 
								    get_dist__two_words,
								    get_dist__multiple_words,
								    get_ceil
								    )

# returns (words permutation, distances between words)
def get_best_words_permut_cos_sim(words_ls, model, verbose = False):
	best_words_permut_1 = None
	best_words_permut_dist_ls = None
	dist_ls = []
	permut_dist_1 = 0
	shortest_permut__cos_dist = 100000

	for words_permut in itertools.permutations(words_ls):
		if(verbose):
			print('i:', words_permut)

		#calculate dist between each word in permutation
		for i in range(len(words_permut)-1):
			word_1 = words_permut[i]
			word_2 = words_permut[i+1]
			#cos_dist_1 = model.similarity(word_1, word_1)
			#print word_1, word_2, cos_dist_1

			word_vec_1 = model[word_1]
			word_vec_2 = model[word_2]
			cos_dist_2 = get_cosine_similarity(word_vec_1, word_vec_2)
			dist_ls.append(cos_dist_2)
			permut_dist_1 = permut_dist_1 + cos_dist_2

			if(verbose):
				print(word_1, word_2, cos_dist_2)
				print(permut_dist_1)


		if(permut_dist_1 < shortest_permut__cos_dist):
			shortest_permut__cos_dist = permut_dist_1
			best_words_permut_1 = words_permut
			best_words_permut_dist_ls = dist_ls
		permut_dist_1 = 0
		dist_ls = []


	return best_words_permut_1, best_words_permut_dist_ls

# returns (words permutation, distances between words)
def get_best_words_permut_euclid_dist(words_ls, model, verbose = False):
	best_words_permut_2 = None
	best_words_permut_dist_ls = None
	dist_ls = []
	permut_dist_2 = 0
	shortest_permut__euclid_dist = 100000
	for words_permut in itertools.permutations(words_ls):
		if(verbose):
			print('i:', words_permut)

		#calculate dist between each word in permutation
		for i in range(len(words_permut)-1):
			word_1 = words_permut[i]
			word_2 = words_permut[i+1]
			#cos_dist_1 = model.similarity(word_1, word_1)
			#print word_1, word_2, cos_dist_1

			word_vec_1 = model[word_1]
			word_vec_2 = model[word_2]
			#distance   = get_euclidian_distance(word_vec_1, word_vec_2)
			distance   = get_euclidian_distance_2(word_vec_1, word_vec_2)
			dist_ls.append(distance)
			permut_dist_2 = permut_dist_2 + distance

			if(verbose):
				print(word_1, word_2, distance)
				print(permut_dist_2)


		if(permut_dist_2 < shortest_permut__euclid_dist):
			shortest_permut__euclid_dist = permut_dist_2
			best_words_permut_2 = words_permut
			best_words_permut_dist_ls = dist_ls
		permut_dist_2 = 0
		dist_ls = []

	return best_words_permut_2, best_words_permut_dist_ls

def get_best_n_worst_words_permut_euclid_dist(words_ls, model, verbose = False):
	best_words_permut_2 = None
	best_words_permut_dist_ls = None
	dist_ls = []
	permut_dist_2 = 0
	shortest_permut__euclid_dist = 100000

	worst_words_permut_2 = None
	worst_words_permut_dist_ls = None
	longest_permut__euclid_dist = 0

	for words_permut in itertools.permutations(words_ls):
		if(verbose):
			print('i:', words_permut)

		#calculate dist between each word in permutation
		for i in range(len(words_permut)-1):
			word_1 = words_permut[i]
			word_2 = words_permut[i+1]
			#cos_dist_1 = model.similarity(word_1, word_1)
			#print word_1, word_2, cos_dist_1

			word_vec_1 = model[word_1]
			word_vec_2 = model[word_2]
			#distance   = get_euclidian_distance(word_vec_1, word_vec_2)
			distance   = get_euclidian_distance_2(word_vec_1, word_vec_2)
			dist_ls.append(distance)
			permut_dist_2 = permut_dist_2 + distance

			if(verbose):
				print(word_1, word_2, distance)
				print(permut_dist_2)


		if(permut_dist_2 < shortest_permut__euclid_dist):
			shortest_permut__euclid_dist = permut_dist_2
			best_words_permut_2 = words_permut
			best_words_permut_dist_ls = dist_ls

		if(permut_dist_2 > longest_permut__euclid_dist):
			longest_permut__euclid_dist = permut_dist_2
			worst_words_permut_2 = words_permut   # A
			worst_words_permut_dist_ls = dist_ls  # B

		permut_dist_2 = 0
		dist_ls = []

	return best_words_permut_2, best_words_permut_dist_ls, worst_words_permut_2, worst_words_permut_dist_ls

# A: words permutation
# B: distances between words
def merge_(A,B):
	temp_ls = []
	for i in range(len(B)):
		temp_ls.append(A[i])
		temp_ls.append(B[i])
	temp_ls.append(A[len(A)-1])
	
	return temp_ls




