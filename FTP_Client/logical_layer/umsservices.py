import sys
sys.path.append("..")
from data_layer.DBConnection import DBconnection
from data_layer.user import User

class UMS:
	@staticmethod
	def add(u):
		result=False
		cnx=DBconnection.connect()
		cur=cnx.cursor()
		query="insert into user(username,password,usertype,userstatus,name,email,contact,address,gender) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		data=[]
		data.append(u.getUsername())
		data.append(u.getPassword())
		data.append(u.getUsertype())
		data.append(u.getUserstatus())
		data.append(u.getName())
		data.append(u.getEmail())
		data.append(u.getContact())
		data.append(u.getAddress())
		data.append(u.getGender())
		try:
			cur.execute(query,data)
		except:
			result=False
		if (cur.rowcount==1):
			result=True
		cnx.commit()
		cur.close()
		cnx.close()
		return result
	@staticmethod
	def view():
		ulist=[]
		cnx=DBconnection.connect()
		cur=cnx.cursor()
		query="select * from user"
		cur.execute(query)
		d=cur.fetchall()
		for i in d:
			u=User()
			u.setUserid(int(i[0]))
			u.setUsername(i[1])
			u.setPassword(i[2])
			u.setUsertype(i[3])
			u.setUserstatus(bool(i[4]))
			u.setName(i[5])
			u.setEmail(i[6])
			u.setContact(i[7])
			u.setAddress(i[8])
			u.setGender(bool(i[9]))
			ulist.append(u)
		cur.close()
		cnx.close()
		return ulist
	@staticmethod
	def updateUser(u):
		result=False
		cnx=DBconnection.connect()
		cur=cnx.cursor()
		query="update user set usertype=%s,userstatus=%s,name=%s,email=%s,contact=%s,address=%s,gender=%s where userid=%s"
		data=[]
		data.append(u.getUsertype())
		data.append(u.getUserstatus())
		data.append(u.getName())
		data.append(u.getEmail())
		data.append(u.getContact())
		data.append(u.getAddress())
		data.append(u.getGender())
		data.append(u.getUserid())
		cur.execute(query,data)
		if cur.rowcount==1:
			result=True
		cnx.commit()
		cur.close()
		cnx.close()
		return result
	@staticmethod
	def updateProfile(p):
		result=False
		cnx=DBconnection.connect()
		cur=cnx.cursor()
		query="update user set name=%s,email=%s,contact=%s,address=%s,gender=%s where userid=%s"
		data=[]
		data.append(p.getName())
		data.append(p.getEmail())
		data.append(p.getContact())
		data.append(p.getAddress())
		data.append(p.getGender())
		data.append(p.getUserid())
		cur.execute(query,data)
		if cur.rowcount==1:
			result=True
		cnx.commit()
		cur.close()
		cnx.close()
		return result
	@staticmethod
	def search(id):
		cnx=DBconnection.connect()
		cur=cnx.cursor()
		query="select * from user where userid=%s"
		data=[]
		data.append(id)
		cur.execute(query,data)
		d=cur.fetchall()
		if cur.rowcount==0:
			cur.close()
			cnx.close()
			return None
		for i in d:
			u=User()
			u.setUserid(int(i[0]))
			u.setUsername(i[1])
			u.setPassword(i[2])
			u.setUsertype(i[3])
			u.setUserstatus(bool(i[4]))
			u.setName(i[5])
			u.setEmail(i[6])
			u.setContact(i[7])
			u.setAddress(i[8])
			u.setGender(bool(i[9]))
		cur.close()
		cnx.close()
		return u
		
	
	@staticmethod
	def viewFiles(uname):
		flist=[]
		cnx=DBconnection.connect()
		cur=cnx.cursor()
		query="select f_name,date,type,size from uploaded_files where username=%s"
		data=[]
		data.append(uname)
		cur.execute(query,data)
		d=cur.fetchall()
		for i in d:
			flist.append(i)	
		cur.close()
		cnx.close()
		return flist
		
	@staticmethod
	def getFileType(uname,f_name):
		cnx=DBconnection.connect()
		cur=cnx.cursor()
		query="select type from uploaded_files where username=%s and f_name=%s"
		data=[]
		data.append(uname)
		data.append(f_name)
		cur.execute(query,data)
		type=cur.fetchall()[0][0]
		cur.close()
		cnx.close()
		return type
	
		
		
		
			
	