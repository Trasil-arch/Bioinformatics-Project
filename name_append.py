#! /usr/bin/python3
#Code written by Ethan Deal
#This script combines a unique list identified genomes from aligned files and
#updates the names of the genomes if there are more than one occurences of the
#names present
#Example: Desulfovibrio desulfuricans -> Desulfovibrio desulfuricans
#Output File - updated_name.list; *_u.faa.alg files(updated alignment files of
#files requesting name change)
#File does not currently ask for arguments; fill in file names at these lines:
#37 & 44 - Same file name; 94 - list you want changed

#Variables
#Dictionaries and Lists
pre_gca = {}
gca_name_file = {}
gca_name_update = {}
pre_name = {}
added_names_char = {}
name_filter = []
filenames = []
saved_lines = []
pre_line = {}

#Strings
updated_name = ''
amino = ''
seq = ''

#Replaces the last character with the next
def updateChar(char):
	ch = chr(ord(char) + 1)
	#print(ch)
	return(str(ch))

#For some reason does not grab the middle list number
#Still unknown but run this normally
with open('unique_num.gca.list','r') as u:
	for line in u:
		data = line.split('\t')
		gca_name_file.update({ data[0]:data[-1].replace('\n', '') })
		#print(data[0] + ' ' + data[-1])

#Grab the numbers and prefixes for the GCAs
with open('unique_num.gca.list', 'r') as g:
	for line in g:
		pre = ''
		gca = ''
		num = line.split('\t')
		counter = 0
		while (counter < len(num)):
			if counter == 0:
				gca = num[0]
			elif counter == 1:
				pre = num[1]
			counter += 1
		pre_gca.update({ pre:gca })

#Loop to cycle through and append the new characters
for (x, y) in gca_name_file.items():
	updated_name = ''
	#Has the file been updated already?
	if x not in gca_name_update.keys():
		#Has the name been changed yet?
		if y not in added_names_char.keys():
			added_names_char.update({ y:'a' })
			updated_name = y + ' ' + 'a'
			gca_name_update.update({ x:updated_name })
			name_filter.append(updated_name)
		#If the name has already been modified find it and append the new characters after
		if y in added_names_char.keys():
			for (nx, ny) in added_names_char.items():
				if y == nx:
					char = updateChar(ny)
					updated_name = y + ' ' + char
					added_names_char.update({ nx:char })
					gca_name_update.update({ x:updated_name })
					name_filter.append(updated_name)
					break

#Sort the list to keep it consistent
name_filter.sort()

file = open('updated_names.list', 'w')
#Write the overall name changed file with all the information
for (x, y) in gca_name_update.items():
	for (px, py) in pre_gca.items():
		if x == py:
			for (gx, gy) in gca_name_file.items():
				if x == gx:
					file.write(x + '\t' + px + '\t' + gy + '\t' + y + '\n')
file.close()

#Update the .alg files with the correct naming schemes
with open ('rib_alg.list', 'r') as r:
	for line in r:
		fixed = line.replace('\n', '')
		filenames.append(fixed)

#Read the file and pull out the lines and appendices

#Resetting some lists and dictionaries to hold some new information
#Holds parts of a section (will be made into a seperate class later on)
pre_amino = {}
pre_file = {}
before_pre = ''
ag_file = {}
ag_l = {}
ag_align = {}
ag_bool = False
ag_line = ''
ag_seq = ''
ag = ''
counterz = 0

for z in filenames:
	with open(z, 'r') as f:
		for line in f:
			if "Alpha" in line or "Gamma" in line:
				counterz += 1
				ag_file.update({counterz:z})
				ag_l.update({counterz:line})
				print(str(counterz) + ' ' + z + ' ' + line)
				if ag_seq != "":
					ag_align.update({(counterz-1):ag_seq})
					#ag_file_align.update({z:aq_seq})
					print(str((counterz-1)) + " " + z + " " + ag_seq)
				#print(z + ' ' + line)
				ag_seq = ""
				ag_bool = True
			elif ag_bool == True and line[0] != ">":
				ag = line.replace('\n', '')
				ag_seq += ag
			elif line[0] == ">":
				ag_bool = False
				pre_amino.update({ before_pre:seq })
				#print(before_pre + ' ' + seq)
				seq = ''
				data = line.split(' ')
				saved_lines.append(line)
				before_pre = data[0].replace('>', '')
				pre_line.update({ before_pre:line })
				filen = z.split('.')
				pre_file.update({ before_pre:filen[0] })
				#print(filen[0])
			else:
				amino = line.replace('\n', '')
				seq += amino


#Update the files now
for z in filenames:
	filen = z.split('.')
	fx = filen[0] + '_u.faa.alg'
	file = open(fx, 'w')
	print(fx)
	#print("I'm starting")
	for (x,y) in pre_file.items():
		if y == filen[0]:
			#print('Here 1')
			for (lx, ly) in pre_line.items():
				if lx == x:
					#print('Here 2')
					for (ax, ay) in pre_amino.items():
						if ax == x:
							#print('Here 3')
							for (gx, gy) in pre_gca.items():
								if gx == x:
									#print('Here 4')
									for (ux, uy) in gca_name_update.items():
										if gy == ux:
											#replaced = ly.split('[')
											replace = uy.replace(' ', '_')
											file.write('>' + replace + '\n')
											file.write(ay + '\n')
											#print(replaced[0] + '[' + uy + ']')
											#print(ay)

	#Print updated files here
	for (f,a) in ag_file.items():
		if a == z:
			print(str(f) + ' ' + z)
			for (g,k) in ag_align.items():
				if f == g:
					print(str(f) + ' ' + z + ' ' + k)
					for (c,v) in ag_l.items():
						if c == f:
							print(str(c) + ' ' + z + ' ' + v)
							file.write(v)
							file.write(k + '\n')
