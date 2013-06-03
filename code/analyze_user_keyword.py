import sys

userkeyword_f = open(sys.argv[1], "r")
lines = userkeyword_f.readlines()
keywordsSet={}
mean=0
maxv=0
for line in lines:
    line = line.split()
    keywords = line[1].split(';')
    userid = line[0]
    for keyword in keywords:
        keyword=keyword.split(':')
        if int(keyword[0]) not in keywordsSet:
            keywordsSet[int(keyword[0])]=1
        else:
            keywordsSet[int(keyword[0])]+=1
    mean += len(keywords)
    maxv=max(maxv,len(keywords))
print("mean:%d"%(float(mean)/len(lines)))
print("max:%d"%maxv)
print("cnt:%d"%len(keywordsSet))
for i in keywordsSet.keys():
    print(keywordsSet[i])
