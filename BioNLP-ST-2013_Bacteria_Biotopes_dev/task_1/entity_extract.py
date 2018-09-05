# This Python file uses the following encoding: utf-8
import fileinput
import re
import os
import time
import lxml
from lxml import etree

"""
This programs purpose is to extract entities from parsed texts on the basis of a given set of rules and write them sortedly
into an *.a2 file.
It is called with a *.txt file and later on opens the corresponding .xml-file in the same directory
"""

start = time.time()
linestring = []	
linestring_sentence = []
counter = 1
rules = open("keywords_revised_deleted_out.txt", "r")		#open the given rule-book
borders_end = 0
phrase_counter = 0
phrases_to_sort = [[]]
first = False
phrases_to_print = []

for line_a in fileinput.input():
	file_name = os.path.splitext(fileinput.filename())[0]		#get file-name without file-type extension

for line_b in rules:
	rule_tofind = re.search(r'(\w+[.]*|%)\s[+]\s(\w+\S*)', line_b)	#for every line in the rule book read out the dependency relation and the keyword
	keyword = rule_tofind.group(1)
	relation = rule_tofind.group(2)
	#print line_b
	tree = etree.parse(file_name + ".txt.xml")						#make the .xml-file an object so as to enable deleting out all
	root = tree.getroot()											#dependencies except the enhanced-plus-plus-dependencies

	for dependencies in root.iter('dependencies'):
		if dependencies.get('type') != 'enhanced-plus-plus-dependencies':
			dependencies.getparent().remove(dependencies)
	tree.write('output.xml')
	treenew = open('output.xml')									#write the stripped tree into a new file
	
	if linestring == []:									#turn it into on long string 
		for line_c in treenew :
			linestring.append(line_c)
			joined= ' '.join(linestring)
					
	
	find_relation = re.findall(r'<dep type="' + re.escape(relation) + '">\s*<governor idx="\d*">' + re.escape(keyword) + '</governor>\s*<dependent idx="(\d*)">(.*?)</dependent>.*?<sentence id="(\d*)">', joined, flags=re.DOTALL)
						#find every word where the keyword is the governor and stands in the rule-given relation to this word
						#output is a list of lists which in turn contain the words index, the word, and the sentence index of the next sentence
	
	
	
	#print find_relation
	phrase_list = []			
	looked_up = []					
	#print "\nSET\n" 
	for head in find_relation:		#find all dependency-subtrees of the found word, which the is the head of those subtrees
		phrase_list.append(head)
		
		#print "HEAD: " 
		#print head
		tree = etree.parse("output.xml")						#make the .xml-file an object so as to enable deleting out all
		root = tree.getroot()
		for sentence in root.iter('sentence'):
		#		print "index" + head[2]
		#		print str(int(head[2])-1)
		#		print sentence.get('id')
				if sentence.get('id') != str(int(head[2])-1):
					sentence.getparent().remove(sentence)
		tree.write('sentence.xml')
		tree_sentence = open('sentence.xml')									#write the stripped tree into a new file
	
									#turn it into on long string 
		for line_d in tree_sentence :
			linestring_sentence.append(line_d)
			joined_sentence= ' '.join(linestring_sentence)
			
		
		for word in phrase_list:
			
			
			
			try:
				find_phrase = re.findall(r'<governor idx="' + word[0] + '">' + word[1] + '</governor>\s*<dependent idx="(\d*)">(.*?)</dependent>', joined_sentence)
				# find every word, and its index, where the head is the governor
				#print find_phrase
				relative_clauses = re.search(r'who|\'\,\'|where|which|that', str(find_phrase)) #trigger for relative-clauses, which will be deleted out  , .*?<sentence id="' + word[2]+ '">  flags=re.DOTALL
				if relative_clauses:
					sorted_for_delete = sorted(find_phrase, key=lambda is_this_comma: int(is_this_comma[0]))
	
					go_on = []
					for comma_search in sorted_for_delete:
						if comma_search[1] in (",","who","where","which","that"):
							break
						else:
							go_on.append(comma_search)
						
					find_phrase = go_on	
				
				looked_up.append(word) #keep track of every word that was already searched for subtrees
				#print "looked up: "
				#print looked_up
				if find_phrase != []:
					for i in range(len(find_phrase)):
						phrase_list.append(find_phrase[i-1])	#append the found words to also find their subtrees			
		
			except IndexError:		#if nothing is found there is no subtree. continue with the next word
				continue	
			
		linestring_sentence = []
			
		sorted_lookup = sorted(looked_up, key=lambda word: int(word[0])) #sort the whole subtree by word-index to get the word-phrase
		
		entities = open(file_name + ".a2", "a+")
		
		phrase = []
		
		#instead of writing the found phrase directly into the output file, we collect every phrase that was found in the text to
		#sort them by onset in the text first
		#a list of lists is used, where every list will contain a line to be printed in the output-file
		
		for entity in sorted_lookup:
			if entity[1] in ["the", "from", "in", "-LRB-", "-RRB-", "a"]: 	#delete articles, brackets and prepositions
				continue
			elif entity[1] == "and":		#if there is a conjunction open up a new list
				phrase_counter += 1
				phrases_to_sort.append([])
			else: 
				phrases_to_sort[phrase_counter].append(entity)	#add word into list
		
		#phrases_to_sort is just the mere collection of all the found word phrases in the text
		#phrases_to_print integrates the phrases in the necessary format of the lines in the output file
		#print joined_sentence
		for i in range(len(phrases_to_sort)):
			phrases_to_print.append([])
			phrases_to_print[counter-1].append("Habitat ")		#start the line with "Habitat"
			
			for k in phrases_to_sort[i]:	#for every word in the phrase find out its on- and offset
				#print k
				borders = re.search(r'<token id="' + re.escape(k[0]) + '">\s*<word>' + re.escape(k[1]) + '</word>\s*<lemma>.*</lemma>\s*<CharacterOffsetBegin>(\d+)</CharacterOffsetBegin>\s*<CharacterOffsetEnd>(\d+)</CharacterOffsetEnd>', joined_sentence)
				if first == False:
					borders_start = borders.group(1)	
					phrases_to_print[counter-1].append(borders_start + " ")		#add to the line the onset of the first word
					first = True
				if int(borders_end) < int(borders.group(2)):
						borders_end = borders.group(2)			#update the offset until the last word

			phrases_to_print[counter-1].append(borders_end + "\t")	#add to the line the offset of the last word
			
			first_word_seen = False
			for k in phrases_to_sort[i]:
				if first_word_seen == True:
					phrases_to_print[counter-1].append(" " + k[1])	#finally add to the line the phrase of words
				else: 
					phrases_to_print[counter-1].append(k[1])
					first_word_seen = True
					
			phrases_to_print[counter-1].append("\n")	#also add a newline
			
			first = False			#reset variables
			borders_end = 0 
			border_start = 0
			counter +=1
			
		phrases_to_sort = [[]]
		phrase_counter = 0
		phrase_list = []
		looked_up = []
	
sorted_phrases_back = sorted(phrases_to_print, key=lambda phrase: int(phrase[2]))	#sort all the lines by offset
sorted_phrases = sorted(sorted_phrases_back, key=lambda phrase: int(phrase[1]))		#sort all the lines by onset

t_counter = 1
for single_phrase in sorted_phrases:				#for every line write a "T" and a counting up number behind and then the line
	entities.write("T" + str(t_counter) + "\t")
	t_counter +=1
	for l in single_phrase:
		entities.write(l)							#into the output-file