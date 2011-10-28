# Standalone LexSub
# Ravi S Sinha
# University of North Texas
# Summer 2011

# Class definition
import re

class TextBase:
	def __init__(self, rawTextFile):
		tempFH = open(rawTextFile, "r")
		tempStr = ""
		for line in tempFH:
			tempStr += line.strip() + " "
		self.raw = tempStr
		self.text = []

	def preprocess(self):
		flag = True
		self.text = self.raw.split('.')
		self.text.pop() # Get rid of the last element which is empty by default
		for line in self.text:
			# print line # Tested
			if "<head>" not in line or "</head>" not in line:
				flag = False
			# print flag # Tested
			# Enforcing no spaces between <head>, word and </head>
			if re.search(r'<head>\s+', line) or re.search(r'\s+</head>', line):
				flag = False	

		if not flag:
			print "Error: you did not specify <head> and </head> tags or there are extra spaces in the lines . . ."
			import sys
			sys.exit()

	def displayText(self):
		for line in self.text:
			print line



