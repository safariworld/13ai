#!/usr/bin/python
import sys
import numpy as np

lines = []
remove_reason = [0, 0]
remove_lines = 0

class user_session:
    def __init__(self):
        self.uiddict = {} 
        self.stats = []        # size is equal to uiddict
        self.timelists = []    # total size is equal to lines
        self.lidlists = []     # total size is equal to lines
        self.declists = []     # total size is equal to lines
        self.sessionlists = []

    def append(self, uid, time, dec, lid):
        if uid in self.uiddict:
            idx = self.uiddict[uid]
            self.timelists[idx].append(time)
            self.lidlists[idx].append(lid)
            self.declists[idx].append(dec)
        else :
            # save index of lists
            self.uiddict[uid] = len(self.timelists)

            timelist = [time]
            lidlist = [lid]
            declist = [dec]
            self.timelists.append(timelist)
            self.lidlists.append(lidlist)
            self.declists.append(declist)

    def calcStats(self):
        nuser = len(self.uiddict)

        for i in range(nuser):
            deltime = []
            hdeltime = []

            for j in range(len(self.timelists[i])-1):
                delt = self.timelists[i][j+1]-self.timelists[i][j]
                deltime.append(delt)
                if delt < 3600:
                    hdeltime.append(delt)

            if len(hdeltime) > 0:
                utime = np.array(hdeltime)
                self.stats.append([len(deltime), len(hdeltime), np.mean(utime)*3, np.amin(utime), np.amax(utime), np.median(utime)])

            else:
                self.stats.append(None)

            if i % 1000 == 0:
                print('Processed ' + str(i) + ' users')

        print('Length of uiddict is ' + str(len(self.uiddict)) + '\n')
        print('Length of stats is ' + str(len(self.stats)) + '\n')

    def genSession(self):
        for i in range(len(self.uiddict)):
            self.sessionlist = []

            for j in range(len(self.timelists[i])-1):
                delt = self.timelists[i][j+1]-self.timelists[i][j]

                if delt > 3600 or (delt > 60 and delt > self.stats[i][2]):
                    self.sessionlist.append(j)
#                    print('seperating delta is ' + str(delt))
#                    print('mean is ' + str(self.stats[i][2]))

            self.sessionlist.append(len(self.timelists[i])-1)
            self.sessionlists.append(self.sessionlist)

        print('Number of sessionlist is ' + str(len(self.sessionlists)))


    def getDecisionCount(self, uidx, sid, eid):
        pcnt = ncnt = 0  

        for i in range(eid-sid+1):
            if self.declists[uidx][i+sid] == 1:
                pcnt += 1
            else:
                ncnt += 1

        return [pcnt, ncnt]


    def removeLines(self, uidx, sid, eid):
        global remove_lines
        for i in range(eid-sid+1):
            lines[self.lidlists[uidx][i+sid]] = '-1\n'
            remove_lines += 1


    def removeSession(self):
        for i in range(len(self.uiddict)):
            sid = 0
            for j in range(len(self.sessionlists[i])):
                session = self.sessionlists[i][j]
                count = self.getDecisionCount(i, sid, session)

                remove = 0
                size = count[0]+count[1]

                if count[0] == 0:
                    remove_reason[0] += 1                                 
                    remove = 1
                elif count[0] / size > 0.9 and size > 10:
                    remove_reason[1] += 1                                 
                    remove = 1

                if remove == 1: 
                    # remove session
                    self.removeLines(i, sid, session)
                    self.sessionlists[i][j] = -1         

                sid = session + 1

    def analysis(self, souttxt):
        self.calcStats()
        self.genSession()

        self.removeSession()


if len(sys.argv) < 2 :
   print('Usage : ' + sys.argv[0] + ' data')
   sys.exit(0)

datatxt = open(sys.argv[1])

print('Reading ' + sys.argv[1])
count = 0

for line in datatxt.readlines() :
    lines.append(line)

    count += 1
    if count % 1000 == 0 :
        print('Read ' + str(count) + ' lines')

datatxt.close()

us = user_session()

count = 0
for line in lines:
    tmp = line.split()
    if len(tmp) > 3 :
        us.append(int(tmp[0]), int(tmp[3]), int(tmp[2]), count)
    else :
        print(tmp)

    count += 1
    if count % 1000 == 0 :
        print('Processed ' + str(count) + ' lines')

souttxt = open(sys.argv[1] + '.sa', 'w')

us.analysis(souttxt)

for line in lines:
    if line != '-1\n':
        souttxt.write(line)

souttxt.close()

print('remove reason is ' + str(remove_reason[0]) + ', ' + str(remove_reason[1]))
print('number of total removed lines is ' + str(remove_lines))
