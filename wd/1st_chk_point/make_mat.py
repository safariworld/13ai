userProfile = {}
item = {}

def read_user_profile():
	global userProfile
	txt = open('user_profile.txt')
	for line in txt.readlines():
		tmp = line.split()
		try:
			tmp[1] = int(tmp[1])
			tmp[1] = str(tmp[1])
		except:
			tmp[1] = 'NA'
		List = [tmp[1], tmp[2], tmp[3]] # year, gender, numOfTweet
		userProfile[tmp[0]] = List

def read_item():
	global item
	txt = open('item.txt')
	for line in txt.readlines():
		tmp = line.split()
		taxo = tmp[1].split('.')
		try:
			retaxo = float(taxo[0])*100 + float(taxo[1]) + float(taxo[2])*0.01 + float(taxo[3])*0.0001
		except:
			retaxo = float(taxo[0])*100 + float(taxo[1])
		item[tmp[0]] = str(retaxo)

read_user_profile()
read_item()
txt = open('rec_log_test.txt')
#txt = open('rec_log_train.txt')
for line in txt.readlines():
	tmp = line.split()
	List = userProfile[tmp[0]]
	print tmp[0] + '::' + tmp[1] + '::' + tmp[2] + '::' + List[0] + '::' + List[1] + '::' + List[2] + '::' + item[tmp[1]]
