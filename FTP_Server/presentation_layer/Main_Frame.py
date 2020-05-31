import login
import sys
sys.path.append("..")
import tkinter
from tkinter import messagebox
from logical_layer.loginservices import Authentication
from logical_layer.umsservices import *
from data_layer.user import User
from presentation_layer.login import Login
import socket
from threading import Thread
import os
from datetime import datetime

class MainFrame:
	def __init__(self,uid,uname):
		self.uid=uid
		self.uname=uname
		
		self.root=tkinter.Tk()
		self.root.title("FTP Server")
		self.root.geometry("500x200")
		
		self.menubar=tkinter.Menu(self.root,relief="flat")
		self.logoutmenu=tkinter.Menu(self.menubar,tearoff=0)
		self.logoutmenu.add_command(label="Logout",font=("Calibri Light",12),command=self.menu_logout_clicked)
		self.logoutmenu.add_command(label="Change Password",font=("Calibri Light",12),command=self.menu_changepass_clicked)
		self.menubar.add_cascade(label="Logout",menu=self.logoutmenu)
		
		self.umsmenu=tkinter.Menu(self.menubar,tearoff=0)
		self.umsmenu.add_command(label="Manage User",font=("Calibri Light",12),command=self.menu_manageuser_clicked)
		self.umsmenu.add_command(label="Manage Profile",font=("Calibri Light",12),command=self.menu_manageprofile_clicked)
		self.menubar.add_cascade(label="UMS",menu=self.umsmenu)
		
		self.servermenu=tkinter.Menu(self.menubar,tearoff=0)
		self.servermenu.add_command(label="Start Server",font=("Calibri Light",12),command=self.menu_startserver_clicked)
		self.servermenu.add_command(label="Stop Server",font=("Calibri Light",12),command=self.menu_stopserver_clicked)
		self.menubar.add_cascade(label="Server",menu=self.servermenu)
		
		self.root.config(menu=self.menubar)
		self.root.mainloop()
		
	def menu_logout_clicked(self):
		Authentication.logout(self.root)
		Login()
	def menu_changepass_clicked(self):
		self.root.destroy()
		ChangePass(self.uid)
	def menu_manageuser_clicked(self):
		self.root.destroy()
		ManageUser(self.uid)
	def menu_manageprofile_clicked(self):
		self.root.destroy()
		ManageProfile(self.uid)
	def menu_startserver_clicked(self):
		StartServer()
	def menu_stopserver_clicked(self):
		pass
	
class ChangePass:
	def __init__(self,uid):
		self.uid=uid
		self.root=tkinter.Tk()
		self.root.title("Change Password")
		self.root.geometry("400x200")
		self.root.configure(bg="gray99")
		
		tkinter.Label(self.root,text="Old Password",bg="gray99",font=("Calibri Light",12)).place(x=50,y=30)
		tkinter.Label(self.root,text="New Password",bg="gray99",font=("Calibri Light",12)).place(x=50,y=70)
		
		self.__oldpassword=tkinter.Entry(self.root,relief="flat",bg="white",highlightbackground="gray",highlightthicknes=1,highlightcolor="RoyalBlue2",font=("Calibri Light",12),show="*")
		self.__oldpassword.place(x=170,y=30,height=32)
		def on_enter_op(event=None):
			self.__oldpassword.config(highlightbackground="RoyalBlue2",highlightthicknes=2)
		def on_leave_op(event=None):
			self.__oldpassword.config(highlightbackground="gray",highlightthicknes=1)
		self.__oldpassword.bind("<Enter>",on_enter_op)
		self.__oldpassword.bind("<Leave>",on_leave_op)
		
		self.__newpassword=tkinter.Entry(self.root,show="*",relief="flat",bg="white",highlightbackground="gray",highlightthicknes=1,highlightcolor="RoyalBlue2",font=("Calibri Light",12))
		self.__newpassword.place(x=170,y=70,height=32)
		def on_enter_np(event=None):
			self.__newpassword.config(highlightbackground="RoyalBlue2",highlightthicknes=2)
		def on_leave_np(event=None):
			self.__newpassword.config(highlightbackground="gray",highlightthicknes=1)
		self.__newpassword.bind("<Enter>",on_enter_np)
		self.__newpassword.bind("<Leave>",on_leave_np)
		self.__newpassword.bind("<Return>",self.btn_change_clicked)
		
		self.btn_changePass=tkinter.Button(self.root,text="Change Password",width=14,relief="flat",bg="RoyalBlue2",fg="gray99",font=("Calibri Light",16,"bold"),command=self.btn_change_clicked)
		self.btn_changePass.place(x=50,y=120,height=35)
		def on_enter_btn_cp(event):
			self.btn_changePass.config(bg="SkyBlue1")
		def on_leave_btn_cp(event):
			self.btn_changePass.config(bg="RoyalBlue2")
		self.btn_changePass.bind("<Enter>",on_enter_btn_cp)
		self.btn_changePass.bind("<Leave>",on_leave_btn_cp)
		
		self.btn_clear=tkinter.Button(self.root,text="Clear",width=7,relief="flat",bg="RoyalBlue2",fg="gray99",font=("Calibri Light",16,"bold"),command=self.btn_clear_clicked)
		self.btn_clear.place(x=240,y=120,height=35)
		def on_enter_btn_cl(event):
			self.btn_clear.config(bg="SkyBlue1")
		def on_leave_btn_cl(event):
			self.btn_clear.config(bg="RoyalBlue2")
		self.btn_clear.bind("<Enter>",on_enter_btn_cl)
		self.btn_clear.bind("<Leave>",on_leave_btn_cl)
		
		self.root.mainloop()
		
	def btn_change_clicked(self,event=None):
		if Authentication.changePassword(self.uid,self.__oldpassword.get(),self.__newpassword.get()):
			messagebox.showinfo("Change Password","Password changed")
			self.root.destroy()
			Login()
		else:
			messagebox.showerror("Error","old password not matched")
			
	def btn_clear_clicked(self):
		self.__newpassword.delete(0,"end")
		self.__oldpassword.delete(0,"end")

class ManageUser:
	def __init__(self,uid):
		self.uid=uid
		self.root=tkinter.Tk()
		self.root.title("Manage User")
		self.root.geometry("500x400")
		tkinter.Label(self.root,text="User ID",anchor="w").grid(row=0,column=0,padx=30)
		tkinter.Label(self.root,text="Username",anchor="w").grid(row=1,column=0)
		tkinter.Label(self.root,text="User type",anchor="w").grid(row=2,column=0)
		tkinter.Label(self.root,text="User status",anchor="w").grid(row=3,column=0)
		tkinter.Label(self.root,text="Name",anchor="w").grid(row=4,column=0)
		tkinter.Label(self.root,text="Email",anchor="w").grid(row=5,column=0)
		tkinter.Label(self.root,text="Contact",anchor="w").grid(row=6,column=0)
		tkinter.Label(self.root,text="Gender",anchor="w").grid(row=7,column=0)
		tkinter.Label(self.root,text="Address",anchor="w").grid(row=8,column=0)
		self.userid=tkinter.Entry(self.root)
		self.userid.grid(row=0,column=1)
		self.username=tkinter.Entry(self.root)
		self.username.grid(row=1,column=1)
		self.usertype=tkinter.StringVar()
		self.usertype.set("Admin")
		self.ut=tkinter.OptionMenu(self.root,self.usertype,"Admin","User")
		self.ut.grid(row=2,column=1)
		self.userstatus=tkinter.StringVar()
		self.userstatus.set("0")
		self.us0=tkinter.Radiobutton(self.root,text="Active",variable=self.userstatus,value="0")
		self.us0.grid(row=3,column=1)
		self.us1=tkinter.Radiobutton(self.root,text="Inactive",variable=self.userstatus,value="1")
		self.us1.grid(row=3,column=2)
		self.name=tkinter.Entry(self.root)
		self.name.grid(row=4,column=1)
		self.email=tkinter.Entry(self.root)
		self.email.grid(row=5,column=1)
		self.contact=tkinter.Entry(self.root)
		self.contact.grid(row=6,column=1)
		self.gender=tkinter.StringVar()
		self.gender.set("0")
		self.g0=tkinter.Radiobutton(self.root,text="Male",variable=self.gender,value="0")
		self.g0.grid(row=7,column=1)
		self.g1=tkinter.Radiobutton(self.root,text="Female",variable=self.gender,value="1")
		self.g1.grid(row=7,column=2)
		self.address=tkinter.Text(self.root,height=4,width=15)
		self.address.grid(row=8,column=1)
		self.btn_first=tkinter.Button(self.root,text="First",width=10,command=self.btn_first_clicked)
		self.btn_first.grid(row=9,column=0,pady=20)
		self.btn_previous=tkinter.Button(self.root,text="Previous",width=10,command=self.btn_previous_clicked)
		self.btn_previous.grid(row=9,column=1)
		self.btn_next=tkinter.Button(self.root,text="Next",width=10,command=self.btn_next_clicked)
		self.btn_next.grid(row=9,column=2)
		self.btn_last=tkinter.Button(self.root,text="Last",width=10,command=self.btn_last_clicked)
		self.btn_last.grid(row=9,column=3)
		self.btn_add=tkinter.Button(self.root,text="Add",width=10,command=self.btn_add_clicked)
		self.btn_add.grid(row=10,column=0)
		self.btn_edit=tkinter.Button(self.root,text="Edit",width=10,command=self.btn_edit_clicked)
		self.btn_edit.grid(row=10,column=1)
		self.btn_save=tkinter.Button(self.root,text="Save",width=10,command=self.btn_save_clicked)
		self.btn_save.grid(row=10,column=2)
		self.btn_cancel=tkinter.Button(self.root,text="Cancel",width=10,command=self.btn_cancel_clicked)
		self.btn_cancel.grid(row=10,column=3)
		self.userlist=UMS.view()
		self.current_index=0
		self.btn_save.config(state="disabled")
		self.showrecord()
		self.add_edit_flag="view"
		self.root.mainloop()
	
	def enableALL(self):
		self.userid.config(state="normal")
		self.username.config(state="normal")
		self.ut.config(state="normal")
		self.us0.config(state="normal")
		self.us1.config(state="normal")
		self.name.config(state="normal")
		self.email.config(state="normal")
		self.contact.config(state="normal")
		self.g0.config(state="normal")
		self.g1.config(state="normal")
		self.address.config(state="normal")
		
	def disableALL(self):
		self.userid.config(state="disabled")
		self.username.config(state="disabled")
		self.ut.config(state="disabled")
		self.us0.config(state="disabled")
		self.us1.config(state="disabled")
		self.name.config(state="disabled")
		self.email.config(state="disabled")
		self.contact.config(state="disabled")
		self.g0.config(state="disabled")
		self.g1.config(state="disabled")
		self.address.config(state="disabled")
	
	def showrecord(self):
		self.enableALL()
		usr=self.userlist[self.current_index]
		self.userid.delete(0,"end")
		self.userid.insert(0,str(usr.getUserid()))
		self.username.delete(0,"end")
		self.username.insert(0,usr.getUsername())
		self.usertype.set(usr.getUsertype())
		if usr.getUserstatus()==1:
			self.userstatus.set("1")
		else:
			self.userstatus.set("0")
		self.name.delete(0,"end")
		self.name.insert(0,usr.getName())
		self.email.delete(0,"end")
		self.email.insert(0,usr.getEmail())
		self.contact.delete(0,"end")
		self.contact.insert(0,usr.getContact())
		if usr.getGender()==0:
			self.gender.set("0")
		else:
			self.gender.set("1")
		self.address.delete(1.0,"end")
		self.address.insert(1.0,usr.getAddress())
		self.disableALL()
		self.btn_first.config(state="normal")
		self.btn_previous.config(state="normal")
		self.btn_next.config(state="normal")
		self.btn_last.config(state="normal")
		if self.current_index==0:
			self.btn_first.config(state="disabled")
			self.btn_previous.config(state="disabled")
		if self.current_index==len(self.userlist)-1:
			self.btn_last.config(state="disabled")
			self.btn_next.config(state="disabled")
			
	def btn_first_clicked(self):
		self.current_index=0
		self.showrecord()
	def btn_previous_clicked(self):
		self.current_index=self.current_index-1
		self.showrecord()
	def btn_next_clicked(self):
		self.current_index=self.current_index+1
		self.showrecord()
	def btn_last_clicked(self):
		self.current_index=len(self.userlist)-1
		self.showrecord()
		
	def btn_add_clicked(self):
		self.add_edit_flag="add"
		self.enableALL()
		self.btn_save.config(state="normal")
		self.userid.delete(0,"end")
		self.userid.config(state="disabled")
		self.btn_first.config(state="disabled")
		self.btn_previous.config(state="disabled")
		self.btn_next.config(state="disabled")
		self.btn_last.config(state="disabled")
		self.btn_edit.config(state="disabled")
		self.btn_add.config(state="disabled")
		self.username.delete(0,"end")
		self.name.delete(0,"end")
		self.email.delete(0,"end")
		self.contact.delete(0,"end")
		self.address.delete(1.0,"end")
		self.userstatus.set("0")
		self.gender.set("0")
		self.usertype.set("Admin")
		
	def btn_edit_clicked(self):
		self.add_edit_flag="edit"
		self.enableALL()
		self.btn_save.config(state="normal")
		self.userid.config(state="disabled")
		self.username.config(state="disabled")
		self.btn_first.config(state="disabled")
		self.btn_previous.config(state="disabled")
		self.btn_next.config(state="disabled")
		self.btn_last.config(state="disabled")
		self.btn_edit.config(state="disabled")
		self.btn_add.config(state="disabled")
		
	def btn_save_clicked(self):
		usr=User()
		usr.setUsertype(self.usertype.get())
		usr.setUserstatus(int(self.userstatus.get()))
		usr.setName(self.name.get())
		usr.setEmail(self.email.get())
		usr.setContact(self.contact.get())
		usr.setAddress(self.address.get(1.0,"end"))
		usr.setGender(int(self.gender.get()))
		if self.add_edit_flag=="add":
			usr.setUsername(self.username.get())
			usr.setPassword("user")
			if UMS.add(usr)==True:
				messagebox.showinfo("Add User","User record added Succesfully, default password is 'user'")
			else:
				messagebox.showerror("Add User","User record already exists")
		elif self.add_edit_flag=="edit":
			self.userid.config(state="normal")
			usr.setUserid(self.userid.get())
			self.userid.config(state="disabled")
			if UMS.updateUser(usr):
				messagebox.showinfo("Edit user record","User record updated successfully")
			else:
				messagebox.showerror("Edit user record","Error")
		self.btn_save.config(state="disabled")
		self.btn_add.config(state="normal")
		self.btn_edit.config(state="normal")
		self.userlist=UMS.view()
		if self.add_edit_flag=="add":
			self.current_index=len(self.userlist)-1
		self.add_edit_flag="view"
		self.showrecord()
		
			
	def btn_cancel_clicked(self):
		if self.add_edit_flag=="view":
			self.root.destroy()
			MainFrame(self.uid)
		else:
			self.showrecord()
			self.add_edit_flag="view"
			self.btn_save.config(state="disabled")
			self.btn_add.config(state="normal")
			self.btn_edit.config(state="normal")

class ManageProfile:
	def __init__(self,uid):
		self.uid=uid
		self.root=tkinter.Tk()
		self.root.title("Manage User")
		self.root.geometry("500x400")
		tkinter.Label(self.root,text="User ID",anchor="w").grid(row=0,column=0,padx=30)
		tkinter.Label(self.root,text="Username",anchor="w").grid(row=1,column=0)
		tkinter.Label(self.root,text="Name",anchor="w").grid(row=2,column=0)
		tkinter.Label(self.root,text="Email",anchor="w").grid(row=3,column=0)
		tkinter.Label(self.root,text="Contact",anchor="w").grid(row=4,column=0)
		tkinter.Label(self.root,text="Gender",anchor="w").grid(row=5,column=0)
		tkinter.Label(self.root,text="Address",anchor="w").grid(row=6,column=0)
		self.userid=tkinter.Entry(self.root)
		self.userid.grid(row=0,column=1)
		self.username=tkinter.Entry(self.root)
		self.username.grid(row=1,column=1)
		self.name=tkinter.Entry(self.root)
		self.name.grid(row=2,column=1)
		self.email=tkinter.Entry(self.root)
		self.email.grid(row=3,column=1)
		self.contact=tkinter.Entry(self.root)
		self.contact.grid(row=4,column=1)
		self.gender=tkinter.StringVar()
		self.gender.set("0")
		self.g0=tkinter.Radiobutton(self.root,text="Male",variable=self.gender,value="0")
		self.g0.grid(row=5,column=1)
		self.g1=tkinter.Radiobutton(self.root,text="Female",variable=self.gender,value="1")
		self.g1.grid(row=5,column=2)
		self.address=tkinter.Text(self.root,height=4,width=15)
		self.address.grid(row=6,column=1)
		self.btn_edit=tkinter.Button(self.root,text="Edit",width=10,command=self.btn_edit_clicked)
		self.btn_edit.grid(row=7,column=0,pady=20)
		self.btn_save=tkinter.Button(self.root,text="Save",width=10,command=self.btn_save_clicked)
		self.btn_save.grid(row=7,column=1)
		self.btn_cancel=tkinter.Button(self.root,text="Cancel",width=10,command=self.btn_cancel_clicked)
		self.btn_cancel.grid(row=7,column=2)
		self.usr=UMS.search(self.uid)
		self.btn_save.config(state="disabled")
		self.add_edit_flag="view"
		self.showrecord()
		self.root.mainloop()
	
	def enableALL(self):
		self.userid.config(state="normal")
		self.username.config(state="normal")
		self.name.config(state="normal")
		self.email.config(state="normal")
		self.contact.config(state="normal")
		self.g0.config(state="normal")
		self.g1.config(state="normal")
		self.address.config(state="normal")
		
	def disableALL(self):
		self.userid.config(state="disabled")
		self.username.config(state="disabled")
		self.name.config(state="disabled")
		self.email.config(state="disabled")
		self.contact.config(state="disabled")
		self.g0.config(state="disabled")
		self.g1.config(state="disabled")
		self.address.config(state="disabled")
	
	def showrecord(self):
		self.enableALL()
		self.userid.delete(0,"end")
		self.userid.insert(0,str(self.usr.getUserid()))
		self.username.delete(0,"end")
		self.username.insert(0,self.usr.getUsername())
		self.name.delete(0,"end")
		self.name.insert(0,self.usr.getName())
		self.email.delete(0,"end")
		self.email.insert(0,self.usr.getEmail())
		self.contact.delete(0,"end")
		self.contact.insert(0,self.usr.getContact())
		if self.usr.getGender()==0:
			self.gender.set("0")
		else:
			self.gender.set("1")
		self.address.delete(1.0,"end")
		self.address.insert(1.0,self.usr.getAddress())
		self.disableALL()
		
	def btn_edit_clicked(self):
		self.add_edit_flag="edit"
		self.enableALL()
		self.btn_save.config(state="normal")
		self.username.config(state="normal")
		self.userid.config(state="disabled")
		self.btn_edit.config(state="disabled")
		
	def btn_save_clicked(self):
		self.userid.config(state="normal")
		usr=User()
		usr.setUserid(self.userid.get())
		self.userid.config(state="disabled")
		usr.setName(self.name.get())
		usr.setEmail(self.email.get())
		usr.setContact(self.contact.get())
		usr.setAddress(self.address.get(1.0,"end"))
		usr.setGender(int(self.gender.get()))
		if UMS.updateProfile(usr):
			messagebox.showinfo("Edit user record","User record updated successfully")
		else:
			messagebox.showerror("Edit user record","Error")
		self.btn_save.config(state="disabled")
		self.btn_edit.config(state="normal")
		self.usr=UMS.search(self.uid)
		self.showrecord()
		
	def btn_cancel_clicked(self):
		if self.add_edit_flag=="view":
			self.root.destroy()
			MainFrame(self.uid)
		else:
			self.showrecord()
			self.add_edit_flag="view"
			self.btn_save.config(state="disabled")
			self.btn_edit.config(state="normal")
			
class StartServer:
	def __init__(self):
		self.root=tkinter.Tk()
		self.root.title("Start server")
		self.root.geometry("300x150")
		tkinter.Label(self.root,text="Port Number").grid(row=0,column=0,padx=20,pady=20)
		self.portno=tkinter.Entry(self.root)
		self.portno.grid(row=0,column=1)
		self.btn_start=tkinter.Button(self.root,text="Start",width=15,command=self.btn_start_clicked)
		self.btn_start.grid(row=1,columnspan=2,pady=5)
		self.label=tkinter.Label(self.root)
		self.label.grid(row=2,column=0,pady=5)
		self.portno.bind("<Return>",self.btn_start_clicked)
		self.root.mainloop()
		
	def btn_start_clicked(self,event=None):
		self.s=socket.socket()
		self.s.bind(("",int(self.portno.get())))
		self.label.config(text="Socket server created")
		self.s.listen(10)
		self.label.config(text="Waiting for client request...")
		self.btn_start.config(state="disabled")
		self.portno.config(state="disabled")
		
		self.t1=Thread(target=self.connection)
		self.t1.start()
		
	def connection(self):
		i=1
		while i<=10:
			self.conn,self.addr=self.s.accept()
			self.label.config(text="Clients connected : "+str(i))
			tkinter.Label(self.root,text="connected to"+str(self.addr)).grid(row=i+2,column=0)
			c=Choice(self.conn)
			c.start()
			i+=1
			
class Choice(Thread):
	def __init__(self,conn):
		Thread.__init__(self)
		self.conn=conn
	def upload(self,conn):
		os.chdir("uploaded_files")
		dir_uname=self.conn.recv(1024).decode("latin-1")
		print(dir_uname)
		self.conn.send("ack".encode("latin-1"))
		if os.path.exists(dir_uname)==False:
			os.mkdir(dir_uname)
		os.chdir(dir_uname)
		no_of_files=self.conn.recv(1024).decode("latin-1")
		print(no_of_files)
		self.conn.send("ack".encode("latin-1"))
		for i in range(int(no_of_files)):
			filename=self.conn.recv(1024).decode("latin-1")
			print(filename)
			self.conn.send("ack".encode("latin-1"))
			'''i=1
			a=filename
			while True:
				if os.path.exists(a):
					f=os.path.splitext(filename)[0]
					f=f+str(i)
					a=f+(a.split(".")[-1])
				else:
					break
					'''
			f=open(filename,"wb")
			data=self.conn.recv(4096)
			while data:
				f.write(data)
				data=self.conn.recv(4096)
				if data==b"done":
					break
			f.close()
			print("done")
			type=(filename.split(".")[-1])
			f_name=os.path.splitext(filename)[0]
			date=(datetime.now()).strftime("%d-%m-%Y %H:%M")
			size=str((os.path.getsize(filename))//1024)+" KB"
			UMS.updateFiles(dir_uname,f_name,date,type,size)
		os.chdir("..")
		os.chdir("..")
		messagebox.showinfo("Recieve","File recieved succesfully")	

	def download(self,conn):
		os.chdir("uploaded_files")
		dir_uname=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		os.chdir(dir_uname)
		no_of_files=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		for i in range(int(no_of_files)):
			filename=self.conn.recv(1024).decode("latin-1")
			self.conn.send("ack".encode("latin-1"))
			f=open(filename,"rb")
			data=f.read(4096)
			while data:
				self.conn.send(data)
				data=f.read(4096)
			f.close()
			self.conn.send(b"done")
		messagebox.showinfo("Sent",filename+"sent succesfully")
		os.chdir("..")
		os.chdir("..")
			
	def remove(self,conn):
		os.chdir("uploaded_files")
		dir_uname=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		os.chdir(dir_uname)
		no_of_files=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		for i in range(int(no_of_files)):
			filename=self.conn.recv(1024).decode("latin-1")
			self.conn.send("ack".encode("latin-1"))
			os.remove(filename)
			print("deleted from server")
			f_name=os.path.splitext(filename)[0]
			UMS.deleteFile(dir_uname,f_name)
			print("deleted from database")
		os.chdir("..")
		os.chdir("..")
			
	def rename(self,conn):
		os.chdir("uploaded_files")
		dir_uname=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		os.chdir(dir_uname)
		filename=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		f_name=os.path.splitext(filename)[0]
		extension="."+filename.split(".")[-1]
		new_filename=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		os.rename(filename,new_filename+str(extension))
		UMS.renameFile(dir_uname,f_name,new_filename)
		os.chdir("..")
		os.chdir("..")
	def run(self):
		while True:
			choice=self.conn.recv(1024).decode("latin-1")
			self.conn.send("ack".encode("latin-1"))
			if choice=="upload":
				self.upload(self.conn)
			elif choice=="download":
				self.download(self.conn)
			elif choice=="remove":
				elf.remove(self.conn)
			elif choice=="rename":
				self.rename(self.conn)
			elif choice=="share":
				pass
		

'''			
class Upload(Thread):
	def __init__(self,conn):
		Thread.__init__(self)
		self.conn=conn
	def run(self):
		os.chdir("uploaded_files")
		dir_uname=self.conn.recv(1024).decode("latin-1")
		print(dir_uname)
		self.conn.send("ack".encode("latin-1"))
		if os.path.exists(dir_uname)==False:
			os.mkdir(dir_uname)
		os.chdir(dir_uname)
		no_of_files=self.conn.recv(1024).decode("latin-1")
		print(no_of_files)
		self.conn.send("ack".encode("latin-1"))
		for i in range(int(no_of_files)):
			filename=self.conn.recv(1024).decode("latin-1")
			print(filename)
			self.conn.send("ack".encode("latin-1"))
			f=open(filename,"wb")
			data=self.conn.recv(4096)
			while data:
				f.write(data)
				data=self.conn.recv(4096)
				if data==b"done":
					break
			f.close()
			print("done")
			type=(filename.split(".")[-1])
			f_name=os.path.splitext(filename)[0]
			date=(datetime.now()).strftime("%d-%m-%Y %H:%M")
			size=str((os.path.getsize(filename))//1024)+" KB"
			UMS.updateFiles(dir_uname,f_name,date,type,size)
		os.chdir("..")
		os.chdir("..")
		messagebox.showinfo("Recieve","File recieved succesfully")	
		
class Download(Thread):
	def __init__(self,conn):
		Thread.__init__(self)
		self.conn=conn
	def run(self):
		os.chdir("uploaded_files")
		dir_uname=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		os.chdir(dir_uname)
		no_of_files=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		for i in range(int(no_of_files)):
			filename=self.conn.recv(1024).decode("latin-1")
			self.conn.send("ack".encode("latin-1"))
			f=open(filename,"rb")
			data=f.read(4096)
			while data:
				self.conn.send(data)
				data=f.read(4096)
			f.close()
			self.conn.send(b"done")
			messagebox.showinfo("Sent",filename+"sent succesfully")
		os.chdir("..")
		os.chdir("..")
		
class Remove(Thread):
	def __init__(self,conn):
		Thread.__init__(self)
		self.conn=conn
	def run(self):
		os.chdir("uploaded_files")
		dir_uname=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		os.chdir(dir_uname)
		no_of_files=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		for i in range(int(no_of_files)):
			filename=self.conn.recv(1024).decode("latin-1")
			self.conn.send("ack".encode("latin-1"))
			os.remove(filename)
			print("deleted from server")
			f_name=os.path.splitext(filename)[0]
			UMS.deleteFile(dir_uname,f_name)
			print("deleted from database")
		os.chdir("..")
		os.chdir("..")
		
class Rename(Thread):
	def __init__(self,conn):
		Thread.__init__(self)
		self.conn=conn
	def run(self):
		os.chdir("uploaded_files")
		dir_uname=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		os.chdir(dir_uname)
		filename=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		f_name=os.path.splitext(filename)[0]
		extension="."+filename.split(".")[-1]
		new_filename=self.conn.recv(1024).decode("latin-1")
		self.conn.send("ack".encode("latin-1"))
		os.rename(filename,new_filename+str(extension))
		UMS.renameFile(dir_uname,f_name,new_filename)
		os.chdir("..")
		os.chdir("..")
			
'''
