import mysql.connector

class DBconnection:
	host="127.0.0.1"
	port="3306"
	username="root"
	password=""
	database="ftpserver"
	@staticmethod
	def connect():
		return mysql.connector.connect(host=DBconnection.host,port=DBconnection.port,username=DBconnection.username,passwd=DBconnection.password,database=DBconnection.database)
		