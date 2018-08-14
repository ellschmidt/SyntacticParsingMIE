import fileinput
import re
import os


keywords = open("keywords.txt","a+")
linestring = []
boolean_found = False

for line in fileinput.input():
	
	global habitat
	habitat = None
	
	file_name = os.path.splitext(fileinput.filename())[0]		#get the file_name without the extension to be
	#print file_name												#able to look dependencies up in corresponding files

	habitatfound = re.search(r'T\d\sHabitat\s\d{3}\s\d{3}\s(.*)', line)
	
	if habitatfound:
		habitat = habitatfound
		
		single_words = habitat.group(1).split()
		print single_words
		
		for word in single_words:
			print "word: " + word
			dependencies_lookup = open(file_name + ".txt.xml")
			
			if linestring == []:
				for line in dependencies_lookup :
					linestring.append(line)
					joined= ' '.join(linestring)
			
			habitat_dependency = re.search(r'<dep\stype="(.*)">\s*<governor\sidx="\d*">(.*)</governor>\s*<dependent\sidx="\d*">' + re.escape(word) + '</dependent>',joined)
			if habitat_dependency:
				#print "Group 1 found: " + habitat_dependency.group(1)
				#print "Group 2 found: " + habitat_dependency.group(2)
				for phrase_member in single_words:
					#print "Phrase Memeber: " + phrase_member
					#print boolean_found
					if habitat_dependency.group(2) == phrase_member:
						boolean_found = True
				
				if boolean_found == False:
					print "Group 2: " + habitat_dependency.group(2)
					keywords.write(str(habitat_dependency.group(2)) + " + " + str(habitat_dependency.group(1)) + "\n")
			
			boolean_found = False
					
			
			#print habitat.group(1)
	
	habitat = None
	
keywords.close()