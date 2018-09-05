# This Python file uses the following encoding: utf-8
import fileinput
import re
import os
import lxml
from lxml import etree

"""
This program is used to extract rules from annotated and parsed texts and to create a list of those rules. 
It does so in reading the correct entities from the annotation files (*.a2) and searching them in the corresponding parsing-file (*.xml). 
During this process it also recognizes the dependencies of this entity, so that their governor can then be marked as trigger word and written
into the rule-file "keywords.txt", additionally to the relation.
For example we find that for the first entity in file BTID-10084.a2 the governor 'invading' and the dependency 'dobj' is filtered out, 
which will then correspond to the rule: if you find the word 'invading', then its 'dobj' is probably one of the entities we are looking for.
"""

keywords = open("keywords.txt","a+")	# File, in which the rules are written. 
linestring = []							# xml-input as a string to allow for multiline-search
boolean_found = False					
counter = 1
index_int = 1
counter_tag = False						# keep track wether or not an apostrophy, hyphen or bracket was found which could throw of the index-counter


for line in fileinput.input():
	
	file_name = os.path.splitext(fileinput.filename())[0]		#get the file_name without the extension to be able to look dependencies up in corresponding files
	
	tree = etree.parse(file_name + ".txt.xml")					#create a tree-object of the xml-file, which will allow us
	root = tree.getroot()										# to only grab the enhanced-plus-plus-dependencies-subtree

	for dependencies in root.iter('dependencies'):							
		if dependencies.get('type') != 'enhanced-plus-plus-dependencies':
			dependencies.getparent().remove(dependencies)
	tree.write('output.xml')									# and save that stripped xml-file

	
	habitatfound = re.search(r'T\d*\sHabitat\s(\d{1,5})\s(\d{1,5})\s(.*)', line)		#find all given training-entities
	
		
	if habitatfound:									#if you find one:
		
		onset = habitatfound.group(1)					#start of the word(-group)		
		offset = habitatfound.group(2)					#end of the word(-group)
		
		single_words = habitatfound.group(3).split()			#split it into single words (in case there are entity-phrases)
		
		for word in single_words:								
				
			treenew = open('output.xml')						# open stripped xml-file
		
			#account for specialites such as hyphens, apostrophes, percentages and brackets
			
			if re.search(r'[(]\w+[\s-]\w+[)]',word):				
				word = re.search(r'(\w+[\s-]\w+)\W',word).group(1)
			
			elif re.search(r'\d+%',word):		
				word = re.search(r'\d+(%)',word).group(1)
				index = str(int(index) + 1)
				index_int = index_int + 1
								
			elif re.search(r'(\w+)[\']s', word):
				word = re.search(r'(\w+)[\']s',word).group(1)
				counter_tag = True
			
			elif re.search(r'\w+[-]\w+',word) == None :
				if re.search(r'[(-](\w+)', word):
					word = re.search(r'[(-]{0,1}(\w+)[-)]{0,1}', word).group(1)
					counter +=1
				elif re.search(r'(\w+)[-,)]', word):
					word = re.search(r'[-(]{0,1}(\w+)[-)]{0,1}', word).group(1)
					counter_tag = True					
				else: word = word
			
		
			if linestring == []:									#turn xml-file into a long string
				for line in treenew :
					linestring.append(line)
					joined= ' '.join(linestring)
						
			if counter == 1:						#find the first word and look for its index, its lemma 
				try: 
					find_index = re.search(r'<token id="(\d*)">\s*<word>' + re.escape(word) + '\S*</word>\s*<lemma>(.*)</lemma>\s*<CharacterOffsetBegin>' + re.escape(onset) + '</CharacterOffsetBegin>', joined)
					index = find_index.group(1)
					index_int = int(find_index.group(1))
					lemma = find_index.group(2)
				 
				except AttributeError:
					find_index = re.search(r'<token id="(\d*)">\s*<word>[\w*-]*' + re.escape(word) + '</word>\s*<lemma>(.*)</lemma>\s*<CharacterOffsetBegin>\d*</CharacterOffsetBegin>\s*<CharacterOffsetEnd>' + re.escape(offset) + '</CharacterOffsetEnd>', joined)
					index = find_index.group(1)
					index_int = int(find_index.group(1))
					lemma = find_index.group(2)
			
				counter += 1			
				if counter_tag == True:
					counter += 1
				counter_tag = False
				
			else:			# if its a phrase add one to the index and find the next word
				try:
					index = str(index_int + counter - 1)
					lemma_find = re.search(r'<token id="' + re.escape(index) + '">\s*<word>\w*[-]{0,1}' + re.escape(word) + '[.]*</word>\s*<lemma>(.*)</lemma>', joined)
					lemma = lemma_find.group(1)
				
				except AttributeError:
					try:
						lemma_find = re.search(r'<word>' + re.escape(word) + '</word>\s*<lemma>(.*)</lemma>\s*<CharacterOffsetBegin>\d*</CharacterOffsetBegin>\s*<CharacterOffsetEnd>' + re.escape(offset) + '</CharacterOffsetEnd>', joined)
						lemma = lemma_find.group(1)
						
					except AttributeError:
						counter += 1
						index = str(index_int + counter -1)
						lemma_find = re.search(r'<token id="' + re.escape(index) + '">\s*<word>\w*[-]{0,1}' + re.escape(word) + '</word>\s*<lemma>(.*)</lemma>', joined)
						lemma = lemma_find.group(1)
					
				counter += 1
				if counter_tag == True:
					counter += 1
				counter_tag = False	
				
			habitat_dependency = re.search(r'<dep\stype="(.*)">\s*<governor\sidx="\d*">(.*)</governor>\s*<dependent\sidx="' + re.escape(index) + '">' + re.escape(word) + '</dependent>',joined)
			
			if habitat_dependency:						#look for a relation where the found entity is a dependent and remember the dependency and the governor
				
				for phrase_member in single_words:
					
					if habitat_dependency.group(2) == phrase_member:	#look, if the governor is part of the phrase, if so turn boolean to true
						boolean_found = True
				
				if boolean_found == False:
					
					keywords.write(str(habitat_dependency.group(2)) + " + " + str(habitat_dependency.group(1)) + "\n")		#only, if the governor isn't part of the phrase write it as rule into the file "keywords.txt"
																															
			boolean_found = False		# reset variables
		counter = 1	

keywords.close()		#close file