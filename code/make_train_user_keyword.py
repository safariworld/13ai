import sys

userkeyword_f = open(sys.argv[1], "r")
lines = userkeyword_f.readlines()
keywordsSet={}

userKeywords = {}
userKeyweights = {}
keywordIdx = {}

mean=0
maxv=0

print("filling keywords per user...")
line_num = len(lines)
i=0
for line in lines:
    print(float(i)/line_num)
    i+=1
    line = line.split()
    keywords = line[1].split(';')
    userid = int(line[0])
    userKeywords[userid] = []
    userKeyweights[userid] = {}

    for keyword in keywords:
        keyword=keyword.split(':')
        userKeywords[userid].append(int(keyword[0]))
        userKeyweights[userid][int(keyword[0])] = float(keyword[1])

        if int(keyword[0]) not in keywordsSet:
            keywordsSet[int(keyword[0])]=1
        else:
            keywordsSet[int(keyword[0])]+=1
    mean += len(keywords)
    maxv=max(maxv,len(keywords))

print("arranging keyword index...")
idx = 0
for i in keywordsSet.keys():
    if keywordsSet[i] > 1:
        keywordIdx[i] = idx
        idx += 1

data_fp = open(sys.argv[2], "r")
out_fp = open("data_keyword_out.txt", "w")
lines = data_fp.readlines()

print("creating output file...")
#make matrix
for line in lines:
    line = line.split()
    userid = int(line[0])

    out_fp.write("%s"%userid)
    for keyword in userKeywords[userid]:
        if keyword in keywordIdx:
            out_fp.write(" %d:%.2f"%(keywordIdx[keyword],userKeyweights[userid][keyword]))
    out_fp.write("\n")

out_fp.close()
data_fp.close()
userkeyword_f.close()

print("mean:%d"%(float(mean)/len(lines)))
print("max:%d"%maxv)
print("cnt:%d"%len(keywordsSet))
