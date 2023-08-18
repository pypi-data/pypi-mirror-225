import os
import pandas as pd
import time 
import random 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def rc(listo, to_remove = False):

    exclude = ['.DS_Store']
    if to_remove:
        exclude.extend(to_remove)

    ## Remove strings in list if string contains something from exclude
    inter = [s for s in listo if not any(x in s for x in exclude)]

    return inter

def pp(frame):
  inter = frame.copy()

  print(inter)
  print(inter.columns.tolist())


def unique_in_col(frame, col):
  inter = frame.copy()
  print(inter)
  print(inter.columns.tolist())
  print(inter[col].unique().tolist())


def null_in_col(frame, col):
  inter = frame.loc[frame[col].isna()].copy()
  print(inter)
  print(inter.columns.tolist())
  print(inter[col].unique().tolist())


def dumper(path, name, frame):
    with open(f'{path}/{name}.csv', 'w') as f:
        frame.to_csv(f, index=False, header=True)


def make_num(frame, col):
    copier = frame.copy()
    copier[col] = pd.to_numeric(copier[col])
    return copier


def combine_from_folder(pathos):

  listo = []

  fillos = os.listdir(pathos)
  fillos = [pathos + x for x in fillos if x != '.DS_Store']

  for fillo in fillos:
    inter = pd.read_csv(fillo)

    listo.append(inter)

  cat = pd.concat(listo)

  return cat


def print_headers(frame, num_row):
  copier = frame.copy()
  cols = copier.columns.tolist()
  for i in range(num_row, len(cols), num_row):
    first = i - num_row
    print(f"{str(cols[first:i])[1:-1]}")


def rand_delay(num):
  import random 
  import time 
  rando = random.random() * num
  print(rando)
  time.sleep(rando)


def return_similar(list_one, list_two, threshold=90, limit=5):

	from fuzzywuzzy import fuzz
	from fuzzywuzzy import process
	dicto = {}

	sec = list_two.copy()

	inter = [x for x in list_one if x not in sec]

	for word in inter:

		result = process.extract(word, sec, limit=limit)
		result = [x for x in result if (x[1] >= threshold) and (x[0] != word)] 
		# print(word)  
		# print(result) 

		if len(result) > 0:
				result = result[0]
				dicto[word] = result[0]

	return dicto 


def matcher(pattern, stringo, return_num):
  import re
  searcho = re.search(pattern, stringo).group(return_num)
  print(searcho)


def return_similar(list_one, list_two, threshold=90, limit=5):

	from fuzzywuzzy import fuzz
	from fuzzywuzzy import process
	dicto = {}

	sec = list_two.copy()

	inter = [x for x in list_one if x not in sec]

	for word in inter:

		result = process.extract(word, sec, limit=limit)
		result = [x for x in result if (x[1] >= threshold) and (x[0] != word)] 
		# print(word)  
		# print(result) 

		if len(result) > 0:
				result = result[0]
				dicto[word] = result[0]

	return dicto 

# python3 -m pip install --user --upgrade setuptools wheel
# python3 -m pip install --user --upgrade twine
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload dist/*