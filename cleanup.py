# This Python file uses the following encoding: utf-8
import os

###delete any doubles in the file:###

lines_seen = set() # holds lines already seen
keywrds_revised = open("keywrds_revised.txt", "a+")

for line in open("keywords.txt", "r"):
	if line not in lines_seen:
		keywrds_revised.write(line)
		lines_seen.add(line)
keywrds_revised.close()


os.remove("output.xml")		#removes temporary file 