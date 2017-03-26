from __future__ import division
from sets import Set

import re
import nltk
import sys
import collections
import pickle

reload(sys)  
sys.setdefaultencoding('utf8')

def save_obj(obj, name ):
	with open('obj/'+ name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


text = []
corpus = ''

with open('data/hob.txt') as f:
	for x in f:
		corpus = corpus+x
		# l = nltk.word_tokenize(x)
		# tags=nltk.pos_tag(l)
		# print tags

print "sentence tokenizer"
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
sentence = sent_detector.tokenize(corpus)

print "Create HMM using MLE"

emission = {}
transition = {}

for x in sentence:
	words = nltk.word_tokenize(x)
	if len(words) > 2:
		tags = nltk.pos_tag(words)
		# print tags

		for y in range(0, len(tags)):			
		
			# tags[y][0] = re.sub(r'[^\x00-\x7F]+','', tags[y][0])

			word = tags[y][0]
			word = re.sub(r'[^\x00-\x7F]+','', word)
			word = word.lower()

			try:
				emission[tags[y][1]]
			except KeyError:
				emission[tags[y][1]] = {}
				transition[tags[y][1]] = {}
			try:
				emission[tags[y][1]][word]+=1
			except KeyError:
				emission[tags[y][1]][word] = 1

			# emission[tags[y][1]][tags[y][0]]+=1

			if y+1 < len(tags):
				trans = tags[y+1][1]
			else:
				tran = '0'

			try:
				transition[tags[y][1]][trans]+=1
			except KeyError:
				transition[tags[y][1]][trans]=1


# print emission['NN']
# print "---------------------------"
# print transition

emission_prob = {}
transition_prob = {}

print "Computing Emission and Transition Probabilities"

for x in emission:
	# print emission_prob

	emission_prob[x]={}
	tot = 0
	for y in emission[x]:
		tot += emission[x][y]

	for y in emission[x]:
		emission_prob[x][y] = emission[x][y]/tot


for x in transition:
	transition_prob[x]={}
	tot = 0
	for y in transition[x]:
		tot += transition[x][y]

	for y in transition[x]:
		transition_prob[x][y] = transition[x][y]/tot

# print emission_prob
# print "---------------"
# print transition_prob

print "Saving..."

save_obj(emission_prob,'emission')
save_obj(transition_prob,'transition')