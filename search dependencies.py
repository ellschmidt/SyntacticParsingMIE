import fileinput
import re

for line in fileinput.input():
	habitat_dependency = re.search(r'<dep\stype="(.*)">\n\s*<governor\sidx="\d*">(.*)</governor>\n\s*<dependent\sidx="\d*">' + tract + '</dependent>',line)
	print habitat_dependency.group(1)