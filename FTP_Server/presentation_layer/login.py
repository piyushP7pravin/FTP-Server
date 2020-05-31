import Main_Frame
import sys
sys.path.append("..")
from data_layer.user import User
import tkinter
from tkinter import messagebox
from logical_layer.loginservices import Authentication

class Login:
	def __init__(self):
		self.root=tkinter.Tk()
		self.root.title("FTP Server")
		self.root.configure(bg="gray99")
		self.root.geometry("400x200")
		tkinter.Label(self.root,text="Username",bg="gray99",font=("Calibri Light",12)).place(x=65,y=30)
		tkinter.Label(self.root,text="Password",bg="gray99",font=("Calibri Light",12)).place(x=65,y=70)
		
		self.username=tkinter.Entry(self.root,relief="flat",bg="white",highlightbackground="gray",highlightthicknes=1,highlightcolor="RoyalBlue2",font=("Calibri Light",12))
		self.username.place(x=155,y=30,height=32)
		def on_enter_un(event=None):
			self.username.config(highlightbackground="RoyalBlue2",highlightthicknes=2)
		def on_leave_un(event=None):
			self.username.config(highlightbackground="gray",highlightthicknes=1)
		self.username.bind("<Enter>",on_enter_un)
		self.username.bind("<Leave>",on_leave_un)
		
		self.__password=tkinter.Entry(self.root,relief="flat",show="*",bg="white",highlightbackground="gray",highlightthicknes=1,highlightcolor="RoyalBlue2",font=("Calibri Light",12))
		self.__password.place(x=155,y=70,height=32)
		self.__password.bind("<Return>",self.btn_login_clicked)
		def on_enter_pd(event=None):
			self.__password.config(highlightbackground="RoyalBlue2",highlightthicknes=2)
		def on_leave_pd(event=None):
			self.__password.config(highlightbackground="gray",highlightthicknes=1)
		self.__password.bind("<Enter>",on_enter_pd)
		self.__password.bind("<Leave>",on_leave_pd)
		
		self.btn_login=tkinter.Button(self.root,text="Login",width=9,relief="flat",bg="RoyalBlue2",fg="gray99",font=("Calibri Light",16,"bold"),command=self.btn_login_clicked)
		self.btn_login.place(x=65,y=120,height=35)
		self.btn_clear=tkinter.Button(self.root,text="Clear",width=9,relief="flat",bg="RoyalBlue2",fg="gray99",font=("Calibri Light",16,"bold"),command=self.btn_clear_clicked)
		self.btn_clear.place(x=200,y=120,height=35)
		def on_enter_btn_lg(event):
			self.btn_login.config(bg="SkyBlue1")
		def on_leave_btn_lg(event):
			self.btn_login.config(bg="RoyalBlue2")
		self.btn_login.bind("<Enter>",on_enter_btn_lg)
		self.btn_login.bind("<Leave>",on_leave_btn_lg)
		def on_enter_btn_cl(event):
			self.btn_clear.config(bg="SkyBlue1")
		def on_leave_btn_cl(event):
			self.btn_clear.config(bg="RoyalBlue2")
		self.btn_clear.bind("<Enter>",on_enter_btn_cl)
		self.btn_clear.bind("<Leave>",on_leave_btn_cl)
		
		self.root.mainloop()
	def btn_login_clicked(self,event=None):
		uname=self.username.get()
		uid=Authentication.loginCheck(uname,self.__password.get())
		if uid!=-1:
			if self.__password.get()=="user":
				self.root.destroy()
				Main_Frame.ChangePass(uid)
			else:   
				self.root.destroy()
				Main_Frame.MainFrame(uid,uname)
		else:
			messagebox.showerror("Error","Wrong username or password")
			self.root.destroy()
			Login()
	def btn_clear_clicked(self):
		self.username.delete(0,"end")
		self.__password.delete(0,"end")
if __name__=="__main__":
	Login()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	