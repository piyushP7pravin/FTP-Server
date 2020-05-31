class User:
	def __init__(self,userid=1,username="",password="",usertype="",userstatus=1,name="",email="",contact="",address="",gender=0):
		self.__userid=userid
		self.__username=username
		self.__password=password
		self.__usertype=usertype
		self.__userstatus=userstatus
		self.__name=name
		self.__email=email
		self.__contact=contact
		self.__address=address
		self.__gender=gender
	def __str__(self):
		return str(self.__userid)+" "+str(self.__username)+" "+str(self.__password)+" "+str(self.__usertype)+" "+str(self.__userstatus)+" "+str(self.__name)+" "+str(self.__email)+" "+str(self.__contact)+" "+str(self.__address)+" "+str(self.__gender)
	def getUserid(self):
		return self.__userid
	def getUsername(self):
		return self.__username
	def getPassword(self):
		return self.__password
	def getUsertype(self):
		return self.__usertype
	def getUserstatus(self):
		return self.__userstatus
	def getName(self):
		return self.__name
	def getEmail(self):
		return self.__email
	def getContact(self):
		return self.__contact
	def getAddress(self):
		return self.__address
	def getGender(self):
		return self.__gender
	def setUserid(self,id):
		self.__userid=id
	def setUsername(self,uname):
		self.__username=uname
	def setPassword(self,passwd):
		self.__password=passwd
	def setUsertype(self,utype):
		self.__usertype=utype
	def setUserstatus(self,status):
		self.__userstatus=status
	def setName(self,name):
		self.__name=name
	def setEmail(self,email):
		self.__email=email
	def setContact(self,contact):
		self.__contact=contact
	def setAddress(self,address):
		self.__address=address
	def setGender(self,gender):
		self.__gender=gender
		
		
