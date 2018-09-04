import fileinput
import re
import os
import difflib
import math

correct_count = 0.0
recall_counter = 0.0
precision_counter = 0.0
predictions_counter = 0.0

for line_a in fileinput.input():
	file_name = os.path.splitext(fileinput.filename())[0]
	
original = open(file_name + " (2).a2", "r")

for line_origin in original:
	if re.search(r'OntoBiotope',line_origin):
		continue
	stripped_line_origin = line_origin.replace(re.search(r'(T\d*\s*)', line_origin).group(1),'')
	recall_counter += 1
	prediction = open(file_name + ".a2", "r")
	
	for line_pred in prediction:
		stripped_line_pred = line_pred.replace(re.search(r'(T\d*\s*)', line_pred).group(1),'')
		predictions_counter += 1

		if difflib.SequenceMatcher(None, stripped_line_origin, stripped_line_pred).ratio() >= 0.8:
			correct_count += 1

precision_counter = predictions_counter / recall_counter
recall = correct_count / recall_counter
print recall
precision = correct_count / precision_counter
print precision
f_one = 2*((precision*recall)/(precision+recall))
			
keeping_score = open("Scoretable.txt", "a")
keeping_score.write(file_name + "\t\t" + str(correct_count) + "\t\t" + str(round(recall,3)) + "\t\t" + str(round(precision,3)) + "\t\t" + str(round(f_one,3)) + "\n")