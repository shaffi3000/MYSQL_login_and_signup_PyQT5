#all imports below are standed for every PyQt5 project. 
import mysql.connector
import sys, os, time, uuid, hashlib, re
from PyQt5 import QtCore, QtGui, uic  
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QComboBox, QTextEdit   ###imports all the modules (files stored as part of PyQt5 dowloand) needed to 

winHome = uic.loadUiType("UI_files\homeScreen.ui") [0]  ##this links the userinterface files to the program
winSignUp = uic.loadUiType("UI_files\signup.ui")[0]
winLogin = uic.loadUiType("UI_files\login.ui")[0]

class HomeWin(QtWidgets.QMainWindow, winHome):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.signupBtn.clicked.connect(self.signup)
        self.loginBtn.clicked.connect(self.login)

    def login(self):
        self.hide()
        self.newWindow = winLogin
        self.newWindow.show()

    def signup(self):
        self.hide()
        self.newWindow = winSignUp
        self.newWindow.show()



class SignUpWin(QtWidgets.QMainWindow, winSignUp):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.signupbtn.clicked.connect(self.signup)

    def signup(self):
        valid = False
        while not valid:
            user.username = self.unameSTxt.text()
            user.password = self.passwordSTxt.text()
            user.email = self.emailTxt.text()
            if user.username and user.password and user.email:
                valid = True

        hashedUserpass = hasher.hashPassword(user.password) 
        dbActions.addToDb(user.username, hashedUserpass, user.email)
        ##display message, go back to login 
        self.login()

    def login(self):
        self.hide()
        self.newWindow = winLogin
        self.newWindow.show()



class User():
    def __init__(self):
        self.username = None
        self.password = None
        self.email = None 
        self.loggedIn = False

user = User()


class LoginWin(QtWidgets.QMainWindow, winLogin):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.loginBtn.clicked.connect(self.login)

    def login(self):
        valid = False
        loggedIn = False
        while not valid:
            user.username = self.unameTxt.text()
            user.password = self.passwdTxt.text()
            if user.username and user.password:
                valid = True
                print('Validated \n')
        while not loggedIn:
            sql = f"""SELECT password FROM users WHERE username='{user.username}'"""
            dbActions.execute(sql)
            items = dbActions.dbCur.fetchone()
            print(items)
            if items:
                dbPassword = items[0]
                match = hasher.verifyhash(user.password, dbPassword)
                if match:
                    loggedIn = True
                    print('You are now logged in. ')
                else:
                    print('The password doesnt match')
            else:
                print('Sorry, I could not find you ')
                




class DBCon():
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = os.environ.get('dbPassword')
        self.dataBase = 'DBUsers'
        self.cur = None
        self.con = None

    def getCon(self):
        self.con = mysql.connector.connect(
        host = self.host,
        user = self.user,
        password =f"{self.password}",
        database= self.dataBase
        )

        self.cur = self.con.cursor()

    def closeDB(self):
        self.con.close()


    def showDatabases(self):
        self.cur.execute('SHOW DATABASES')
        dbs = self.cur.fetchall()
        print(dbs)
# dataB.showDatabases()

class DatabaseActions():
    def __init__(self):
        self.dbCur = dataB.cur
        self.dbCon = dataB.con


    def addToDb(self, username, HashedPassword, email):
        try:
            sql = f"""INSERT INTO `users` VALUES ('{username}', '{HashedPassword}','{email}')"""
            self.dbCur.execute(sql)
            self.commit1()
        except:
            print('Did not insert')
        else:
            print('All done :) ')


    def commit1(self):
        self.dbCon.commit()

    def execute(self, sqlCommand):
        self.dbCur.execute(sqlCommand)

class HashingPasswords():

    def hashPassword(self, password):
        salt = uuid.uuid4().hex
        hashedPassword = hashlib.sha256(salt.encode()+password.encode()).hexdigest()+":"+salt

        return hashedPassword


    def verifyhash(self, userpass, storedpass):   #Verifies the hash
        try:   #Prevents crash in instance of invalid stored hash
            password,salt=storedpass.split(":")
        except:
            pass
        else:
            data = []
            data.append(password)
            data.append(hashlib.sha256(salt.encode()+userpass.encode()).hexdigest())
        
        return data[0]==data[1]




dataB = DBCon()
dataB.getCon()
dbActions = DatabaseActions()
hasher = HashingPasswords()

app = QtWidgets.QApplication(sys.argv)
winHome = HomeWin()
winSignUp = SignUpWin()
winLogin = LoginWin()




 #think of this as the 'main ()' section in procedural programming. Allows you to call the program into action 

winHome.show()
app.exec_()