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

for line in fileinput.input():
	file_name = os.path.splitext(fileinput.filename())[0]

for line in rules:
	rule_tofind = re.search(r'(\w+[.]*|%)\s[+]\s(\w+\S*)', line)
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
		for line in treenew :
			linestring.append(line)
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
			
		entities = open("entities.txt", "a+")
		entities.write("T" + str(counter) + " Habitat ")
		for entity in sorted_lookup:
			entities.write(entity[1] + " ")
		
		entities.write("\n")
		counter += 1
		#print "\n", sorted_lookup
		
		#print "SET" + "\n"
		phrase_list = []
		looked_up = []
	
	#print "\n" + "next rule" + "\n"		
	#counter += 1
	
	
			
			
			
			
			
			
		