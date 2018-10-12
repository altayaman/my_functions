'''
import sys
sys.path.insert(0, './my_functions')

from my_functions__permutation import (get_index_bounds, 
									   partition_indexes, 
									   permutations_one_thread, 
									   permutations_threaded,
									   get_best_words_permut_euclid_dist_one_thread,
									   get_best_words_permut_euclid_dist_threaded,
									   get_best_n_worst_words_permut_euclid_dist_threaded
									   )
'''


import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from copy import deepcopy
from itertools import permutations as iter_perm
from multiprocessing import Pool, Queue
from functools import partial
from my_functions__distance import (get_cosine_similarity, 
								    get_euclidian_distance, 
								    get_euclidian_distance_2, 
								    get_dist__two_words,
								    get_dist__multiple_words,
								    get_ceil
								    )

# Set of functions for threaded permutation
def get_index_bounds(ls, div = 4):
	rem = len(ls)%div
	chunk = (len(ls) - len(ls)%div)/div
	#print(rem, chunk)
	ls_parts = []

	s = 0
	e = 0
	while e != len(ls):
		if(rem > 0):
			s = e
			e = e + chunk + 1
			rem = rem - 1
		else:
			s = e
			e = e + chunk
		ls_parts.append([s,e-1])

	return ls_parts

def partition_indexes(ls, div = 4):
	for b in get_index_bounds(ls, div):
		#yield ls[b[0] : b[1]+1]
		yield [i for i in range(b[0], b[1]+1)]

def permutations_one_thread(ls, indexes):
	for i in indexes:
		for perm in iter_perm(ls[:i]+ls[i+1:]):
			yield (ls[i],) + perm

def permutations_threaded(ls, thread_num):
	for idx_ls in partition_indexes(ls, thread_num):
		print('idx_ls: ', idx_ls)
		for perm in permutations_one_thread(ls, idx_ls):
			print(list(perm))
		print()

lsd = []
def get_best_words_permut_euclid_dist_one_thread(words_ls, model, verbose, idx_ls):
	best_words_permut_2 = None
	best_words_permut_dist_ls = None
	dist_ls = []
	permut_dist_2 = 0
	shortest_permut__euclid_dist = 100000
	#for words_permut in itertools.permutations(words_ls):
	for words_permut in permutations_one_thread(words_ls, idx_ls):
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
			best_words_permut_2 = words_permut   # A
			best_words_permut_dist_ls = dist_ls  # B
		permut_dist_2 = 0
		dist_ls = []

	global lsd
	lsd.append((best_words_permut_2, best_words_permut_dist_ls))
	print('\n\t',best_words_permut_2, best_words_permut_dist_ls,'\n\t')
	return best_words_permut_2, best_words_permut_dist_ls


lsd_2 = []
def get_best_n_worst_words_permut_euclid_dist_one_thread(words_ls, model, verbose, idx_ls):
	best_words_permut_2 = None
	best_words_permut_dist_ls = None
	dist_ls = []
	permut_dist_2 = 0
	shortest_permut__euclid_dist = 100000

	worst_words_permut_2 = None
	worst_words_permut_dist_ls = None
	longest_permut__euclid_dist = 0
	#for words_permut in itertools.permutations(words_ls):
	for words_permut in permutations_one_thread(words_ls, idx_ls):
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
			best_words_permut_2 = words_permut   # A
			best_words_permut_dist_ls = dist_ls  # B

		if(permut_dist_2 > longest_permut__euclid_dist):
			longest_permut__euclid_dist = permut_dist_2
			worst_words_permut_2 = words_permut   # A
			worst_words_permut_dist_ls = dist_ls  # B

		permut_dist_2 = 0
		dist_ls = []

	#global lsd_2
	#lsd_2.append((best_words_permut_2, best_words_permut_dist_ls))
	#print('\n\t',best_words_permut_2, best_words_permut_dist_ls,'\n\t')
	return best_words_permut_2, best_words_permut_dist_ls, worst_words_permut_2, worst_words_permut_dist_ls

def get_best_words_permut_euclid_dist_threaded(words_ls, thread_num, model, verbose = False):
	indexes_ls = [idx_ls for idx_ls in partition_indexes(words_ls, thread_num)]
	print('indexes_ls: ', indexes_ls)

	results_ls = []

	is_verbose = False
	apply_predictions_partial = partial(get_best_words_permut_euclid_dist_one_thread, words_ls, model, is_verbose)
	#apply_predictions_partial = partial(get_best_words_permut_euclid_dist_one_thread, deepcopy(words_ls), deepcopy(model), is_verbose)
	pool = Pool(processes=thread_num)

	pool_results = pool.map(apply_predictions_partial, indexes_ls)
	#pool_results = pool.map_async(apply_predictions_partial, indexes_ls)
	pool.close()
	pool.join()


	short_d = 10000
	A = B = None
	for a,b in pool_results:
		if(sum(b) < short_d):
			A = a
			B = b

	return A,B


def get_best_n_worst_words_permut_euclid_dist_threaded(words_ls, thread_num, model, verbose = False):
	indexes_ls = [idx_ls for idx_ls in partition_indexes(words_ls, thread_num)]
	print('indexes_ls: ', indexes_ls)

	results_ls = []

	is_verbose = False
	apply_predictions_partial = partial(get_best_n_worst_words_permut_euclid_dist_one_thread, words_ls, model, is_verbose)
	#apply_predictions_partial = partial(get_best_words_permut_euclid_dist_one_thread, deepcopy(words_ls), deepcopy(model), is_verbose)
	pool = Pool(processes=thread_num)

	pool_results = pool.map(apply_predictions_partial, indexes_ls)
	#pool_results = pool.map_async(apply_predictions_partial, indexes_ls)
	pool.close()
	pool.join()


	short_d = 1000000
	long_d = 0
	BA = BB = WA = WB = None
	for ba,bb, wa,wb in pool_results:
		if(sum(bb) < short_d):
			BA = ba
			BB = bb
			short_d = sum(bb)

		if(sum(wb) > long_d):
			WA = wa
			WB = wb
			long_d = sum(wb)

	return BA,BB, WA,WB



