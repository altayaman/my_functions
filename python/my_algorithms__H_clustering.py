'''
import sys
sys.path.insert(0, './my_functions')
from my_algorithms__H_clustering import H_clustering
'''


import numpy as np
import itertools
from copy import deepcopy
# from my_functions__distance import (get_cosine_similarity, 
# 								    get_euclidian_distance, 
# 								    get_euclidian_distance_2, 
# 								    get_dist__two_words,
# 								    get_dist__multiple_words,
# 								    get_ceil
# 								    )


'''
Current class does Hierachical clustering and returns lustered items as just a list,
so it won't be clear how items are clustered.

Ex:
	ls_input  = [1,9,2,7]
	ls_output = [1,2,7,9]

	so in this toy input ls_input you can see that ls_output is h_clustered
	where [1,2] is one cluster as they are close to each other
	and [7,9] is another subcluster, and finally they are in one single
	super-cluster which is [ [1,2], [7,9] ].

	But in stead of this [ [1,2], [7,9] ] it gives us [1,2,7,9].

USAGE:
	# model - word2vec model
	# words_vocab_ls - list of words that should be present in word2vec model

	h_clust = H_clustering(words_vocab_ls, model)
	A = h_clust.cluster()

	print('Final clusters:', A)

'''
class H_clustering():
	def __init__(self, ls, model):
		self.clusters = [[e] for e in ls]
		#print('self.clusters: ', self.clusters)
		self.model = model

	def cluster(self):

		while(len(self.clusters) > 1):
			cl_1_idx = None
			cl_2_idx = None
			cl_1_merge_part = None
			cl_2_merge_part = None
			shortest_dist = 10000000

			idx_ls = [i for i in range(len(self.clusters))]
			#print('idx_ls: ', idx_ls)

			for i in idx_ls[0:-1]:
				for j in idx_ls[i+1:]:
					part_1, part_2, dist = self.get_merging_ends(self.clusters[i], self.clusters[j], self.model)

					if(dist < shortest_dist):
						shortest_dist   = dist
						cl_1_idx = i
						cl_2_idx = j
						cl_1_merge_part = part_1
						cl_2_merge_part = part_2

						#print(cl_1_idx, cl_2_idx, cl_1_merge_part, cl_2_merge_part)



			#print('Merging clusters: ', self.clusters[cl_1_idx], self.clusters[cl_2_idx])
			merged_clusters = self.merge_clusters(self.clusters[cl_1_idx], self.clusters[cl_2_idx], cl_1_merge_part, cl_2_merge_part)
			merged_clusters = [merged_clusters]

			idx_ls = [e for e in idx_ls if e not in [cl_1_idx, cl_2_idx]]
			#print('idx popped: ', idx_ls, cl_1_idx, cl_2_idx)

			self.clusters = [self.clusters[i] for i in idx_ls] + merged_clusters
			#print('self.clusters: ', self.clusters)
			#print

		return self.clusters[0]

	def get_merging_ends(self, cl_1, cl_2, model):
		comb = [(0,0), (-1, -1), (0, -1), (-1, 0)]
		shortest_dist = 1000000
		cl_1_merge_part = cl_2_merge_part = None

		for c in comb:
			w1 = cl_1[c[0]]
			w2 = cl_2[c[1]]
			word_vec_1 = model[w1]
			word_vec_2 = model[w2]

			dist = self.get_euclidian_distance_2(word_vec_1, word_vec_2)
			if(dist < shortest_dist):
				shortest_dist = dist
				cl_1_merge_part = c[0]
				cl_2_merge_part = c[1]

		return cl_1_merge_part, cl_2_merge_part, shortest_dist

	def get_euclidian_distance_2(self, word_vec_1, word_vec_2):

		return np.linalg.norm(word_vec_1 - word_vec_2)

	def merge_clusters(self, cl_1, cl_2, cl_1_idx, cl_2_idx):
		if(cl_1_idx==0 and cl_2_idx==0):
			#print('Merging clusters: ', self.reverse_ls(cl_1) + cl_2)
			return self.reverse_ls(cl_1) + cl_2

		elif(cl_1_idx==-1 and cl_2_idx==-1):
			return cl_1 + self.reverse_ls(cl_2)

		elif(cl_1_idx==0 and cl_2_idx==-1):
			return cl_2 + cl_1

		elif(cl_1_idx==-1 and cl_2_idx==0):
			return cl_1 + cl_2

	def reverse_ls(self, ls):
		# for i in range(int(len(ls)/2)):
		# 	temp = ls[i]
		# 	ls[i] = ls[-1-i]
		# 	ls[-1-i] = temp

		return [e for e in reversed(ls)]


'''
Current class is used to store superlist of complex nested lists
and flat form of superlist.
'''
class Cluster_Object():
	def __init__(self, ls=None, flat=None):
		#if(len(ls) == 1 and flat is None):
		if(isinstance(ls, list) and flat is None):
			self.cluster = ls
			self.flat = ls
		elif(isinstance(ls, list) and isinstance(flat, list)):
			self.cluster = ls
			self.flat = flat
		else:
			self.cluster = None
			self.flat = None


	def merge(self, cluster_object):
		if(isinstance(cluster_object, Cluster_Object)):
			cl = [self.cluster] + [cluster_object.get_cluster_deepcopy()]
			fl = self.flat + cluster_object.get_flat_deepcopy()
			return Cluster_Object(cl, fl)
		else:
			print('ERROR: \n\tmerging object should be Cluster_Object')

	def get_cluster_deepcopy(self):

		return deepcopy(self.cluster)

	def get_flat_deepcopy(self):

		return deepcopy(self.flat)

	def get_cluster(self):

		return self.cluster

	def get_flat(self):

		return self.flat

	def set_cluster(self, cl):

		self.cluster = cl

	def set_flat(self, fl):

		self.flat = fl

	def reverse(self):
		self.cluster.reverse()
		self.flat.reverse()

		return self


'''
Current class does Hierachical clustering as previous one (e.g. H_clustering class),
but it fixes the clustered output issue which H_clustering class has.

So H_clustering_2 class provides a result list where each pair of subclusters
are separate in nested list.

H_clustering_2 class uses helper Cluster_Object class.

USAGE:
	# model - word2vec model
	# words_vocab_ls - list of words that should be present in word2vec model

	h_clust = H_clustering_2(words_vocab_ls, model)
	A = h_clust.cluster(stop_at = 3) # stop clustering when 3 clusters are formed

	print('Final clusters:', A.get_cluster())  # h_clustered words as superlist of nested lists cluster pairs
	print 'Final flat:', A.get_flat()          # flat form of above superlist.
'''
class H_clustering_2():
	def __init__(self, ls, model):
		#self.clusters = [[e] for e in ls]
		self.clusters = [Cluster_Object([e]) for e in ls]
		self.model = model

	def cluster(self, stop_at=1):

		while(len(self.clusters) > stop_at):
			# if(stop_at is not None):
			# 	if(len(self.clusters) == stop_at):
			# 		break

			cl_1_idx = None
			cl_2_idx = None
			cl_1_merge_part = None
			cl_2_merge_part = None
			shortest_dist = 10000000

			idx_ls = [i for i in range(len(self.clusters))]
			#print('idx_ls: ', idx_ls)

			for i in idx_ls[0:-1]:
				for j in idx_ls[i+1:]:
					part_1, part_2, dist = self.get_merging_ends(self.clusters[i], self.clusters[j], self.model)

					if(dist < shortest_dist):
						shortest_dist   = dist
						cl_1_idx = i
						cl_2_idx = j
						cl_1_merge_part = part_1
						cl_2_merge_part = part_2

						#print(cl_1_idx, cl_2_idx, cl_1_merge_part, cl_2_merge_part)



			#print('Merging clusters: ', self.clusters[cl_1_idx], self.clusters[cl_2_idx])
			merged_clusters = self.merge_clusters(self.clusters[cl_1_idx], self.clusters[cl_2_idx], cl_1_merge_part, cl_2_merge_part)
			merged_clusters = [merged_clusters]

			idx_ls = [e for e in idx_ls if e not in [cl_1_idx, cl_2_idx]]
			#print('idx popped: ', idx_ls, cl_1_idx, cl_2_idx)

			self.clusters = [self.clusters[i] for i in idx_ls] + merged_clusters
			# print('self.clusters: ', self.clusters)
			#print



		#return self.clusters[0]
		return self.return_clusters()

	def return_clusters(self):
		new_cl_obj = Cluster_Object()

		cl = [cl_obj.get_cluster() for cl_obj in self.clusters]
		new_cl_obj.set_cluster(cl)

		fl = [cl_obj.get_flat() for cl_obj in self.clusters]
		fl = itertools.chain.from_iterable(fl)
		fl = list(fl)
		new_cl_obj.set_flat(fl)

		return new_cl_obj

	def get_merging_ends(self, cl_1, cl_2, model):
		comb = [(0,0), (-1, -1), (0, -1), (-1, 0)]
		shortest_dist = 1000000
		cl_1_merge_part = cl_2_merge_part = None

		# print('cluster 1:', cl_1.get_cluster(), cl_1.get_flat())
		# print('cluster 2:', cl_2.get_cluster(), cl_2.get_flat())

		cl_1_flat = cl_1.get_flat()
		cl_2_flat = cl_2.get_flat()
		for c in comb:
			w1 = cl_1_flat[c[0]]
			w2 = cl_2_flat[c[1]]
			# print('w1:',w1)
			# print('w2:',w2)

			word_vec_1 = model[w1]
			word_vec_2 = model[w2]

			dist = self.get_euclidian_distance_2(word_vec_1, word_vec_2)
			if(dist < shortest_dist):
				shortest_dist = dist
				cl_1_merge_part = c[0]
				cl_2_merge_part = c[1]

		return cl_1_merge_part, cl_2_merge_part, shortest_dist

	def get_euclidian_distance_2(self, word_vec_1, word_vec_2):

		return np.linalg.norm(word_vec_1 - word_vec_2)

	def merge_clusters(self, cl_1, cl_2, cl_1_idx, cl_2_idx):
		if(cl_1_idx==0 and cl_2_idx==0):
			#return [self.reverse_ls(cl_1)] + [cl_2]
			return cl_1.reverse().merge(cl_2)

		elif(cl_1_idx==-1 and cl_2_idx==-1):
			#return [cl_1] + [self.reverse_ls(cl_2)]
			return cl_1.merge(cl_2.reverse())

		elif(cl_1_idx==0 and cl_2_idx==-1):
			#return [cl_2] + [cl_1]
			return cl_2.merge(cl_1)


		elif(cl_1_idx==-1 and cl_2_idx==0):
			#return [cl_1] + [cl_2]
			return cl_1.merge(cl_2)

	def reverse_ls(self, ls):
		# for i in range(int(len(ls)/2)):
		# 	temp = ls[i]
		# 	ls[i] = ls[-1-i]
		# 	ls[-1-i] = temp

		return [e for e in reversed(ls)]