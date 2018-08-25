# This Python file uses the following encoding: utf-8
import fileinput
import re
import os
import time
import lxml
from lxml import etree

start = time.time()
linestring = []	
counter = 1
rules = open("keywords_revised.txt", "r")
borders_end = 0
phrase_counter = 0
phrases_to_sort = [[]]
first = False
phrases_to_print = []

for line_a in fileinput.input():
	file_name = os.path.splitext(fileinput.filename())[0]

for line_b in rules:
	rule_tofind = re.search(r'(\w+[.]*|%)\s[+]\s(\w+\S*)', line_b)
	keyword = rule_tofind.group(1)
	relation = rule_tofind.group(2)
	#print "RULE: " + line
	
		

	
	tree = etree.parse(file_name + ".txt.xml")
	root = tree.getroot()

	for dependencies in root.iter('dependencies'):
		if dependencies.get('type') != 'enhanced-plus-plus-dependencies':
			dependencies.getparent().remove(dependencies)
	tree.write('output.xml')
	treenew = open('output.xml')
	
	if linestring == []:									#mache aus der xml-file einen langen String
		for line_c in treenew :
			linestring.append(line_c)
			joined= ' '.join(linestring)
					
					
	find_relation = re.findall(r'<dep type="' + re.escape(relation) + '">\s*<governor idx="\d*">' + re.escape(keyword) + '</governor>\s*<dependent idx="(\d*)">(.*)</dependent>', joined)
	phrase_list = []
	looked_up = []
	#print " find relation: ", find_relation
	for head in find_relation:
		phrase_list.append(head)
		for word in phrase_list:
			#print "phrase list: " , phrase_list
			#print "word: ", word
			
			try:
				find_phrase = re.findall(r'<governor idx="' + word[0] + '">' + word[1] + '</governor>\s*<dependent idx="(\d*)">(.*)</dependent>', joined)
				#print "find_phrase: ", find_phrase
				relative_clauses = re.search(r'who|\'\,\'|where|which', str(find_phrase))
				if relative_clauses:
					#print "found"
					sorted_for_delete = sorted(find_phrase, key=lambda is_this_comma: int(is_this_comma[0]))
					
					go_on = []
					for comma_search in sorted_for_delete:
						if comma_search[1] != ",":
							#print comma_search
							go_on.append(comma_search)
						else:
							break
						
					find_phrase = go_on	
				looked_up.append(word)
				#print "looked_up one: ", looked_up
				
				if find_phrase != []:
					for i in range(len(find_phrase)):
						phrase_list.append(find_phrase[i-1])
					
			
			except IndexError:
				continue	
		
		sorted_lookup = sorted(looked_up, key=lambda word: int(word[0]))
			
		entities = open("entities.a2", "a+")
		
		phrase = []
		for entity in sorted_lookup:
			if entity[1] in ["the", "from", "in", "-LRB-", "-RRB-"]: 
				continue
			elif entity[1] == "and":
				phrase_counter += 1
				phrases_to_sort.append([])
			else: 
				phrases_to_sort[phrase_counter].append(entity)
			
		for i in range(len(phrases_to_sort)):
			phrases_to_print.append([])
			#entities.write("T" + str(counter) + " Habitat ")
			phrases_to_print[counter-1].append(" Habitat ")
			for k in phrases_to_sort[i]:
				borders = re.search(r'<token id="' + re.escape(k[0]) + '">\s*<word>' + re.escape(k[1]) + '</word>\s*<lemma>.*</lemma>\s*<CharacterOffsetBegin>(\d+)</CharacterOffsetBegin>\s*<CharacterOffsetEnd>(\d+)</CharacterOffsetEnd>', joined)
				if first == False:
					borders_start = borders.group(1)
					#entities.write(borders_start + " ")
					phrases_to_print[counter-1].append(borders_start + " ")
					first = True
				if int(borders_end) < int(borders.group(2)):
						borders_end = borders.group(2)
						print borders_end
			
			#entities.write(borders_end + " ")
			phrases_to_print[counter-1].append(borders_end + " ")
			
			for k in phrases_to_sort[i]:
				#entities.write(k[1] + " ")
				phrases_to_print[counter-1].append(k[1] + " ")
			
			first = False
			borders_end = 0 
			border_start = 0
			
			#entities.write("\n")
			phrases_to_print[counter-1].append("\n")
			counter +=1
		phrases_to_sort = [[]]
		phrase_counter = 0
		#print "\n", sorted_lookup
		
		#print "SET" + "\n"
		phrase_list = []
		looked_up = []
	
	#print "\n" + "next rule" + "\n"	
	
sorted_phrases_back = sorted(phrases_to_print, key=lambda phrase: int(phrase[2]))
sorted_phrases = sorted(sorted_phrases_back, key=lambda phrase: int(phrase[1]))			
print sorted_phrases
t_counter = 1
for single_phrase in sorted_phrases:
	entities.write("T" + str(t_counter) + "\t")
	t_counter +=1
	for l in single_phrase:
		entities.write(l)
	
	
			
		