import sys

#item profile matrix
item_profile_fp = open(sys.argv[1],"r")
lines = item_profile_fp.readlines()
maxn = 0
mean = 0
keywordsdic = {}
itemKeywords = {}
itemKeywords_bool = {}
keywordIdx = {}

print("filling keywords per item...")
line_num = len(lines)
i=0
for line in lines:
    print(float(i)/line_num)
    i+=1
    line = line.split()
    itemid = int(line[0])
    keywords = line[2].split(';')
    itemKeywords[itemid] = []

    if keywords[0] != '0':
        maxn = max(maxn, len(keywords))
        mean = mean + len(keywords)
        for keyword in keywords:
            keyword = int(keyword)
            itemKeywords[itemid].append(keyword)
            if keyword not in keywordsdic:
                keywordsdic[keyword] = 1 
            else:
                keywordsdic[keyword] += 1

print("arranging keyword index...")
#select keyword idx
idx = 0
for i in keywordsdic.keys():
    if keywordsdic[i] > 1:
        keywordIdx[i]=idx
        idx += 1

print("# of total keywords: %d"%len(keywordsdic))
print("# of keywords having items more or equal to 1: %d"%idx)

out_fp = open("train_keyword_out.txt", "w")
item_profile_fp.close()
item_profile_fp = open(sys.argv[1], "r")
lines = item_profile_fp.readlines()

print("creating output file...")
#make matrix
for line in lines:
    line = line.split()
    itemid = int(line[0])

    out_fp.write("%s"%itemid)
    for keyword in itemKeywords[itemid]:
        if keyword in keywordIdx:
            out_fp.write(" %s"%keywordIdx[keyword])
    out_fp.write("\n")



out_fp.close()
item_profile_fp.close()
