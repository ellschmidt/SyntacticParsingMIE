import fileinput
import re

linestring = []
for line in fileinput.input():
	linestring.append(line)
	
joined= ' '.join(linestring)
print joined
habitat_dependency = re.search(r'<governor\sidx=\"\d*\">(.*)</governor>\s*<dependent\sidx=\"(\d*)\">tract</dependent>', joined)
if habitat_dependency:
	print habitat_dependency.group(1)