import sys

user_profile_fp = open(sys.argv[1],"r")
lines = user_profile_fp.readlines()
maxn = 0
mean = 0
keywordsdic = {}
for line in lines:
    line = line.split()
    userid = line[0]
    keywords = line[4].split(';')
    if keywords[0] != '0':
        maxn = max(maxn, len(keywords))
        mean = mean + len(keywords)
        for keyword in keywords:
            if keyword not in keywordsdic:
                keywordsdic[keyword] = 1 
            else:
                keywordsdic[keyword] += 1


print("max:%d\n"%maxn)
print("mean:%f\n"%(((float)(mean))/len(lines)))
print("# of keywords: %d\n"%len(keywordsdic))
for i in keywordsdic.keys():
    print i, keywordsdic[i]
