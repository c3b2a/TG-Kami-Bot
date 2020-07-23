from . import func
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from datetime import datetime
import time,os,random,string,re,xlrd

def random_string(length):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits,length))
    return ran_str

def chkRepeat(List,Item):
	if Item in List:
		return True
	return False

def chkTagAvail(tag):
	regexp = r'^[A-Za-z0-9\u4e00-\u9fa5:]*$'
	if re.match(regexp,tag):
		return True
	return False

def getKami():
	List = []
	with open('../kamifile.txt','r') as f:
		while True:
			string = f.readline()
			if not string:
				break
			if len(string.split()) >= 4 and string.split()[1] == ''.join(list(filter(str.isdigit,string.split()[1]))):
				segment = string.split()
				tmpList = [None for i in range(4)]
				tmpList[0] = segment[0]
				tmpList[1] = int(segment[1])
				tmpList[2] = segment[2].split(':')
				tmpList[3] = segment[3]
				for index in range(len(segment) - 4):
					tmpList[3] += ' ' + segment[index + 4]
				List.append(tmpList)
	return List

def isLetterOrDigit(string):
	filterNum = ''.join(list(filter(str.isalnum,string)))
	if filterNum == string:
		return True
	return False

def isAllDigit(string):
	filterNum = ''.join(list(filter(str.isdigit,string)))
	if filterNum == string:
		return True
	return False

class util:
	def isLetterOrDigit(string):
		filterNum = ''.join(list(filter(str.isalnum,string)))
		if filterNum == string:
			return True
		return False
	def isAllDigit(string):
		filterNum = ''.join(list(filter(str.isdigit,string)))
		if filterNum == string:
			return True
		return False
	def getBan():
		with open('../ban.txt','r') as f:
			List = []
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) == 1:
					List.append(string.split()[0])
			return List
	def delBan(delList):
		banList = []
		with open('../ban.txt','r+') as f:
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) == 1:
					banList.append(string.split()[0])
			f.seek(0,0)
			f.truncate()
			for i in range(len(banList)):
				if not delList[i]:
					f.write(banList[i] + '\n')
	def addBan(Id):
		with open('../ban.txt','a+') as f:
			f.write(Id + '\n')
	def getAdmin():
		with open('../admin.txt','r') as f:
			List = []
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) == 1 and ''.join(list(filter(str.isdigit,string.split()[0]))) == string.split()[0]:
					List.append(string.split()[0])
			return List
	def getKami():
		List = []
		with open('../kamifile.txt','r') as f:
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) >= 4 and string.split()[1] == ''.join(list(filter(str.isdigit,string.split()[1]))):
					segment = string.split()
					tmpList = [None for i in range(4)]
					tmpList[0] = segment[0]
					tmpList[1] = int(segment[1])
					tmpList[2] = segment[2].split(':')
					tmpList[3] = segment[3]
					for index in range(len(segment) - 4):
						tmpList[3] += ' ' + segment[index + 4]
					List.append(tmpList)
		return List
	def delKami(delList):
		List = []
		with open('../kamifile.txt','r+') as f:
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) >= 4 and string.split()[1] == ''.join(list(filter(str.isdigit,string.split()[1]))):
					segment = string.split()
					tmpList = [None for i in range(4)]
					tmpList[0] = segment[0]
					tmpList[1] = int(segment[1])
					tmpList[2] = segment[2].split(':')
					tmpList[3] = segment[3]
					for index in range(len(segment) - 4):
						tmpList[3] += ' ' + segment[index + 4]
					List.append(tmpList)
			f.seek(0,0)
			f.truncate()
			for i in range(len(delList)):
				if not delList[i]:
					f.write(List[i][0] + ' ' + str(List[i][1]) + ' ' + ':'.join(List[i][2]) + ' ' + List[i][3] + '\n')
	def resetKami(resetList):
		List = []
		with open('../kamifile.txt','r+') as f:
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) >= 4 and string.split()[1] == ''.join(list(filter(str.isdigit,string.split()[1]))):
					segment = string.split()
					tmpList = [None for i in range(4)]
					tmpList[0] = segment[0]
					tmpList[1] = int(segment[1])
					tmpList[2] = segment[2].split(':')
					tmpList[3] = segment[3]
					for index in range(len(segment) - 4):
						tmpList[3] += ' ' + segment[index + 4]
					List.append(tmpList)
			f.seek(0,0)
			f.truncate()
			for i in range(len(resetList)):
				if not resetList[i]:
					f.write(List[i][0] + ' ' + str(List[i][1]) + ' ' + ':'.join(List[i][2]) + ' ' + List[i][3] + '\n')
				else:
					f.write(random_string(16) + ' ' + str(List[i][1]) + ' ' + ':'.join(List[i][2]) + ' ' + List[i][3] + '\n')
	def setKami(which,nkami):
		List = []
		with open('../kamifile.txt','r+') as f:
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) >= 4 and string.split()[1] == ''.join(list(filter(str.isdigit,string.split()[1]))):
					segment = string.split()
					tmpList = [None for i in range(4)]
					tmpList[0] = segment[0]
					tmpList[1] = int(segment[1])
					tmpList[2] = segment[2].split(':')
					tmpList[3] = segment[3]
					for index in range(len(segment) - 4):
						tmpList[3] += ' ' + segment[index + 4]
					if nkami.split()[0] == tmpList[0].split()[0]:
						return False
					List.append(tmpList)
			f.seek(0,0)
			f.truncate()
			for i in range(len(List)):
				if i != which:
					f.write(List[i][0] + ' ' + str(List[i][1]) + ' ' + ':'.join(List[i][2]) + ' ' + List[i][3] + '\n')
				else:
					f.write(nkami + ' ' + str(List[i][1]) + ' ' + ':'.join(List[i][2]) + ' ' + List[i][3] + '\n')
		return True
	def setNum(changeList,nNum):
		List = []
		with open('../kamifile.txt','r+') as f:
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) >= 4 and string.split()[1] == ''.join(list(filter(str.isdigit,string.split()[1]))):
					segment = string.split()
					tmpList = [None for i in range(4)]
					tmpList[0] = segment[0]
					tmpList[1] = int(segment[1])
					tmpList[2] = segment[2].split(':')
					tmpList[3] = segment[3]
					for index in range(len(segment) - 4):
						tmpList[3] += ' ' + segment[index + 4]
					List.append(tmpList)
			f.seek(0,0)
			f.truncate()
			for i in range(len(List)):
				if not changeList[i]:
					f.write(List[i][0] + ' ' + str(List[i][1]) + ' ' + ':'.join(List[i][2]) + ' ' + List[i][3] + '\n')
				else:
					f.write(List[i][0] + ' ' + str(nNum) + ' ' + ':'.join(List[i][2]) + ' ' + List[i][3] + '\n')
	def editKami(nkami,nnum,ntag,nps,which):
		List = []
		with open('../kamifile.txt','r+') as f:
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) >= 4 and string.split()[1] == ''.join(list(filter(str.isdigit,string.split()[1]))):
					segment = string.split()
					if segment[0].split()[0] == nkami.split()[0]:
						return False
					tmpList = [None for i in range(4)]
					tmpList[0] = segment[0]
					tmpList[1] = int(segment[1])
					tmpList[2] = segment[2].split(':')
					tmpList[3] = segment[3]
					for index in range(len(segment) - 4):
						tmpList[3] += ' ' + segment[index + 4]
					List.append(tmpList)
			f.seek(0,0)
			f.truncate()
			for i in List:
				if i[0] == which:
					nkami = nkami if nkami else i[0]
					nnum = nnum if nnum else str(i[1])
					if ntag:
						tagSplit = ntag.split(':')
						tagList = []
						for i in tagSplit:
							if i:
								tagList.append(i)
						ntag = ':'.join(tagList)
					else:
						ntag = ':'.join(i[2])
					nps = nps if nps else i[3]
					break
			for i in range(len(List)):
				if List[i][0] != which.split()[0]:
					f.write(List[i][0] + ' ' + str(List[i][1]) + ' ' + ':'.join(List[i][2]) + ' ' + List[i][3] + '\n')
				else:
					f.write(nkami + ' ' + nnum + ' ' + ntag + ' ' + nps + '\n')
		return True
	def addKami(akami,anum,atag,aps):
		akami = akami if akami else random_string(16)
		tmpTagList = []
		tagSplit = atag.split(':')
		for i in tagSplit:
			if i:
				tmpTagList.append(i)
		atag = ':'.join(tmpTagList)
		if chkRepeat([i[0] for i in getKami()],akami):
			return False
		with open('../kamifile.txt','a+') as f:
			f.write(akami + ' ' + anum + ' ' + atag + ' ' + aps + '\n')
		return True
	def addKamiInBulk(addList):
		errCounts = 0
		with open('../kamifile.txt','r+') as f:
			List = []
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) >= 4 and string.split()[1] == ''.join(list(filter(str.isdigit,string.split()[1]))):
					segment = string.split()
					tmpList = [None for i in range(4)]
					tmpList[0] = segment[0]
					tmpList[1] = int(segment[1])
					tmpList[2] = segment[2].split(':')
					tmpList[3] = segment[3]
					for index in range(len(segment) - 4):
						tmpList[3] += ' ' + segment[index + 4]
					List.append(tmpList)
			for i in range(len(addList)):
				if addList[i][0]:
					if not isLetterOrDigit(addList[i][0]):
						errCounts += 1
						continue
				else:
					addList[i][0] = random_string(16)
				if addList[i][0] in [i[0] for i in List]:
					errCounts += 1
					continue
				if (not isAllDigit(addList[i][1])) or (not addList[i][1]):
					errCounts += 1
					continue
				if (not chkTagAvail(addList[i][2])) or (not addList[i][2]):
					errCounts += 1
					continue
				if not addList[i][3]:
					errCounts += 1
					continue
				f.write(addList[i][0] + ' ' + addList[i][1] + ' ' + addList[i][2] + ' ' + addList[i][3] + '\n')
		return errCounts
	def xlsx_to_2darray(file_path):
		xlsx_file = xlrd.open_workbook(file_path)
		sheet = xlsx_file.sheet_by_index(0)
		rows = sheet.nrows
		data = [[] for i in range(rows)]
		for i in range(rows):
			data[i] = sheet.row_values(i)[0:4]
		return data
	def add_kami_with_2d_array(data):
		err_counts = 0
		with open('../kamifile.txt','a+') as f:
			for i in range(len(data)):
				if data[i][0] in [j[0] for j in getKami()]:
					err_counts += 1
					continue
				if data[i][0] and (not isLetterOrDigit(data[i][0])):
					err_counts += 1
					continue
				if not data[i][0]:
					data[i][0] = random_string(16)
				if (not data[i][1]) or ((not isinstance(data[i][1],float)) and (not isinstance(data[i][1],int))) or (int(data[i][1]) != data[i][1]):
					err_counts += 1
					continue
				data[i][1] = str(int(data[i][1]))
				if (not data[i][2]) or (not chkTagAvail(data[i][2])):
					err_counts += 1
					continue
				if not data[i][3]:
					err_counts += 1
					continue
				f.write(data[i][0] + ' ' + data[i][1] + ' ' + data[i][2] + ' ' + data[i][3] + '\n')
		return err_counts
	def read_log():
		List = []
		with open('../searchLog.txt','r') as f:
			while True:
				string = f.readline()
				if not string:
					break
				string_split = string.split()
				if len(string_split) == 3:
					tmpList = []
					tmpList.append(string_split[0])
					tmpList.append(string_split[1])
					tmpList.append(str(datetime.utcfromtimestamp(int(float(string_split[1])))))
					tmpList.append(string_split[2])
					List.append(tmpList)
		return List

class tokenData():
	def __init__(self):
		self.tokenList  = func.Func().Users
		self.tokenCount = func.Func().usersCount
		self.typeList = ['global-admin','privileged-admin','common-admin','readonly','writeonly']
	def chkToken(self,token):
		flag = False
		for i in range(self.tokenCount):
			if str(self.tokenList[i].userToken) == str(token):
				flag = True
				break
		return flag
	def convertDict(self):
		returndict = {}
		for i in range(self.tokenCount):
			returndict[self.tokenList[i].userToken] = self.tokenList[i].userType
		return returndict
	def getBotAdmin(self):
		view_dict = {}
		with open('../admin.txt','r+') as f:
			counts = 0
			while True:
				string = f.readline()
				if not string:
					break
				elif len(string.split()) == 1:
					view_dict[string.split()[0]] = 'super-admin' if counts == 0 else 'common-admin'
					counts += 1
		return view_dict
	def chkIDRepeat(self,ID):
		with open('../admin.txt','r+') as f:
			while True:
				string = f.readline()
				if not string:
					break
				if int(string) == int(ID):
					return True
			return False
	def cookieTimeout(self,request):
		flag = False
		response = HttpResponseRedirect('/')
		timeCookie = request.COOKIES.get('time')
		if timeCookie:
			if time.time() - float(timeCookie) >= 3600 or time.time() - float(timeCookie) < 0:
				flag = True
				response = HttpResponseRedirect('/login')
				response.delete_cookie('time',str(time.time()))
				response.delete_cookie('token')
		return flag,response
	def getIdentity(self,token):
		for i in range(self.tokenCount):
			if str(self.tokenList[i].userToken) == str(token):
				return self.tokenList[i].userType
	def webguiWriteDetail(self,token,identity):
		with open('Token.txt','a+') as f:
			f.write(token + ' ' + identity + '\n')
	def botWriteID(self,ID):
		with open('../admin.txt','a+') as f:
			f.write(ID + '\n')
	def identityAuth(self,identity,args):
		boolean = [False for i in range(len(self.typeList))]
		for i in range(len(args)):
			boolean[args[i]] = True
		for i in range(len(self.typeList)):
			if identity == self.typeList[i] and boolean[i]:
				return True
		return False
	def refreshData(self):
		data.loadFile()
		self.tokenList = func.Func().Users
		self.tokenCount = func.Func().usersCount
	def delWebguiAdmin(self,token):
		with open('Token.txt','w') as f:
			for i in range(self.tokenCount):
				if self.tokenList[i].userToken != token:
					f.write(self.tokenList[i].userToken + ' ' + self.tokenList[i].userType + '\n')
	def editWebguiAdmin(self,token,ntoken,nidentity):
		with open('Token.txt','w') as f:
			for i in range(self.tokenCount):
				if self.tokenList[i].userToken != token:
					f.write(self.tokenList[i].userToken + ' ' + self.tokenList[i].userType + '\n')
				else:
					f.write(ntoken + ' ' + nidentity + '\n')
	def delBotAdmin(self,ID):
		with open('../admin.txt','r+') as f:
			adminID = []
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) == 1:
					if util.isAllDigit(string.split()[0]):
						adminID.append(string.split()[0])
			f.seek(0,0)
			f.truncate()
			for i in range(len(adminID)):
				if int(ID) != int(adminID[i]):
					f.write(adminID[i] + '\n')
	def editBotAdmin(self,ID,nid):
		with open('../admin.txt','r+') as f:
			adminID = []
			while True:
				string = f.readline()
				if not string:
					break
				if len(string.split()) == 1:
					if util.isAllDigit(string.split()[0]):
						adminID.append(string.split()[0])
			f.seek(0,0)
			f.truncate()
			for i in range(len(adminID)):
				if int(ID) != int(adminID[i]):
					f.write(adminID[i] + '\n')
				else:
					f.write(str(int(nid)) + '\n')
