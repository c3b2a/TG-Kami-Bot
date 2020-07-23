import time,os

if not os.path.exists('Token.txt'):
	newFile = open('Token.txt','w')
	newFile.close()

class Func():
	class tokenClass():
		def __init__(self):
			self.userToken = ""
			self.userType  = ""
		def chkAvail(self,userType):
			availList = ['global-admin','privileged-admin','common-admin','readonly','writeonly']
			for i in availList:
				if i == userType:
					return True
			return False
	def __init__(self):
		self.Users = [None for i in range(100)]
		self.usersCount = 0
		self.tokenFile = open('Token.txt','r+')
		self.tokenFile.seek(0,0)
		self.usersCount = 0
		while True:
			string = self.tokenFile.readline()
			if not string:
				break
			else:
				if len(string.split()) == 2 and self.tokenClass().chkAvail(string.split()[1]):
					self.Users[self.usersCount] = self.tokenClass()
					self.Users[self.usersCount].userToken = string.split()[0]
					self.Users[self.usersCount].userType  = string.split()[1]
					self.usersCount += 1