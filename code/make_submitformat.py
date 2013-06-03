#Author: Seung-hwan Baek
#This code will parse the output of libFM into KDD2012 cup format.
import sys

print len(sys.argv)

print("reading libFM output file: %s..."%(sys.argv[1]))
outf = open(sys.argv[1], "r")
probs = outf.readlines()

print("reading test file: %s..."%(sys.argv[2]))
datf = open(sys.argv[2], "r")
dats = datf.readlines()

print("result filename:%s"%(sys.argv[3]))
resultf = open(sys.argv[3], "w")

print("runing mapping...")
sat1_user = dict()
sat2_user = dict()

dats_len = len(dats)
for i, dat in enumerate(dats):

    #debug
    if i%100000 == 0:
        print("%d/%d"%(i/100000,dats_len/100000))

    dat = dat.split()
    probs[i] = float(probs[i])
    (userid, itemid) = (int(dat[0]), int(dat[1]))
    if int(dat[3]) < 1321891200:
        if sat1_user.has_key(userid) == False:
            sat1_user[userid] = []
            sat1_user[userid].append( (probs[i],itemid) )
        else:
            sat1_user[userid].append( (probs[i],itemid) )
    else:
        if sat2_user.has_key(userid) == False:
            sat2_user[userid] = []
            sat2_user[userid].append( (probs[i],itemid) )
        else:
            sat2_user[userid].append( (probs[i],itemid) )


print("mapping done")
print("Sat1: picking top 3 items for each user...")
print("sat1len:%d"%len(sat1_user))
print("sat2len:%d"%len(sat2_user))
dickeys = sat1_user.keys()
dickeys.sort()

for userid in dickeys:
    itemlist = sat1_user[userid]
    itemlist = sorted(itemlist, key=lambda prob: -prob[0])
    resultf.write("%d,"%(userid))
    for i in range(1,min(3,len(itemlist))+1):
        resultf.write("%d "%(itemlist[i-1][1]))
    resultf.write("\n")
    
print("Sat2: picking top 3 items for each user...")
for userid, itemlist in sorted(sat2_user.iteritems()):
    #print(itemlist)
    itemlist = sorted(itemlist, key=lambda prob: -prob[0])
    #print(itemlist)
    resultf.write("%d,"%(userid))
    for i in range(1,min(3,len(itemlist))+1):
        resultf.write("%d "%(itemlist[i-1][1]))
    resultf.write("\n")

outf.close()
datf.close()
resultf.close()

print("%s is created."%(sys.argv[3]))

