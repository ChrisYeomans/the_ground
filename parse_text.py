import sys

name = input("Name to search for: ")
filename = input("Filename of text: ")
cntr = 0

with open(filename+".txt", 'rb') as f:
	inp = f.readlines()

	for line in inp:
		for word in str(line).split():
			#sys.stderr.write(word+'\n')
			if word.lower() == name.lower():
				cntr += 1
				sys.stderr.write("Occurence\n")

print("Counter is: " + str(cntr))