import sys
sys.path.append("..")
from data_layer.DBConnection import DBconnection
from data_layer.user import User

class Authentication():
	@staticmethod
	def loginCheck(un,pd):
		result=-1 
		cnx=DBconnection.connect()
		cur=cnx.cursor()
		query="select userid,username,password from user"
		cur.execute(query)
		d=cur.fetchall()
		for i in d:
			if i[1]==un and i[2]==pd:
				result=i[0]
		cur.close()
		cnx.close()
		return result
	@staticmethod			
	def forgotPassword():
		pass
	@staticmethod
	def changePassword(userid,pd,new_pd):
		result=False
		cnx=DBconnection.connect()
		cur=cnx.cursor()
		query="select password from user where userid=%s"
		cur.execute(query,(userid,))
		d=cur.fetchall()
		for i in d:
			if pd==i[0]:
				query="update user set password=%s where userid=%s"
				cur.execute(query,(new_pd,userid))
				result=True
		cnx.commit()
		cur.close()
		cnx.close()
		return result
	@staticmethod	
	def logout(root):
		root.destroy()