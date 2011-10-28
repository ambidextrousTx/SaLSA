StandAlone Lexical Substitution Analyzer (SaLSA)
v 0.0.1
October, 2011

Ravi Sinha
Language and Information Technologies
University Of North Texas
Fall 2011

License
-------
This software is provided under the BSD license for research purposes. Refer to the file LICENSE.txt for details.

Information
-----------
SaLSA (StandAlone Lexical Substitution Analyzer) is a standalone application for filtering out irrelevant synonyms and keeping in relevant synonyms in a lexical substitution setting. In particular, the input and output are as follows -

INPUT: a text file with sentences separated by the dot ('.'), and with each sentence having one word marked as the target (head) word like so -

The sun was shining <head>brightly</head>. This is a thin photographic <head>film</head>.

The head words can be inflected, and SaLSA will lemmatize it for you. You can have multiple sentences on the same line separared by the dot, or one sentence on each line. 

OUTPUT: a reverse-ranked list of candidate substitutes along with their n-gram scores, along with detailed output showing all n-grams, all inflections, all synonyms, and their final scores, for each input sentence (each ID).

Requirements
------------
SaLSA has the following requirements -
[1] NLTK - the Natural Language ToolKit is a Python module that incorporates some off-the-shelf basic NLP tools such as a part-of-speech tagger and a lemmatizer that SaLSA uses. If you do not want to use NLTK, you will have to replace the corresponding lines in the code with your own toolchain that tags and lemmatizes text.

When in doubt, just do (on Ubuntu)

$ sudo apt-get install python-nltk python-numpy

This should install NLTK on you. 

NOTE: You might need to do the following to get the tagger and lemmatizer to work within NLTK -
$ python
>> import nltk
>> nltk.download()

And then choose 'all packages' in the window that pops up.

Again, if you do not wish to use NLTK, then the following will need to be changed in SaLSA -
[a] method posTag in file InfoBase.py - change so it returns a list of tuples, where each tuple is a word and its part of speech (compatible with the format that NLTK's recommended tagger uses by default)
[b] method lemmatize in file InfoBase.py - change it to return a single string, which is the lemmatized form

[2] UNTIndexer - the n-gram indexer from the University of North Texas, which, once the index is built, returns n-gram counts in constant time. If you do not wish to use UNTIndexer, you will have to change the corresponding parts in SaLSA with something that has the same functionality.

In particular, you will need to change the following -
[a] files salsaApp.pl and nGramModule.pl will become useless
[b] method getCounts in file NGrams.py - change it so the variable 'output' gets the count for the 3-gram you are interested in

Composition
-----------
SaLSA has the following elements -
[1] salsa.py - The entry point that you run from a shell 
[2] TextBase.py - The TextBase class handles the input file
[3] InfoBase.py	- The InfoBase class represents the input data as well as data derived during the processing, e.g. the parts of speech, the synonyms and inflections
[4] salsaApp.pl - A Perl script that calls UNTIndexer and gathers n-gram counts
[5] synonyms.db - A Python persistent object containing all the synonyms from WordNet and Microsoft Encarta for all the words that we propose SaLSA will cover
[6] inflections.db - A Python persistent object containing inflections for all the synonyms to be covered
[7] nGramModule.pl - Module that handles making n-gram queries to the server

You are encouraged to participate and beta-test SaLSA, which is currently in its version number 0.0.1 

Configuration
-------------
[1] Fill in the host name of the machine that is hosting your n-gram server, in the file salsaApp.pl
[2] Create a plain text file with sentences and headwords as outlined above

SaLSA takes, on the command line, one argument, which is the name of the file it is going to process. So in a terminal, an invocation will look like this -
$ python salsa.py sample.txt

Where the sample.txt file contains sentences and headwords as outlined above.

Provided you have the n-gram server and NLTK properly set up, this should run and return a detailed output that you can leverage/ modify the way you want.

Features
--------
v 0.0.1
- inflections.db has inflections for adverbs as well, even though they might not necessarily be legal terms in standard English
- SaLSA has a method that sanitizes grammar, to make sure whether an article (if present) should be 'a' or 'an' in a particular n-gram. For example, 
INPUT: She was a <head>smart<head> student.
Generated n-grams (some of them) - 
	- was a brilliant
	- a brilliant student
	- was an intelligent
	- an intelligent student

- head words are lemmatized if you provide an inflected form in the input
- tested on a virtual machine (Ubuntu)
- currently, SaLSA only looks at 3-grams and adds up counts for all possible 3-grams generated using a particular synonym

To Do
-----
- Add unit tests to make sure that progressively adding new features to the codebase doesn't break the older features

Contact
-------
Forward all questions, comments and bug-reports to the following address-
ravi DOT sinha AT my DOT unt DOT edu


