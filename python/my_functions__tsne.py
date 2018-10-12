'''
import sys
sys.path.insert(0, './my_functions')

from my_functions__tsne import (display_closest_words_tsne_scatterplot_1D, 
                                display_closest_words_tsne_scatterplot_2D,
                                display_selected_words_tsne_scatterplot_2D,
                                display_selected_words_tsne_scatterplot_3D
                                )
'''


from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np


def display_closest_words_tsne_scatterplot_1D(model, word, word2vec_size):

    arr = np.empty((0, word2vec_size), dtype='f')
    word_labels = [word]

    # get close words
    close_words = model.similar_by_word(word)

    # add the vector for each of the closest words to the array
    arr = np.append(arr, np.array([model[word]]), axis=0)
    for wrd_score in close_words:
        wrd_vector = model[wrd_score[0]]
        word_labels.append(wrd_score[0])
        arr = np.append(arr, np.array([wrd_vector]), axis=0)
        
    # find tsne coords for 2 dimensions
    tsne = TSNE(n_components=1, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(arr)
    print('tsne shape:', Y.shape)
    print('tsne type:', type(Y.ravel().tolist()))

    for i,l in zip(Y.ravel().tolist(),word_labels):
        print('Y:',i,l)

    x_coords = Y[:, 0]
    #y_coords = Y[:, 1]
    # display scatter plot
    #plt.scatter(x_coords, y_coords)
    #plt.plot(Y.ravel(),np.ones(np.shape(Y.ravel())),'*',markersize=10)

    # val = 0. # this is the value where you want the data to appear on the y-axis.
    # ar = np.arange(10) # just as an example array
    # plt.plot(Y.ravel(), np.zeros_like(Y.ravel()) + val, 'x')

    #plt.plot(Y.ravel().tolist(), len(Y.ravel().tolist()) * [1], "x")
    # plt.plot(Y)
    #plt.show()


    x_coords = Y.ravel()
    y_coords = np.zeros_like(Y.ravel())
    #y_coords = np.asarray([x*1 for x in range(1,12,100)])

    lim = 0.00005
    lim = 1000
    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.xlim(x_coords.min()+lim, x_coords.max()+lim)
    plt.ylim(y_coords.min()+lim, y_coords.max()+lim)
    plt.show()

def display_closest_words_tsne_scatterplot_2D(model, word, word2vec_size):

    arr = np.empty((0, word2vec_size), dtype='f')
    word_labels = [word]

    # get close words
    close_words = model.similar_by_word(word)

    # add the vector for each of the closest words to the array
    arr = np.append(arr, np.array([model[word]]), axis=0)
    for wrd_score in close_words:
        wrd_vector = model[wrd_score[0]]
        word_labels.append(wrd_score[0])
        arr = np.append(arr, np.array([wrd_vector]), axis=0)
        
    # find tsne coords for 2 dimensions
    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(arr)

    x_coords = Y[:, 0]
    y_coords = Y[:, 1]
    # display scatter plot
    plt.scatter(x_coords, y_coords)

    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.xlim(x_coords.min()+0.00005, x_coords.max()+0.00005)
    plt.ylim(y_coords.min()+0.00005, y_coords.max()+0.00005)
    plt.show()


def display_selected_words_tsne_scatterplot_2D(model, words_ls, word2vec_size):

    arr = np.empty((0, word2vec_size), dtype='f')
    word_labels = []

    # get close words
    #close_words = model.similar_by_word(word)

    # add the vector for each of the closest words to the array
    #arr = np.append(arr, np.array([model[word]]), axis=0)
    for wrd in words_ls:
        wrd_vector = model[wrd]
        word_labels.append(wrd)
        arr = np.append(arr, np.array([wrd_vector]), axis=0)
        
    # find tsne coords for 2 dimensions
    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(arr)

    x_coords = Y[:, 0]
    y_coords = Y[:, 1]
    # display scatter plot
    plt.scatter(x_coords, y_coords)

    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.xlim(x_coords.min()+0.00005, x_coords.max()+0.00005)
    plt.ylim(y_coords.min()+0.00005, y_coords.max()+0.00005)
    plt.show()

def display_selected_words_tsne_scatterplot_3D(model, words_ls, word2vec_size):

	arr = np.empty((0, word2vec_size), dtype='f')
	word_labels = []

    # get close words
    #close_words = model.similar_by_word(word)

    # add the vector for each of the closest words to the array
    #arr = np.append(arr, np.array([model[word]]), axis=0)
	for wrd in words_ls:
		wrd_vector = model[wrd]
		word_labels.append(wrd)
		arr = np.append(arr, np.array([wrd_vector]), axis=0)
        
    # find tsne coords for 2 dimensions
	tsne = TSNE(n_components=3, random_state=0)
	np.set_printoptions(suppress=True)
	Y = tsne.fit_transform(arr)

	x_coords = Y[:, 0]
	y_coords = Y[:, 1]
	z_coords = Y[:, 2]

	# display scatter plot
	fig=plt.figure()
	ax = fig.gca(projection='3d')
	#cset = ax.contour(x_coords, y_coords, z_coords) #, 16, extend3d=True)

	for x,y,z,word in zip(x_coords, y_coords, z_coords, words_ls):
		#ax.plot(x,y,z, 'gray')  # draws line
		ax.scatter(x,y,z, c='blue', edgecolors='none', s=50)  # draws dots
		ax.text(x,y,z, word, size=10, zorder=1, color='k') # puts annotations over dots

	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	plt.show()
