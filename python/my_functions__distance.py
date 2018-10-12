'''
import sys
sys.path.insert(0, './my_functions')

from my_functions__distance import (get_cosine_similarity, 
								    get_euclidian_distance, 
								    get_euclidian_distance_2, 
								    get_dist__two_words,
								    get_dist__multiple_words,
								    get_ceil
								    )
'''

import numpy as np
import math

def get_cosine_similarity(word_vec_1, word_vec_2):
	cosine_similarity = np.dot(word_vec_1, word_vec_2)/ \
						(np.linalg.norm(word_vec_1)* np.linalg.norm(word_vec_2))
	return cosine_similarity

def get_euclidian_distance(word_vec_1, word_vec_2):
	distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(word_vec_1, word_vec_2)]))
	return distance

def get_euclidian_distance_2(word_vec_1, word_vec_2):

	return np.linalg.norm(word_vec_1 - word_vec_2)

def get_dist__two_words(word_1, word_2, model, dist_func = None):
	if dist_func is None:
		print('You need to provide distance function.')
		return None

	word_vec_1 = model[word_1]
	word_vec_2 = model[word_2]
	#distance   = get_euclidian_distance(word_vec_1, word_vec_2)
	distance   = dist_func(word_vec_1, word_vec_2)

	return distance

def get_dist__multiple_words(words_ls, model, dist_func = None):
	if dist_func is None:
		print('You need to provide distance function.')
		return None

	distance_ls = []
	for i in range(len(words_ls)-1):
		distance = get_dist__two_words(words_ls[i], words_ls[i+1], model, dist_func = dist_func)
		distance_ls.append(distance)

	return distance_ls

def get_ceil(x, deg = 2):
	div = 10**deg
	if(isinstance(x,int) or isinstance(x,float)):
		return math.ceil(x*div)/div
	elif(isinstance(x, list)):
		return [math.ceil(f*div)/div for f in x]