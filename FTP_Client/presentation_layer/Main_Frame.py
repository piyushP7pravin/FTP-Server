import sys
import login
sys.path.append("..")
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
from logical_layer.loginservices import Authentication
from logical_layer.umsservices import *
from data_layer.user import User
from presentation_layer.login import Login
import socket
from threading import Thread
import os

class MainFrame:
	def __init__(self,uid,uname):
		self.uid=uid
		self.uname=uname
		self.s=socket.socket()
		self.s.connect(("localhost",12345))
		self.root=tkinter.Tk()
		self.root.title("FTP Client")
		self.root.geometry("500x200")
		self.menubar=tkinter.Menu(self.root)
		self.logoutmenu=tkinter.Menu(self.menubar,tearoff=0)
		self.logoutmenu.add_command(label="Logout",command=self.menu_logout_clicked)
		self.logoutmenu.add_command(label="Change Password",command=self.menu_changepass_clicked)
		self.menubar.add_cascade(label="Logout",menu=self.logoutmenu)
		
		self.umsmenu=tkinter.Menu(self.menubar,tearoff=0)
		self.umsmenu.add_command(label="Manage User",command=self.menu_manageuser_clicked)
		self.umsmenu.add_command(label="Manage Profile",command=self.menu_manageprofile_clicked)
		self.menubar.add_cascade(label="UMS",menu=self.umsmenu)
		
		self.filemenu=tkinter.Menu(self.menubar,tearoff=0)
		self.filemenu.add_command(label="Upload",command=self.menu_upload_clicked)
		self.filemenu.add_command(label="Download",command=self.menu_download_clicked)
		self.menubar.add_cascade(label="File Manager",menu=self.filemenu)
		
		self.root.config(menu=self.menubar)
		self.root.mainloop()
		
	def menu_logout_clicked(self):
		self.s.close()
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
	def menu_upload_clicked(self):
		UploadFile(self.uid,self.uname,self.s)
	def menu_download_clicked(self):
		DownloadFile(self.uid,self.uname,self.s)
	
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

class UploadFile:
	def __init__(self,uid,uname,s):
		self.uid=uid
		self.uname=uname
		self.s=s
		self.root=tkinter.Tk()
		self.root.title("Upload file")
		self.root.geometry("400x150")
		self.path=tkinter.Entry(self.root,width=30)
		self.path.grid(row=0,column=0,padx=20,pady=20)
		self.btn_select=tkinter.Button(self.root,text="Select File",command=self.btn_select_clicked)
		self.btn_select.grid(row=0,column=1)
		self.btn_upload=tkinter.Button(self.root,text="Upload",command=self.btn_upload_clicked)
		self.btn_upload.grid(row=1,columnspan=2,pady=10)
		self.btn_upload.config(state="disabled")
		self.root.mainloop()
		
	def btn_select_clicked(self):
		self.path.insert(0,filedialog.askopenfilenames())
		self.btn_upload.config(state="normal")
		
	def btn_upload_clicked(self):
		print("Upload clicked")
		self.s.send("upload".encode("latin-1"))
		print("upload send")
		self.s.recv(1024).decode("latin-1")
		print("ack recieved")
		self.s.send(self.uname.encode("latin-1"))
		print("username send")
		self.s.recv(1024).decode("latin-1")
		print("ack recived")
		file_path_list=self.root.tk.splitlist(self.path.get())
		no_of_files=len(file_path_list)
		self.s.send(str(no_of_files).encode("latin-1"))
		print(no_of_files)
		self.s.recv(1024).decode("latin-1")
		for file_path in file_path_list:
			filename=file_path.split("/")[-1]
			self.s.send(filename.encode("latin-1"))
			print(filename+" send")
			self.s.recv(1024).decode("latin-1")
			f=open(file_path,"rb")
			data=f.read(4096)
			while data:
				self.s.send(data)
				print("file uploading")
				print("****")
				data=f.read(4096)
			f.close()
			self.s.send(b"done")
			print("done")
		messagebox.showinfo("Upload File","File uploaded succesfully")
		self.root.destroy()
		
			
class DownloadFile:
	def __init__(self,uid,uname,s):
		self.uid=uid
		self.s=s
		self.uname=uname
		self.root=tkinter.Tk()
		self.root.title("Download file")
		self.root.geometry("500x400")
		
		self.l_frame1=tkinter.Frame(self.root,height=30,width=500)
		self.l_frame1.place(x=0,y=0)
		
		'''self.l_frame2=tkinter.Frame(self.root,height=30,width=500)
		self.l_frame2.place(x=500,y=0)'''
		
		self.l1=tkinter.Label(self.l_frame1,text="Uploaded Files",font=4,anchor="w",width=71,bg="lightblue")
		self.l1.pack(side="left",fill="y")
		'''self.l2=tkinter.Label(self.l_frame2,text="Shared Files",font=4,anchor="w",width=71,bg="lightblue")
		self.l2.pack(side="left",fill="y")'''
		
		
		self.uploaded_file_frame=tkinter.Frame(self.root,height=340,width=500,bg="white")
		self.uploaded_file_frame.place(x=0,y=30)
		
		'''self.shared_file_frame=tkinter.Frame(self.root,height=340,width=500,bg="white")
		self.shared_file_frame.place(x=500,y=30)'''
		
		self.button_frame=tkinter.Frame(self.root,height=40,width=1000,bg="white")
		self.button_frame.place(x=0,y=370)
		
		self.tree=ttk.Treeview(self.uploaded_file_frame,height=15,columns=["Date","Type","Size"])
		self.tree.pack(side="left",fill="both",expand=True)
		self.tree.heading("#0",text="Name")
		self.tree.heading("Date",text="Date")
		self.tree.heading("Type",text="Type")
		self.tree.heading("Size",text="Size")
		self.tree.column("Date",width=120)
		self.tree.column("Type",width=60)
		self.tree.column("Size",width=100)
		
		for i in UMS.viewFiles(self.uname):
			self.tree.insert("","end",i[0],text=i[0],values=(i[1],i[2].upper(),i[3]))
			
		self.scroll=ttk.Scrollbar(self.uploaded_file_frame,orient="vertical",command=self.tree.yview)
		self.scroll.pack(side="right",fill="y")
		self.tree.configure(yscrollcommand=self.scroll.set)
		
		self.btn_download=tkinter.Button(self.button_frame,text="Download",width=22,command=self.btn_download_clicked)
		self.btn_download.grid(row=0,column=0)
		self.btn_remove=tkinter.Button(self.button_frame,text="Remove",width=22,command=self.btn_remove_clicked)
		self.btn_remove.grid(row=0,column=1)
		self.btn_rename=tkinter.Button(self.button_frame,text="Rename",width=22,command=self.btn_rename_clicked)
		self.btn_rename.grid(row=0,column=2)
		
		self.root.mainloop()

	def btn_download_clicked(self):
		self.s.send("download".encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		self.s.send(self.uname.encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		files=self.tree.selection()
		no_of_files=len(files)
		self.s.send(str(no_of_files).encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		download_dir=filedialog.askdirectory(initialdir="C:/Users/Piyush Pravin/Downloads")
		os.chdir(download_dir)
		for f_name in files:
			filename=f_name+"."+UMS.getFileType(self.uname,f_name)
			self.s.send(filename.encode("latin-1"))
			self.s.recv(1024).decode("latin-1")
			f=open(filename,"wb")
			data=self.s.recv(4096)
			while data:
				f.write(data)
				data=self.s.recv(4096)
				if data==b"done":
					break
			f.close()
			messagebox.showinfo("Downloaded",filename+"downloaded succesfully")
		
	def btn_remove_clicked(self):
		self.s.send("remove".encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		self.s.send(self.uname.encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		files=self.tree.selection()
		no_of_files=len(files)
		self.s.send(str(no_of_files).encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		if messagebox.askquestion("Delete File","Are you sure you want to permanently delete selected file(s)?")=="yes":
			for f_name in files:
				filename=f_name+"."+UMS.getFileType(self.uname,f_name)
				self.s.send(filename.encode("latin-1"))
				self.s.recv(1024).decode("latin-1")
				self.tree.delete(f_name)
			messagebox.showinfo("Deleted",str(files)+"deleted succesfully") 
	def btn_rename_clicked(self):
		self.s.send("rename".encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		self.s.send(self.uname.encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		file=self.tree.selection()
		
		f_name=file[0]
		filename=f_name+"."+UMS.getFileType(self.uname,f_name)
		self.s.send(filename.encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		new_filename=simpledialog.askstring(title="Rename",prompt="Enter new filename :                    ",initialvalue=f_name)
		print(new_filename)
		self.s.send(new_filename.encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		self.tree.item(f_name,text=new_filename)
		messagebox.showinfo("Rename",filename+" renamed to "+new_filename)
		
'''		
class Upload(Thread):
	def __init__(self,uid,uname,s,root,path):
		Thread.__init__(self)
		self.uid=uid
		self.uname=uname
		self.s=s
		self.root=root
		self.path=path
		
	def run(self):
		print("Upload clicked")
		self.s.send("upload".encode("latin-1"))
		print("upload send")
		self.s.recv(1024).decode("latin-1")
		print("ack recieved")
		self.s.send(self.uname.encode("latin-1"))
		print("username send")
		self.s.recv(1024).decode("latin-1")
		print("ack recived")
		file_path_list=self.root.tk.splitlist(self.path.get())
		no_of_files=len(file_path_list)
		self.s.send(str(no_of_files).encode("latin-1"))
		print(no_of_files)
		self.s.recv(1024).decode("latin-1")
		for file_path in file_path_list:
			filename=file_path.split("/")[-1]
			self.s.send(filename.encode("latin-1"))
			print(filename+" send")
			self.s.recv(1024).decode("latin-1")
			f=open(file_path,"rb")
			data=f.read(4096)
			while data:
				self.s.send(data)
				print("file uploading")
				print("****")
				data=f.read(4096)
			f.close()
			self.s.send(b"done")
			print("done")
		messagebox.showinfo("Upload File","File uploaded succesfully")
		self.root.destroy()

class Download(Thread):
	def __init__(self,uid,uname,s,root,tree):
		Thread.__init__(self)
		self.uid=uid
		self.uname=uname
		self.s=s
		self.root=root
		self.tree=tree
	def run(self):
		self.s.send("download".encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		self.s.send(self.uname.encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		files=self.tree.selection()
		no_of_files=len(files)
		self.s.send(str(no_of_files).encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		download_dir=filedialog.askdirectory(initialdir="C:/Users/Piyush Pravin/Downloads")
		os.chdir(download_dir)
		for f_name in files:
			filename=f_name+"."+UMS.getFileType(self.uname,f_name)
			self.s.send(filename.encode("latin-1"))
			self.s.recv(1024).decode("latin-1")
			f=open(filename,"wb")
			data=self.s.recv(4096)
			while data:
				f.write(data)
				data=self.s.recv(4096)
				if data==b"done":
					break
			f.close()
			messagebox.showinfo("Downloaded",filename+"downloaded succesfully")
		
class Remove(Thread):
	def __init__(self,uid,uname,s,root,tree):
		Thread.__init__(self)
		self.uid=uid
		self.uname=uname
		self.s=s
		self.root=root
		self.tree=tree
	def run(self):
		self.s.send("remove".encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		self.s.send(self.uname.encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		files=self.tree.selection()
		no_of_files=len(files)
		self.s.send(str(no_of_files).encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		if messagebox.askquestion("Delete File","Are you sure you want to permanently delete selected file(s)?")=="yes":
			for f_name in files:
				filename=f_name+"."+UMS.getFileType(self.uname,f_name)
				self.s.send(filename.encode("latin-1"))
				self.s.recv(1024).decode("latin-1")
				self.tree.delete(f_name)
			messagebox.showinfo("Deleted",str(files)+"deleted succesfully") 

class Rename(Thread):
	def __init__(self,uid,uname,s,root,tree):
		Thread.__init__(self)
		self.uid=uid
		self.uname=uname
		self.s=s
		self.root=root
		self.tree=tree
	def run(self):
		self.s.send("rename".encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		self.s.send(self.uname.encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		file=self.tree.selection()
		
		f_name=file[0]
		filename=f_name+"."+UMS.getFileType(self.uname,f_name)
		self.s.send(filename.encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		new_filename=simpledialog.askstring(title="Rename",prompt="Enter new filename : ",initialvalue=f_name)
		print(new_filename)
		self.s.send(new_filename.encode("latin-1"))
		self.s.recv(1024).decode("latin-1")
		self.tree.item(f_name,text=new_filename)
		messagebox.showinfo("Rename",filename+" renamed to "+new_filename)
'''	


		
		