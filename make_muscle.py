#! /usr/bin/python3
#Code written by Ethan Deal

#Creates a list of muscle commands in a text to run for the alignments
#Arguments for the command line must look like this:
#python [file name] [list of file names]

#Variables
file_list = []
list_name = ''

list_name = sys.argv[1]

with open(list_name, 'r') as c:
	for line in c:
		data = line.replace('\n', '')
		file_list.append(data)

file = open('muscle_commands.txt', 'w')
for x in file_list:
	str = x + '.faa'
	file.write('muscle -in ' + str + ' -out ' + x + '.alg\n')
