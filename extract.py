import fileinput
import re


for line in fileinput.input():
	global habitat
	habitat = None
	habitatfound = re.search(r'T. Habitat ... ... (.*)')
	
	print habitatfound
	
	if habitatfound:
		habitat = habitatfound
		print habitat.group(1)
	
	habitat = None