#!/usr/bin/python
import sys
import numpy as np

lines = []
cur_duration = {}
prev_duration = {}
next_duration = {}
num_visit = {}


class user_session:
    def __init__(self):
        self.uiddict = {} 
        self.stats = []        # size is equal to uiddict
        self.timelists = []    # total size is equal to lines
        self.lidlists = []     # total size is equal to lines
        self.sessionlists = []
        

    def append(self, uid, time, lid):
        if uid in self.uiddict:
            idx = self.uiddict[uid]
            self.timelists[idx].append(time)
            self.lidlists[idx].append(lid)
        else :
            # save index of lists
            self.uiddict[uid] = len(self.timelists)

            timelist = [time]
            lidlist = [lid]
            self.timelists.append(timelist)
            self.lidlists.append(lidlist)


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


    def genSessionInfo(self):
        for i in range(len(self.uiddict)):
            lent = len(self.timelists[i])

            session = []
            prev_session = []
            prev_delt = 0

            # this list is for visit analysis
            sessionlist = []

            for j in range(lent-1):
                
                delt = self.timelists[i][j+1] - self.timelists[i][j]
                session.append(j)

                if delt > 0 :
                    for k in session: 
                        cur_duration[self.lidlists[i][k]] = delt
                        prev_duration[self.lidlists[i][k]] = prev_delt

                    for k in prev_session:
                        next_duration[self.lidlists[i][k]] = delt

                    prev_session = session
                    session = []
                    prev_delt = delt

                # for visit analysis
                if delt > 3600 or (delt > 60 and delt > self.stats[i][2]):
                    sessionlist.append(j)

            # append the last session
            session.append(lent-1)
            for k in session: 
                cur_duration[self.lidlists[i][k]] = 0
                prev_duration[self.lidlists[i][k]] = prev_delt
                next_duration[self.lidlists[i][k]] = 0
                    
            for k in prev_session:
                next_duration[self.lidlists[i][k]] = 0

            # for visit analysis
            sessionlist.append(len(self.timelists[i])-1)
            self.sessionlists.append(sessionlist)

            if i % 1000 == 0:
                print('Processed ' + str(i) + ' users')


    def visitAnalysis(self):
        for i in range(len(self.uiddict)):
            sid = 0
            for visit in self.sessionlists[i]:
                length = visit-sid+1
                for j in range(length):
                    num_visit[self.lidlists[i][j+sid]] = length
            sid = visit+1


    def analysis(self):
        self.calcStats()
        self.genSessionInfo()
        self.visitAnalysis()


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
        us.append(int(tmp[0]), int(tmp[3]), count)
    else :
        print(tmp)

    count += 1
    if count % 1000 == 0 :
        print('Processed ' + str(count) + ' lines')

souttxt = open(sys.argv[1] + '.sa', 'w')

us.analysis()

count = 0
for line in lines:
    tmp = line.split()
    if len(tmp) > 3:
        souttxt.write(tmp[0] + '\t' + tmp[1] + '\t' +  tmp[2] + '\t' +  str(cur_duration[count]) + '\t'  +  str(prev_duration[count]) + '\t' +  str(next_duration[count]) + '\t' + str(num_visit[count]) + '\n')

    count += 1
    if count % 1000 == 0 :
        print('Writing ' + str(count) + ' lines')

souttxt.close()

