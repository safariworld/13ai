#!/usr/bin/python
import sys

if len(sys.argv) < 2 :
   print('Usage : ' + sys.argv[0] + ' data');
   sys.exit(0)

tid = {} 

#read target_users_id.txt
tidtxt = open('target_users_id.txt')
for line in tidtxt.readlines() :
    tid[int(line)] = 1

datatxt = open(sys.argv[1])
outptxt = open(sys.argv[1] + '.out', 'w')

count = 0

for line in datatxt.readlines() :
    tmp = line.split()
    count += 1

    if int(tmp[0]) in tid :
        outptxt.write(line)

    if count % 1000 == 0 :
        print('Processed ' + str(count) + ' lines')
        outptxt.flush()

 
