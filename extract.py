import fileinput
import re
import os


extractions = open("a2_habitats.txt","w")
linestring = []

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
			print word
			dependencies_lookup = open(file_name + ".txt.xml")
			
			for line in dependencies_lookup :
				linestring.append(line)
				joined= ' '.join(linestring)
				habitat_dependency = re.search(r'<dep\stype="(.*)">\s*<governor\sidx="\d*">(.*)</governor>\s*<dependent\sidx="\d*">' + re.escape(word) + '</dependent>',joined)
				if habitat_dependency:
					print habitat_dependency.group(1)
					print habitat_dependency.group(2)
					
		extractions.write(str(habitat.group(1)) + "\n")
		#print habitat.group(1)
	
	habitat = None
	
extractions.close()