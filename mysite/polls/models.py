import re
import time
import csv
import os
from mysite.settings import BASE_DIR
# Create your models here.
def main():
	print(BASE_DIR)
	current_milli_time = lambda: int(round(time.time() * 1000))
	file_path = os.path.join(BASE_DIR, 'collection.tsv')
	reader = csv.reader(open(file_path), delimiter='\t')
	sortedlist = sorted(list(reader), key=lambda x:int(x[1]), reverse=True)
	collection = []
	for item in sortedlist:
		item[1] = int(item[1])
		item.append(''.join(sorted(item[0])))
		collection.append(item)
	start = current_milli_time()
	# a = fuzzyfinder('gretnss', collection)
	end = current_milli_time()
	print (end - start)
	return collection
	# print(a)
main()