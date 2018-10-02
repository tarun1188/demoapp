from django.shortcuts import render
from . import models
import re
collection = models.main()
import json
# Create your views here.
from django.http import HttpResponse

def index(request):
	return HttpResponse(200)

def search(request):
	user_input = request.GET.get('word')
	print(user_input)
	if user_input is not None:
		user_input = str(user_input).lower()
		response = lets_do_it(user_input)
	else:
		response = (dict(msg= "No input priovided"))
	return HttpResponse(json.dumps(response), content_type="application/json")

def do_search(user_input):
	# suggestions = []
	priority = []
	directs = []
	suggestions = []
	# pattern = '.*?'.join(user_input)
	# regex = re.compile(pattern)
	match = False
	for item in collection:
		if item[0].startswith(user_input):
			if user_input == item[0]:
				match = True
			directs.append(item[0])
		elif match and item[1] <= 2313585 and len(directs) >= 10: # stop suggestions if it's rank is less than 0.1 
			if user_input in directs:
				directs.remove(user_input)
				priority.append(user_input)
				break
		# elif user_input in item[0]:
		# 	suggestions.append(item[0])
		elif abs(len(user_input) - len(item[0])) <= 2:
			min_match = round(len(user_input)/ 4)
			if user_input[0:min_match] == item[0][0:min_match] and user_input[-min_match:] == item[0][-min_match:]:
				suggestions.append(item[0])
			if len(directs) + len(suggestions) == 25:
				break
			# misses = 0
			# index = 0
			# modified_input = ""
			# for char in user_input:
			# 	if char != item[0][index]:
			# 		misses += 1
			# 	else:
			# 		modified_input += char
			# 	index += 1
			# print(modified_input)
			# if modified_input == user_input and misses >= 3:
			# 	suggestions.append(item[0])

	directs.sort(key = len)
	# suggestions.sort(key = len)
	return dict(suggestions=(priority + directs + suggestions)[:25])

def search_regx(user_input):
	suggestions = []
	priority = []
	directs = []
	pattern = '.*?'.join(user_input)
	regex = re.compile(pattern)
	match = False
	for item in collection:
		if item[0].startswith(user_input):
			if user_input == item[0]:
				match = True
			directs.append(item[0])
		elif match and item[1] <= 2313585 and len(directs) >= 10:
			if user_input in directs:
				directs.remove(user_input)
				priority.append(user_input)
			break
		elif user_input[0:2] == item[0][0:2] or user_input[-2:] == item[0][-2:]:
			match = regex.search(item[0])
			if match:
				suggestions.append(item[0])	
	directs.sort(key = len)
	suggestions.sort()
	return dict(suggestions=(priority + directs + suggestions)[:25])

def lets_do_it(user_input):
	for item in collection:
		find_matches(user_input, item)
		
		# for char in user_input:
		# 	if char in item[0]:
		# 		pass
	return dict(ok="no")


def find_matches(source, target):
	pass
	

def words_to_ngrams(words, n, sep=""):
    return [sep.join(words[i:i+n]) for i in range(len(words)-n+1)]


# main()