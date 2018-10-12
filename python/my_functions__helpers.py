'''
import sys
sys.path.insert(0, './my_functions')

from my_functions__helpers import (current_script_dir,
								   print_elapsed_time,
								   iter_CSV_with_index,
								   flatten_list
								   )
'''


from os.path import isfile, isdir, exists, join, abspath, dirname
import time

def current_script_dir(my_path):

	return dirname(abspath(my_path)) + '/'

def print_elapsed_time(start_time):
	elapsed_time = time.time()-start_time
	str_ = 'Time spent for training:' + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
	print(str_)

def iter_CSV_with_index(my_infile_path, delim=';'):
    #with open(my_infile_path, 'r', encoding='utf-8-sig') as infile:
    #with open(my_infile_path, 'r', encoding = "ISO-8859-1") as infile:
    with codecs.open(my_infile_path, "r", encoding='cp1251', errors='ignore') as infile:
    #with codecs.open(my_infile_path, "r", encoding='utf-8-sig', errors='ignore') as infile:
        csv_reader = csv.DictReader(infile, delimiter=delim)
        for idx, row in enumerate(csv_reader):
            yield ((idx+1), row)

def iter_netsed_list(ls):
    for e in ls:
        if isinstance(e, (list,tuple)):
            for ee in flatten_list(e):
                yield ee
        else:
            yield e

def flatten_list(ls):

	return list(iter_netsed_list(ls))
