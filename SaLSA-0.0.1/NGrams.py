"""
NGrams
 - infoElem - one InfoBase object
 - ngrams{syn} = [list of n-grams]
 - score{syn} = 3-gram-sum 
"""

from collections import defaultdict
import os
import re
import commands

class NGrams:
	def __init__(self, infoElem):
		self.infoElem = infoElem
		self.ngrams = defaultdict(dict)
		self.scores = defaultdict(dict)

	def sanitizeGrammar(self):
		""" 
		For now, sanitize a/an
		"""
		vowel = re.compile(r'^(a|e|i|o|u)')
		a = re.compile(r'\ba\b')
		an = re.compile(r'\ban\b')
		if vowel.search(self.infoElem.head):
			# Search all n-grams
			for ngID in self.ngrams.keys():
				for ngSyn in self.ngrams[ngID].keys():
					ngs = self.ngrams[ngID][ngSyn]
					for i in range(0, len(ngs)):
								currNg = ngs[i]
								if an.search(currNg) and not vowel.search(ngSyn):
									currNg = re.sub(r'\ban\b', r'a', currNg)
									ngs[i] = currNg
					self.ngrams[ngID][ngSyn] = ngs

		else:
			# So the head starts with a consonent
			for ngID in self.ngrams.keys():
				for ngSyn in self.ngrams[ngID].keys():
					ngs = self.ngrams[ngID][ngSyn]
					for i in range(0, len(ngs)):
								currNg = ngs[i]
								if a.search(currNg) and vowel.search(ngSyn):
									currNg = re.sub(r'\ba\b', r'an', currNg)
									ngs[i] = currNg
					self.ngrams[ngID][ngSyn] = ngs
			
					 
		

	def constructNGrams(self):
		ID = self.infoElem.sentenceID
		sentence = self.infoElem.sentence
		position = self.infoElem.positionOfHead
		synonyms = self.infoElem.synonyms
		inflections = self.infoElem.inflections
		pos = self.infoElem.headPos

		sentFrags = sentence.split(' ')

		for syn in synonyms:
			self.ngrams[ID][syn] = []
			if inflections.has_key(syn):
				infl = inflections[syn].split(';')
				infl.pop() # Last element empty

				if position - 2 >= 0:
					# Add syn AND inflections
					self.ngrams[ID][syn].append(sentFrags[position-2] + ' ' + sentFrags[position-1] + ' ' + syn)
					for inf in infl:
						self.ngrams[ID][syn].append(sentFrags[position-2] + ' ' + sentFrags[position-1] + ' ' + inf)

				if position + 1 <= len(sentFrags) - 1:
					self.ngrams[ID][syn].append(sentFrags[position-1] + ' ' + syn + ' ' + sentFrags[position+1])
					for inf in infl:
						self.ngrams[ID][syn].append(sentFrags[position-1] + ' ' + inf + ' ' + sentFrags[position+1])

				if position + 2 <= len(sentFrags) - 1:
					self.ngrams[ID][syn].append(syn + ' ' + sentFrags[position+1] + ' ' + sentFrags[position+2])
					for inf in infl:
						self.ngrams[ID][syn].append(inf + ' ' + sentFrags[position+1] + ' ' + sentFrags[position+2])
			else:
				# No inflections, add the basic form
				if position - 2 >= 0:
					self.ngrams[ID][syn].append(sentFrags[position-2] + ' ' + sentFrags[position-1] + ' ' + syn)

				if position + 1 <= len(sentFrags) - 1:
					self.ngrams[ID][syn].append(sentFrags[position-1] + ' ' + syn + ' ' + sentFrags[position+1])

				if position + 2 <= len(sentFrags) - 1:
					self.ngrams[ID][syn].append(syn + ' ' + sentFrags[position+1] + ' ' + sentFrags[position+2])
		
					
	def getCounts(self):
		ID = self.infoElem.sentenceID
		synonyms = self.infoElem.synonyms
		
		self.scores[ID] = {}
		for syn in synonyms:
			# The best place to remove hyphens
			re.sub(r'-', ' ', syn)
			ngrams = self.ngrams[ID][syn]
			self.scores[ID][syn] = 0
			for ngram in ngrams:
				output = commands.getstatusoutput('perl salsaApp.pl "NG english ' + ngram + '"')
				score = output[1].split(' ')[-1]
				self.scores[ID][syn] += int(score)

					
						
			
			
			
	
