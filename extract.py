# This Python file uses the following encoding: utf-8
import fileinput
import re
import os
import untangle

"""
Das Programm dient dazu, aus den gegeben .a2-files die korrekten Entities auszulesen, diese in den xml-files zu suchen
und gleichzeitig ihre Dependencies zu bestimmen, sodass die Worte von denen sie abhängig sind, als Trigger-Worte abgespeichert werden können. 
Beispielsweise wird mit der File BTID-10084.a2 für die erste Gruppe das Wort 'invading' und die Dependency 'dobj' rausgefiltert, 
was der Regel entsprechen wird: wenn du das Wort 'invading' findest, ist das 'dobj' vermutlich eine gesuchte Entity. (Soweit die Idee zumindest)

Der anwendbare Teil aud die Test-files ist noch nicht geschrieben. 
"""

keywords = open("keywords.txt","a+")	# File, in die die regeln geschrieben werden. 
linestring = []							# Globale Variable, die den xml-file-input als einen fortlaufenden String enthält, um auch zeilenübergreifend mit Regex suchen zu können
boolean_found = False					# Boolean, für die Suche des Leitwortes in Wortgruppen
counter = 1
index_int = 1

for line in fileinput.input():
	
	file_name = os.path.splitext(fileinput.filename())[0]		#get the file_name without the extension to be able to look dependencies up in corresponding files

	habitatfound = re.search(r'T\d\sHabitat\s(\d{3})\s(\d{3})\s(.*)', line)		#finde alle gegebenen Trainigsentities
	
	
	if habitatfound:												#wenn du ein gefunden hast
		
		onset = habitatfound.group(1)
		offset = habitatfound.group(2)
		print onset
		print offset
		
		single_words = habitatfound.group(3).split()						#splitte es in einzelne Worte auf (für den Fall, dass Wortgruppen dabei sind)
		
		for word in single_words:
			dependencies_lookup = open(file_name + ".txt.xml")		#öffne die zugehörige xml-file (könnte man natürlich auch schon früher machen, um die Laufzeit zu verbessern)
			xml_untangled = untangle.parse(file_name + ".txt.xml")
			
			sentence_number = None 
			
			if linestring == []:									#mache aus der xml-file einen langen String
				for line in dependencies_lookup :
					linestring.append(line)
					joined= ' '.join(linestring)
			
			if counter == 1:
				find_index = re.search(r'<token id="(\d*)">\s*<word>' + re.escape(word) + '</word>\s*<lemma>(.*)</lemma>\s*<CharacterOffsetBegin>' + re.escape(onset) + '</CharacterOffsetBegin>', joined)
				print find_index
				index = find_index.group(1)
				index_int = int(find_index.group(1))
				lemma = find_index.group(2)
				print index
				print lemma
				counter += 1
				
			else: 
				index = str(index_int + counter - 1)
				print index
				lemma_find = re.search(r'<token id="' + re.escape(index) + '">\s*<word>' + re.escape(word) + '</word>\s*<lemma>(.*)</lemma>', joined)
				lemma = lemma_find.group(1)
				print index
				print lemma
				counter += 1
					
			
			
			habitat_dependency = re.search(r'<dep\stype="(.*)">\s*<governor\sidx="\d*">(.*)</governor>\s*<dependent\sidx="' + re.escape(index) + '">' + re.escape(word) + '</dependent>',joined)
			
			if habitat_dependency:						#suche nach einer Dependency, wo die gefundene Entity der Dependent ist und merke dir die Beziehung und den Governor
				
				for phrase_member in single_words:
					
					if habitat_dependency.group(2) == phrase_member:	#guck, ob der Governor Teil der Wortgruppe ist, wenn ja setze den Boolean auf True
						boolean_found = True
				
				if boolean_found == False:
					
					keywords.write(str(habitat_dependency.group(2)) + " + " + str(habitat_dependency.group(1)) + "\n")		#nur, wenn der Govenor kein Teil der Entitiy-Gruppe war, speichere es als Regel ab
																															
			boolean_found = False		# Boolean zurücksetzen
		counter = 1
	habitat = None		
	
keywords.close()		#File schließen

'''
1.Problem: 
Für Worte wie 'of', die häufiger im Text vorkommen, werden natürlich auch andere Dependencies gefunden. 
Man müsste also jede gefundene Entity aus den .a2-files genau spezifisch in den xml-files wiederfinden und sie mit ihrem idx-tag versehen. 
Dazu könnte man die angegebenen Grenzen aus der .a2-file nutzen, aber ich denke, es ginge auch anders.

2.Problem:
Bei Konjugationen wird als Govenor das andere Wort vor dem 'und' gefunden, was ja auch stimmt. Das ist nur keine gute Regel.
Man müsste spezifizieren, dass dabei geguckt wird, ob das erste Wort ebenfalls eine Entity ist, und wenn ja, welche Dependency dieses hat. 

Weiterer Gedanke: 
Es wäre vmtl. sinnvoll, Lemmas miteinzubeziehen, falls bestimmte Wortformen nicht in den Trainigsdateien waren. 
Allerdings muss man dann auch beachten, das einige Formen z.B. kein dobj haben können. 
'''