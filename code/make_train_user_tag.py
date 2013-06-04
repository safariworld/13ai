import sys

#user profile matrix
user_profile_fp = open(sys.argv[1],"r")
lines = user_profile_fp.readlines()
maxn = 0
mean = 0
tagsdic = {}
userTags = {}
userTags_bool = {}
tagIdx = {}

print("filling tags per user...")
line_num = len(lines)
i=0
for line in lines:
    print(float(i)/line_num)
    i+=1
    line = line.split()
    userid = int(line[0])
    tags = line[4].split(';')
    userTags[userid] = []

    if tags[0] != '0':
        maxn = max(maxn, len(tags))
        mean = mean + len(tags)
        for tag in tags:
            tag = int(tag)
            userTags[userid].append(tag)
            if tag not in tagsdic:
                tagsdic[tag] = 1 
            else:
                tagsdic[tag] += 1

print("arranging tag index...")
#select tag idx
idx = 0
for i in tagsdic.keys():
    if tagsdic[i] > 0:
        tagIdx[i]=idx
        idx += 1


train_fp = open(sys.argv[2], "r")
out_fp = open("train_tag_out.txt", "w")
lines = train_fp.readlines()

print("creating output file...")
#make matrix
for line in lines:
    line = line.split()
    userid = int(line[0])

    out_fp.write("%s"%userid)
    for tag in userTags[userid]:
        if tag in tagIdx:
            out_fp.write(" %s"%tagIdx[tag])
    out_fp.write("\n")

out_fp.close()
train_fp.close()
user_profile_fp.close()
