'''
import sys
sys.path.insert(0, './my_functions')
from my_algorithms__Held_Karp import Held_Karp
'''


import numpy as np

class Held_Karp():

	def __init__(self, model, words_ls, start_index = 0):
		self.memo_path2dist = {}
		self.memo_path2visited = {}
		self.memo_path2unvisited = {}
		self.memo_group2paths = {}
		self.last_group = 0
		#self.visited_glob = None
		#self.unvisited_glob = None
		self.go_on = False
		self.counter = 0
		self.model = model

		self.shortest_path = None
		self.shortest_path_dist_ls = None

		self.start_glob = self.visited_glob = [words_ls[start_index]]
		self.unvisited_glob = words_ls[:start_index] + words_ls[start_index+1:]

		#self.set_traversing_settings(words_ls, start_index)

	def set_traversing_settings(self, words_ls, idx):
		self.start_glob = self.visited_glob = [words_ls[idx]] 
		self.unvisited_glob = words_ls[:idx] + words_ls[idx+1:]

	def get_len_from_memo(self, ls_key):
		if(len(ls_key) == 1):
			return 0
		else:
			k = self.ls_to_key(ls_key)
			return self.memo_path2dist[k]

	def ls_to_key(self, ls):

		return '__'.join([str(i) for i in ls])

	def get_euclidian_distance(self, word_vec_1, word_vec_2):
		distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(word_vec_1, word_vec_2)]))
		return distance

	def get_euclidian_distance_2(self, word_vec_1, word_vec_2):

		return np.linalg.norm(word_vec_1 - word_vec_2)

	def Held_Karp(self):
		if(self.last_group == 0):
			self.last_group = self.last_group + 1
			self.memo_group2paths[self.last_group] = []

			for i in range(len(self.unvisited_glob)):
				s = self.visited_glob[:1] + [self.unvisited_glob[i]] + self.visited_glob[1:]
				l = self.unvisited_glob[:i] + self.unvisited_glob[i+1:]

				prev_len = self.get_len_from_memo(s[1:])
				#new_len  = get_len(mtx, s[0], s[1])
				word_vec_1 = self.model[s[0]]
				word_vec_2 = self.model[s[1]]
				new_len   = self.get_euclidian_distance_2(word_vec_1, word_vec_2)
				new_dist = prev_len + new_len
				k = self.ls_to_key(s)
				#print(s, ls_to_key(s), l, new_dist)

				self.memo_path2dist[k] = new_dist
				self.memo_path2visited[k] = s
				self.memo_path2unvisited[k] = l
				self.memo_group2paths[self.last_group].append(k)

				self.counter+=1
				if(len(l) > 0):
					self.go_on = True

			# print('memo_path2dist:', memo_path2dist)
			# print('memo_path2visited:', memo_path2visited)
			# print('memo_path2unvisited:', memo_path2unvisited)
			# print('memo_group2paths:', memo_group2paths)
			#print()

			if(self.go_on):
				self.go_on = False
				self.Held_Karp()
		else:
			self.last_group = self.last_group + 1
			self.memo_group2paths[self.last_group] = []
			for path_key in self.memo_group2paths[self.last_group-1]:

				#print('last_group:',last_group-1)
				#print('path_key:', path_key)
				#print('memo_path2unvisited[path_key]:', memo_path2unvisited[path_key])
				#print()

				self.visited_glob = self.memo_path2visited[path_key]
				self.unvisited_glob = self.memo_path2unvisited[path_key]
				for i in range(len(self.unvisited_glob)):
					s = self.visited_glob[:1] + [self.unvisited_glob[i]] + self.visited_glob[1:]
					l = self.unvisited_glob[:i] + self.unvisited_glob[i+1:]

					# prev_len = get_len_from_memo(memo_path2dist, s[:2])
					# new_len  = get_len(mtx, s[0], s[1])
					prev_len = self.get_len_from_memo(s[:-1])
					#new_len  = get_len(mtx, s[-2], s[-1])
					word_vec_1 = self.model[s[-2]]
					word_vec_2 = self.model[s[-1]]
					new_len   = self.get_euclidian_distance_2(word_vec_1, word_vec_2)
					new_dist = prev_len + new_len
					k = self.ls_to_key(s)
					#print(s, ls_to_key(s), l, new_dist, prev_len, s[:-1])
					#print()

					self.memo_path2dist[k] = new_dist
					self.memo_path2visited[k] = s
					self.memo_path2unvisited[k] = l
					self.memo_group2paths[self.last_group].append(k)

					self.counter+=1
					if(len(l) > 0):
						self.go_on = True
			
			if(self.go_on):
				self.go_on = False
				self.Held_Karp()
			else:
				self.last_group = self.last_group + 1
				self.memo_group2paths[self.last_group] = []
				for path in self.memo_group2paths[self.last_group-1]:
					self.counter+=1
					# print('Path dist: ', path, memo_path2dist[path])
					# print('Path visited: ', path, memo_path2visited[path])

					s = self.memo_path2visited[path] + self.start_glob
					word_vec_1 = self.model[s[-2]]
					word_vec_2 = self.model[s[-1]]
					new_len   = self.get_euclidian_distance_2(word_vec_1, word_vec_2)
					new_dist = self.memo_path2dist[path] + new_len
					k = self.ls_to_key(s)

					self.memo_path2dist[k] = new_dist
					self.memo_path2visited[k] = s
					self.memo_path2unvisited[k] = l
					self.memo_group2paths[self.last_group].append(k)
					#pass

				# for path in memo_group2paths[last_group]:
				# 	print('Path dist: ', path, memo_path2dist[path])
					#print('Path visited: ', path, memo_path2visited[path])

	def get_dist_between_words(self, words_ls, model):
		ls = []
		for i in range(len(words_ls)-1):
			w1 = words_ls[i]
			w2 = words_ls[i+1]
			w1_vec = model[w1]
			w2_vec = model[w2]
			dist = self.get_euclidian_distance_2(w1_vec, w2_vec)
			ls.append(dist)

		return ls

	def find_shortest_path_details(self):
		d = 10000000
		p_key = None
		for path in self.memo_group2paths[self.last_group]:
			#print('Path dist: ', path, memo_path2dist[path])
			if(self.memo_path2dist[path] < d):
				d = self.memo_path2dist[path]
				p_key = path
				# self.shortest_path_dist = self.memo_path2dist[path]
				# self.shortest_path = self.memo_path2visited[path]

		self.shortest_path = self.memo_path2visited[p_key]
		self.shortest_path_dist_ls = self.get_dist_between_words(self.shortest_path, self.model)

	def run_Held_Karp(self):
		self.Held_Karp()
		self.find_shortest_path_details()

	def get_shortest_path(self):

		return self.shortest_path

	def get_shortest_path_dist_ls(self):

		return self.shortest_path_dist_ls

	def get_time_complexity(self):

		return self.counter


class Held_Karp_v2():

	def __init__(self, model, words_ls, start_index = 0):
		self.memo_path2dist = {}
		self.memo_path2visited = {}
		self.memo_path2unvisited = {}
		self.memo_group2paths = {}
		self.last_group = 0
		#self.visited_glob = None
		#self.unvisited_glob = None
		self.go_on = False
		self.counter = 0
		self.model = model

		self.shortest_path = None
		self.shortest_path_dist_ls = None

		self.start_glob = self.visited_glob = [words_ls[start_index]]
		self.unvisited_glob = words_ls[:start_index] + words_ls[start_index+1:]

		self.words_2_strnum = self.get_words_2_strnum(words_ls)
		#self.set_traversing_settings(words_ls, start_index)


	def get_words_2_strnum(self, words_ls):
		words_2_num = {}
		for idx, w in enumerate(words_ls):
			words_2_num[w] = str(idx + 1)

		return words_2_num

	def set_traversing_settings(self, words_ls, idx):
		self.start_glob = self.visited_glob = [words_ls[idx]] 
		self.unvisited_glob = words_ls[:idx] + words_ls[idx+1:]

	def get_len_from_memo(self, ls_key):
		if(len(ls_key) == 1):
			return 0
		else:
			k = self.ls_to_key_2(ls_key)
			return self.memo_path2dist[k]

	# def ls_to_key(self, ls):

	# 	return '__'.join([str(i) for i in ls])

	def ls_to_key_2(self, ls):

		return '_'.join([self.words_2_strnum[i] for i in ls])

	def get_euclidian_distance(self, word_vec_1, word_vec_2):
		distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(word_vec_1, word_vec_2)]))
		return distance

	def get_euclidian_distance_2(self, word_vec_1, word_vec_2):

		return np.linalg.norm(word_vec_1 - word_vec_2)

	def Held_Karp(self):
		if(self.last_group == 0):
			self.last_group = self.last_group + 1
			self.memo_group2paths[self.last_group] = []

			for i in range(len(self.unvisited_glob)):
				s = self.visited_glob[:1] + [self.unvisited_glob[i]] + self.visited_glob[1:]
				l = self.unvisited_glob[:i] + self.unvisited_glob[i+1:]

				prev_len = self.get_len_from_memo(s[1:])
				#new_len  = get_len(mtx, s[0], s[1])
				word_vec_1 = self.model[s[0]]
				word_vec_2 = self.model[s[1]]
				new_len   = self.get_euclidian_distance_2(word_vec_1, word_vec_2)
				new_dist = prev_len + new_len
				k = self.ls_to_key_2(s)
				#print(s, ls_to_key(s), l, new_dist)

				self.memo_path2dist[k] = new_dist
				self.memo_path2visited[k] = s
				self.memo_path2unvisited[k] = l
				self.memo_group2paths[self.last_group].append(k)

				self.counter+=1
				if(len(l) > 0):
					self.go_on = True

			# print('memo_path2dist:', memo_path2dist)
			# print('memo_path2visited:', memo_path2visited)
			# print('memo_path2unvisited:', memo_path2unvisited)
			# print('memo_group2paths:', memo_group2paths)
			#print()

			if(self.go_on):
				self.go_on = False
				self.Held_Karp()
		else:
			self.last_group = self.last_group + 1
			self.memo_group2paths[self.last_group] = []
			for path_key in self.memo_group2paths[self.last_group-1]:

				#print('last_group:',last_group-1)
				#print('path_key:', path_key)
				#print('memo_path2unvisited[path_key]:', memo_path2unvisited[path_key])
				#print()

				self.visited_glob = self.memo_path2visited[path_key]
				self.unvisited_glob = self.memo_path2unvisited[path_key]
				for i in range(len(self.unvisited_glob)):
					s = self.visited_glob[:1] + [self.unvisited_glob[i]] + self.visited_glob[1:]
					l = self.unvisited_glob[:i] + self.unvisited_glob[i+1:]

					# prev_len = get_len_from_memo(memo_path2dist, s[:2])
					# new_len  = get_len(mtx, s[0], s[1])
					prev_len = self.get_len_from_memo(s[:-1])
					#new_len  = get_len(mtx, s[-2], s[-1])
					word_vec_1 = self.model[s[-2]]
					word_vec_2 = self.model[s[-1]]
					new_len   = self.get_euclidian_distance_2(word_vec_1, word_vec_2)
					new_dist = prev_len + new_len
					k = self.ls_to_key_2(s)
					#print(s, ls_to_key(s), l, new_dist, prev_len, s[:-1])
					#print()

					self.memo_path2dist[k] = new_dist
					self.memo_path2visited[k] = s
					self.memo_path2unvisited[k] = l
					self.memo_group2paths[self.last_group].append(k)

					self.counter+=1
					if(len(l) > 0):
						self.go_on = True
			
			if(self.go_on):
				self.go_on = False
				self.Held_Karp()
			else:
				self.last_group = self.last_group + 1
				self.memo_group2paths[self.last_group] = []
				for path in self.memo_group2paths[self.last_group-1]:
					self.counter+=1
					# print('Path dist: ', path, memo_path2dist[path])
					# print('Path visited: ', path, memo_path2visited[path])

					s = self.memo_path2visited[path] + self.start_glob
					word_vec_1 = self.model[s[-2]]
					word_vec_2 = self.model[s[-1]]
					new_len   = self.get_euclidian_distance_2(word_vec_1, word_vec_2)
					new_dist = self.memo_path2dist[path] + new_len
					k = self.ls_to_key_2(s)

					self.memo_path2dist[k] = new_dist
					self.memo_path2visited[k] = s
					self.memo_path2unvisited[k] = l
					self.memo_group2paths[self.last_group].append(k)
					#pass

				# for path in memo_group2paths[last_group]:
				# 	print('Path dist: ', path, memo_path2dist[path])
					#print('Path visited: ', path, memo_path2visited[path])

	def get_dist_between_words(self, words_ls, model):
		ls = []
		for i in range(len(words_ls)-1):
			w1 = words_ls[i]
			w2 = words_ls[i+1]
			w1_vec = model[w1]
			w2_vec = model[w2]
			dist = self.get_euclidian_distance_2(w1_vec, w2_vec)
			ls.append(dist)

		return ls

	def find_shortest_path_details(self):
		d = 10000000
		p_key = None
		for path in self.memo_group2paths[self.last_group]:
			#print('Path dist: ', path, memo_path2dist[path])
			if(self.memo_path2dist[path] < d):
				d = self.memo_path2dist[path]
				p_key = path
				# self.shortest_path_dist = self.memo_path2dist[path]
				# self.shortest_path = self.memo_path2visited[path]

		self.shortest_path = self.memo_path2visited[p_key]
		self.shortest_path_dist_ls = self.get_dist_between_words(self.shortest_path, self.model)

	def run_Held_Karp(self):
		self.Held_Karp()
		self.find_shortest_path_details()

	def get_shortest_path(self):

		return self.shortest_path

	def get_shortest_path_dist_ls(self):

		return self.shortest_path_dist_ls

	def get_time_complexity(self):

		return self.counter
