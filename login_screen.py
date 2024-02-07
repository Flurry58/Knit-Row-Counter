import tkinter as tk
from tkinter import *
from tkinter import ttk
import json
import hashlib
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import b64encode
 

#go into database with all users and check if a user with that username exists already
#idea:
'''
To encrypt the key is not stored in the database, the key is your password. This password is then used to decrypt the data and make it readable.
The Username/password combo will still be used to find the users data but the actual key will be from the user themselves. The salt 
will be stored within the users database. '''

def encrypt(keyin,message, salt=None, genkey=False, user=None):
   if genkey:
      salt = os.urandom(16)
      
      kdf = PBKDF2HMAC(
          algorithm=hashes.SHA256(),
          length=32,
          salt=salt,
          iterations=390000,
      )
      
      key = base64.urlsafe_b64encode(kdf.derive(keyin))
      f = Fernet(key)
      new_data = {
        user: b64encode(salt).decode('utf-8')

      } 
      print(new_data)
      
      with open(r"C:\Users\logan\OneDrive\Documents\Coding Projects\Row Counter\data.json", "r") as file:
        file_data = json.load(file)
        file_data["sals"].update(new_data)
        file.close()

      with open(r"C:\Users\logan\OneDrive\Documents\Coding Projects\Row Counter\data.json", "w") as file:
        json.dump(file_data, file)
        file.close()

      token = f.encrypt(str.encode(message))
      return token, salt
   
   else:
      str.encode(salt)
      kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=salt,
      iterations=390000)
      key = base64.urlsafe_b64encode(kdf.derive(keyin))
      f = Fernet(key)
      token = f.encrypt(b"Secret message!")
      return token, salt



def decrypt(keyin, salt, message):
  kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000)
  key = base64.urlsafe_b64encode(kdf.derive(keyin))
  f = Fernet(key)
  output = f.decrypt(message)
  return output


#get users salt data
def getsal(user):
  with open(r"C:\Users\logan\OneDrive\Documents\Coding Projects\Row Counter\data.json", "r") as file:
    file_data = json.load(file)
    file.close()
  salt = file_data["sals"][user]
  return salt

def read_names_json(MainUser=None):
  nameList = []
  with open(r"C:\Users\logan\OneDrive\Documents\Coding Projects\Row Counter\data.json", "r") as file:
    data = json.load(file)
    for names in data["containers"][MainUser]:
      nameList.append(names)
  
  return nameList


#encrypt(b"password", "username", genkey=True, user="3f100e7564a18ef92d69f5e969e41bee785001e1acea2fec789bdcaba28a97e9")


#encrypt username 
def scramble(data):
  h = hashlib.new('sha256')
  h.update(data.encode('utf8')) 
  test = h.hexdigest()
  return test

#creates a new dictionary in the json file that holds the users data
def newUser(MainUser):
  new_data = {
    MainUser: {
      "Sample": 0
    }
  } 
  with open("data.json", "r") as file:
    file_data = json.load(file)
    file_data["containers"].update(new_data)
    file.close()
  with open("data.json", "w") as file:
    json.dump(file_data, file)
    file.close()



#create window and manage login screen by defining all labels and buttons 
class runlogin():
    def __init__(self):
        self.existedcalled = False
        self.window = tk.Tk()
        self.window.title("LOGIN")
        self.window.geometry("300x300")
        self.labeluser = tk.Label(self.window,text="Username")
        self.userfield = tk.Text(self.window, height=1, width=20)
        self.labelpass = tk.Label(self.window,text="Password")
        self.passfield = tk.Text(self.window, height=1, width=20)
        self.sub = tk.Button(self.window,text="Submit", command=self.checkuser)
        self.ifexists = tk.Label(self.window,text="")

        self.labeluser.pack()
        self.userfield.pack()
        self.labelpass.pack()
        self.passfield.pack()
        self.sub.pack()
        self.ifexists.pack()


        tk.mainloop()
    def checkuser(self):
        user = self.userfield.get(1.0, "end-1c")
        password = self.passfield.get(1.0, "end-1c")
        comb = user + password
        self.MainUser = scramble(comb)
        try:
            read_names_json(self.MainUser)
            self.userfield.delete(1.0,"end-1c")
            self.destroylogin()
        except KeyError:
            if self.existedcalled:
               newUser(self.MainUser)
               self.destroylogin()
            else:
               self.confirm_creation()
            
    
    def confirm_creation(self):
       self.ifexists["text"] = "Username does not exist. \n Press submit again if you want to continue."
       self.existedcalled = True

    #destorys tkinter loop and continues to normal program
    def destroylogin(self):
        self.window.destroy()
        

    

