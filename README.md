MIT License
Copyright (c) 2020 Piyush Pravin

# Multi-Client FTP Server 
Implementation of socket programming in Python. Based on 3-Tier Architecture

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://https://github.com/piyushP7pravin/Multi-Client-FTP-Server/issues)
[![Forks](https://img.shields.io/github/forks/piyushP7pravin/Multi-Client-FTP-Server.svg?logo=github)](https://github.com/piyushP7pravin/Multi-Client-FTP-Server/network/members)
[![Stargazers](https://img.shields.io/github/stars/piyushP7pravin/Multi-Client-FTP-Server.svg?logo=github)](https://https://github.com/piyushP7pravin/Multi-Client-FTP-Server/stargazers)
[![Issues](https://img.shields.io/github/issues/piyushP7pravin/Multi-Client-FTP-Server.svg?logo=github)](https://https://github.com/piyushP7pravin/Multi-Client-FTP-Server/issues)
[![MIT License](https://img.shields.io/github/license/piyushP7pravin/Multi-Client-FTP-Server.svg?style=flat-square)](https://https://github.com/piyushP7pravin/Multi-Client-FTP-Server/blob/master/LICENSE)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555)](https://www.linkedin.com/in/piyushp7pravin/)

In the simplest of definitions, an FTP Server (which stands for File Transfer Protocol Server) is a software application which enables the transfer of files from one computer to another. FTP is a way to transfer files to any computer in the world that is connected to the internet.
A FTP Sever has basic two components, viz server and client. A server is a computer program or a device that provides functionality for other programs and devices. Clients who want to share files with each other has to be connect to the server first. 
Multiple users can connect to the FTP server and Upload/Download/Manage their files on server and Additionally provided with UMS(User Management System).

## Project Work Flow
1.	On the start of program, call Login window where all widgets are set from Login.py file.
2.	Now user will enter his/her login credentials. After login it will call main frame where all widgets are set from Mainframe.py
3.	Select desired operation from distinct dropdown menu from Main Frame.
4.	After selecting the desired operation it will call the module of respective operation.
5.	There are mainly two operations User management and chatting.

#### For user management:
We can update our profile and view others profile. If an admin user opens this operation then he /she can add user update user and delete user.
##### For FTP:
Server module will take port number as input and start connection.
Client:  Upload file on server, download file from server, Manage uploaded files, Share files to other users.

6.	If you have to change your password then first you have to login and then select the change password menu and then you have to enter new password and confirmation password and after doing this you will get redirected to login window.

7.	To exit you have to logout first and the click on exit button/cross on login window.


