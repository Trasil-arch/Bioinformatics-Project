#!/bin/bash
#Replace the list of the files you want with line 10
#Example: done < directory_wanted.list

counter=0
while read g;
do
	cp "$g" ./
	#counter=$((counter+1))

done < dir_found.list
