from django.shortcuts import render
from . import models
import math
import re
collection = models.main()
WORDS = models.get_dict()
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
		response = suggest_with_corrections(user_input)[:24]
		# response = score_matches(user_input)
	else:
		response = (dict(msg= "No input priovided"))
	return HttpResponse(json.dumps(response), content_type="application/json")
	# return HttpResponse(json.dumps(response), content_type="application/json")

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
	return dict(suggestions=(priority + directs + suggestions)[:25])

def search_regex(user_input):
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

def suggest_with_corrections(user_input):
	match = []
	perfects = []
	good = []
	corrections = []
	for item in collection:
		if(len(good) + len(perfects) + len(match) == 25):
			break
		if item[0].startswith(user_input):
			if user_input == item[0]:
				match.append(item[0])
			else:
				perfects.append(item[0])
		elif user_input in item[0] and len(item[0]) >= len(user_input):
			good.append(item[0])
	corrections = list(candidates(user_input))
	good.sort(key = len)
	perfects.sort(key = len)
	corrections.sort(key = len)
	# print(corrections)
	return match + perfects + good + corrections

def score_matches(user_input):
	perfects = []
	good = []
	not_bad = []
	match = False
	for item in collection:
		# if item[0].startswith(user_input):
		# 	if user_input == item[0]:
		# 		match = True
		# 	good.append(item[0])
		# elif match and item[1] <= 2313585 and len(good) >= 10: # stop suggestions if it's rank is less than 0.1 
		# 	if user_input in good:
		# 		# good.remove(item[0])
		# 		perfects.append(item[0])
		# 		break
		# else:
		score = find_matches(user_input, item[0])
		if score <= 0.5:
			pass
		elif score == 1:
			perfects.append(item[0])
		elif score >= .75:
			good.append(item[0])
		else:
			not_bad.append(item[0])
	return dict(perfects=perfects, good=good, not_bad=not_bad)

def find_matches(user_input, target):
	splitter = math.ceil((25/100) * len(target))
	splits = [target[i:i+splitter] for i in range(0, len(target), splitter)]
	matches = 0
	for text in splits:
		if text in user_input:
			matches += 1
	if matches is 0:
		return 0
	else:
		return matches/len(target)

def words_to_ngrams(words, n, sep=""):
    return [sep.join(words[i:i+n]) for i in range(len(words)-n+1)]

# def P(word, N=sum(WORDS.values())): 
#     "Probability of `word`."
#     return WORDS[word] / N

# def correction(word): 
#     "Most probable spelling correction for word."
#     return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known(word) and known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
	"All edits that are one edit away from `word`."
	letters    = 'abcdefghijklmnopqrstuvwxyz'
	splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
	deletes    = [L + R[1:]               for L, R in splits if R]
	transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
	replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
	inserts    = [L + c + R               for L, R in splits for c in letters]
	return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))