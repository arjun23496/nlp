import pickle
import nltk

def load_obj(name):
	with open('obj/' + name + '.pkl', 'rb') as f:
		return pickle.load(f)

debug = False

emission_prob = load_obj('emission')
transition_prob = load_obj('transition')

input_sentence = "I am running to catch the train"

words = nltk.word_tokenize(input_sentence)

prep = {}
presentp = {}
pred_tags = []

for x in range(0,len(words)):
	presentp = {}
	word = words[x].lower()
	# print "------------------",word
	found = False
	
	for y in emission_prob:
		try:
			emission_prob[y][word]
			
			# print "possible tag "+y

			if x == 0:
				presentp["0$$"+y] = emission_prob[y][word]
			else:
				maxi = ""
				maxp = 0
				trans = {}
				for z in prep:
					try:
						# zpre = ztag
						ztag = z.split('$$')
						ztag = ztag[len(ztag)-1]
						trans[z+"$$"+y] = prep[z]*transition_prob[ztag][y]*emission_prob[y][word]
						if trans[z+"$$"+y] > maxp:
							maxp = trans[z+"$$"+y]
							maxi = z+"$$"+y
					except KeyError:
						if debug:
							print ztag,":",y," transition not Found"
						pass
				
				presentp[maxi] = maxp
				# print "transition"
				# print trans

			found = True
		except KeyError:
			pass

	# print presentp
	# print "--------"
	prep = presentp
	# break

	if not found:
		print "Word not in Vocabulary"

maxi = ""
maxp = 0

for x in presentp:
	if presentp[x] > maxp:
		maxp = presentp[x]
		maxi = x

pred_tags = maxi.split('$$')
print "Probability of sentence: ",maxp

for x in range(0,len(words)):
	print words[x]," : ",pred_tags[x+1]