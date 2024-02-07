import tkinter as tk
from tkinter import *

import font_d as fd
from tkinter import ttk
import os
import json
import hashlib
import login_screen

#need to add a way to delete your account like a manage account button


###
"""
Make an encryption algorithm that decrypts the file contents when you open the file and then encrypts when closing.
(Already fineshed encryting when closing)"""

###
os.chdir(r"C:\Users\logan\OneDrive\Documents\Coding Projects\Row Counter")

#when you press submit deconify make new file window and show file list window


#set debug to True to see print statments and error checking
debug = False
if debug: print("Debug is On")


run = login_screen.runlogin()
MainUser = run.MainUser


#let application stop if closed
def close():
  if debug: print("closed")
  newfilewin.destroy()
  loadmenu.destroy()
  window.destroy()




#check to make sure no file of the same name exists
def check_files(fileName):
  FileList = []
  with open("data.json", "r") as file:
    data = json.load(file)
    for fname in data["containers"][MainUser]:
      FileList.append(fname)
    
  if fileName in FileList:
    return False
  else:
    return True

def getJsondata(fileName):
    with open("data.json", "r") as file:
      data = json.load(file)
      for names in data["containers"][MainUser].items():
        if names[0] == fileName:
          return names[1]

def changeJson(fileName, value):
  with open("data.json", "r") as file:
      data = json.load(file)
      file.close()
  data["containers"][MainUser][fileName] = value
  with open("data.json", "w") as file:
    json.dump(data, file)

def checkempty():
  with open("data.json", "r") as file:
      data = json.load(file)
      file.close()
  if len(data["containers"][MainUser]) < 1:
    new_data = {
      MainUser: {
        "PermFile": 0
      }
    } 
    data["containers"].update(new_data)
  with open("data.json", "w") as file:
    json.dump(data, file)
    file.close()

def deleteFile(fileName):
  fileName = fileName.strip()
  with open("data.json", "r") as file:
      data = json.load(file)
      file.close()

  del data["containers"][MainUser][fileName]
  with open("data.json", "w") as file:
    json.dump(data, file)

def newJsonKey(fileName):
  with open("data.json", "r") as file:
      data = json.load(file)
      file.close()
  new_data = {fileName: 0} 
  data["containers"][MainUser].update(new_data)
  with open("data.json", "w") as file:
    json.dump(data, file)

  #creates Scrollable Frame to make it so file list does not extend past screen length
#Not my class ----------------------
#Source: https://blog.teclado.com/tkinter-scrollable-frames/
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=200,height=150)

      #creates scroll bar object
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
#bind scroll region using canvas configure function
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
      #add window to canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
#position canvas using pack method
        self.canvas.pack(side="left", fill="both", expand=True)
#position scrollbar using pack method
        scrollbar.pack(side="right", fill="y")

#---------------------------------------------------------



#add button to manage files
class filebutton:
  def __init__(self,master,packmethod,filename,back,previous,target):
    #set self variables so they can be accesed throught the class
    self.target = target
    self.prev = previous
    self.packm = packmethod
    self.master = master
    #check if button is a back button
    if back:
      #if button is a back button set command to backfile command
      self.button = Button(master, command=self.backfile, text=filename)
    else:
      #if it isn't a back button it must be a file button so set command to load file button
      self.button = Button(master, command=self.loadfile, text=filename)
    if packmethod != "":
      #if pack method is set and not empty set pack mathod
      self.button.pack(side=packmethod)
    else:
      #if pack method is not specified just do a normal pack
      self.button.pack()

  def loadfile(self):

    namelist = login_screen.read_names_json(MainUser)
    name = self.button.cget('text')

    with open("optionsf/options.txt","r") as file:
      l = file.read()
      l = l.split(",")
      deletemode_result = l[3]
      #print(deletemode_result)
      file.close()
      
    #if delete is checked remove file and all instances of file saved in memory
      #------------------------------
    if deletemode_result == "1":
      self.button.destroy()
      removefilenames(name, namelist)
      
      for item in frame.scrollable_frame.winfo_children():
        item.destroy()

      with open("optionsf/options.txt","r") as file:
        l = file.read()
        l = l.split(",")
        l[3] = "0"
        filelist = l[2]
        l = ",".join(l)
        file.close()

      namelist = login_screen.read_names_json(MainUser)
      loadmenu.withdraw()
      loadfilebut(filelist, namelist)
      loadmenu.deiconify()
      
        #------------------------
      # Else, load the file
    else:
      nametitle = name.capitalize()
      window.title(nametitle)
      #name = str(name)
      r = getJsondata(str(name))
     # with open(name) as file:
     #   r = file.read()
      label["text"] = r
      f = "optionsf/options.txt"
      addnew(name, f, 1)
      loadmenu.withdraw()
      window.deiconify()
      
  def backfile(self):
    errorlabel["text"] = ""
    errorsubmit["text"] = ""
    f = "optionsf/options.txt"
    
    with open(f,"r") as file:
      l = file.read()
      l = l.split(",")
      filelist = l[2]
      file.close()

    namelist = login_screen.read_names_json(MainUser)
      
    for item in frame.scrollable_frame.winfo_children():
      item.destroy()
    loadfilebut(filelist, namelist)
    
    
    self.target.deiconify()
    self.prev.withdraw()



def makestringlist(listin):
  towrite = ""
  for i in range(len(listin)):
    if i == len(listin):
      towrite += str(listin[i])
    else:
      towrite += str(listin[i]) + ","
  towrite = towrite.rstrip(towrite[-1])
  return towrite


def removefilenames(name, namelist):
  if debug: print("removefilenames:")
  length = len(namelist)
  allow = True
  if length < 2:
    if debug: print("Can't Delete All Files!!!")
    errorlabel["text"] = "Can't Delete All Files!!!"
    allow = False
  if allow:
    f = "optionsf/options.txt"
    with open(f) as file:
      nameamount = file.read()
      nameamount = nameamount.split(",")
      file.close()
    amount = int(nameamount[2])
    amount -= 1
    nameamount[2] = str(amount)
    if debug: print(nameamount)
    towrite = makestringlist(nameamount)
    if debug: print("Towrite: " + towrite)
  
    with open(f, "w") as file:
      file.write(towrite)
      file.close()

    if debug: print("Get file name and remove from namelist")

    namelist = login_screen.read_names_json(MainUser)
    for i in range(len(namelist)):
        if str(namelist[i]) == str(name):
          namelist.pop(i)
          break
        
        if debug: print(namelist)
    
    with open(f,"r") as file:
      l = file.read()
      l = l.split(",")
      file.close()

    deleteFile(name)
    f = "optionsf/options.txt"
    nameset = str(namelist[0]) + ".txt"
    nametitle = namelist[0].capitalize()
    window.title(nametitle)
    addnew(nameset, f, 1)
    if debug: print("------------------------------------")
      
def deletemode():
  value = var1.get()
  with open("optionsf/options.txt","r") as file:
    l = file.read()
    l = l.split(",")
  if value == 1:
    with open("optionsf/options.txt","w") as file:
      l[3] = "1"
      l = ",".join(l)
      file.write(l)
      file.close()
  else:
    with open("optionsf/options.txt","w") as file:
      l[3] = "0"
      l = ",".join(l)
      file.write(l)
      file.close()

def reloads():
  namelist = login_screen.read_names_json(MainUser)
  newam = str(len(namelist))
  if debug: print(newam)
  with open("optionsf/options.txt","r") as file:
    l = file.read()
    l = l.split(",")
    l[3] = "0"
    l[2] = newam
    if debug: print(newam)
    l = ",".join(l)
    file.close()
  with open("optionsf/options.txt","w") as file:
    file.write(l)

  namelist = login_screen.read_names_json(MainUser)
  return newam, namelist

def addnew(text,f,location):
  if debug: print("addnew Function:")

  with open(f) as file:
    loaded = file.read()
    file.close()
  l = loaded.split(",")
  if debug: print("Clear file f")

 # newJsonKey(f) #--------------------------------------------------------------------------------------------------
  with open(f, "w") as file:
    file.truncate(0)
    file.close()

  if debug: print("Based on location write were the text will be set")

  if location == 0:
    with open(f, "a") as file:
      file.write(text)
      file.write("," + str(l[1]))
      file.write("," + str(l[2]))
      file.write("," + l[3])
      file.close()

  elif location == 1:
    with open(f, "a") as file:
      file.write(str(l[0] + ","))
      file.write(str(text))
      file.write("," + str(l[2]))
      file.write("," + l[3])
      file.close()

  else:
    with open(f, "a") as file:
      file.write(str(l[0] + ","))
      file.write(str(l[1] + ","))
      file.write(text)
      file.write("," + l[3])
      file.close()

      
  for item in frame.scrollable_frame.winfo_children():
    item.destroy()

  filelist, namelist = reloads()

  if debug: print(namelist)
  newfilewin.withdraw()
  loadfilebut(filelist, namelist)
  loadmenu.deiconify()
  
def readnum():
  try:
    with open("optionsf/options.txt", "r") as file:
      l = file.read()
      l = l.split(",")
      f = l[1]
    
    recent = int(getJsondata(f))
  except:
    names = login_screen.read_names_json(MainUser)
    with open("optionsf/options.txt", "r") as file:
      l = file.read()
      l = l.split(",")
      l[1] = names[0]
      l = ",".join(l)
    with open("optionsf/options.txt", "w") as file:
      file.write(l)
    
    recent = int(getJsondata(names[0]))
  
  return recent

  
    
def updatemain(mod, setnum):
  with open("optionsf/options.txt", "r") as file:
    l = file.read()
    l = l.split(",")
    f = l[1]

  recent = int(getJsondata(f))
  if mod == "+":
    recent += 1
  elif mod == "-":
    recent -= 1
    if recent < 0:
      recent = 0
  elif mod == "res":
    if debug: print("Reseting file")
    recent = 0
  elif mod == "set":
    recent = setnum
  
  changeJson(f, recent)
  return recent

def loadmain():
  errorlabel["text"] = ""
  window.withdraw()
  loadmenu.deiconify()
  
def addfunc():
  result = updatemain("+", 0)
  label["text"] = result

def subtract():
  result = updatemain("-", 0)
  label["text"] = result

def resetfunc():
  result = updatemain("res", 0)
  label["text"] = result


def getname():
  if debug: print("Get Name Function:")
  name = namefield.get(1.0, "end-1c")
  namefield.delete(1.0,"end-1c")
  f = "filenamelist.txt"
  t = "optionsf/options.txt"
  namelist = login_screen.read_names_json(MainUser)
  
  if str(name) in namelist:
    errorsubmit["text"] = "File Name Already Exists!"
  elif str(name) == "filenamelist":
    errorsubmit["text"] = "You can't name a File that!"
  else:
    if debug: print("File name does not exist, make new file")
    newname = str(name)
    
    
    #########################################################
    newJsonKey(newname)
    #########################################################

    with open(t, "r") as file:
      l = file.read().split(",")
      amount = int(l[2])
      amount += 1
      file.close()
    
    
    addnew(str(amount),t,2)

    

def numset():
  if debug: print("Num Set Function:")
  newnum = inp.get(1.0, "end-1c")
  inp.delete("1.0","end")
  try:
    if debug: print("Text is a number")
    number = int(newnum)
    result = updatemain("set", number)
    label["text"] = result
    if debug: print("Label text set to number entered")
    if debug: print("-----------------------------------")
  except ValueError:
    if debug: print("Text entered is not a number")
    inp.insert("1.0", "That is not a number!")
    if debug: print("-----------------------------------")

def resetall():
  window.withdraw()
  double.deiconify()
   
  
def newfile():
  errorlabel["text"] = ""
  newfilewin.deiconify()
  loadmenu.withdraw()

def resetconfirmation():
  if debug: print("All file counts have been reset to 0")
  window.deiconify()
  double.withdraw()
  contents = login_screen.read_names_json(MainUser)
  for i in range(len(contents)):
    filename = str(contents[i])
    changeJson(filename, 0)
  label["text"] = 0
      
    
  
def loadfilebut(filelist, namelist):
  errorlabel["text"] = ""
  #print(filelist)
  try:
    for i in range(int(filelist)):
      clfile = filebutton(frame.scrollable_frame, TOP, str(namelist[i]), False, False, False)
  except:
    if debug: print(filelist)
    pass


def setkey(event):
  if debug: print(event.char)
  keypressed = str(event.char)
  if keypressed == "-":
    subtract()
  elif keypressed == "+":
    addfunc()
  elif keypressed == "r":
    resetfunc()

def subkey(e):
  subtract()

def addkey(e):
  addfunc()


#encrypt everything when you close the window 
def on_closing():
# salt = login_screen.getsal(MainUser)
#  with open("data.json", "r") as file:
#      data = json.load(file)
#      file.close()
#
#  newcopy = {}
#  for key in data["containers"][MainUser]:
#    print(data["containers"][MainUser][key])
#    newcopy[login_screen.scramble(key)] = login_screen.scramble(str(data["containers"][MainUser][key]))
#
#  print(newcopy)
#   
  
  
  window.destroy()
#--------------------------------------------------------------------------------------------------------------------



window = tk.Tk()

window.title("Counter")
window.geometry("300x300")


#----------------Reset All Menu------------------------

double = Toplevel(window)
double.protocol("WM_DELETE_WINDOW", close)
double.geometry("300x300")
double.title("Reset All")
checkreset = tk.Button(double, text="Are you sure?", command=resetconfirmation)
checkreset.pack(fill="none", expand=True)
backbut1 = filebutton(double, RIGHT, "Back", True, double, window)

double.withdraw()
#---------------Load window --------------------

loadmenu = Toplevel(window)
loadmenu.protocol("WM_DELETE_WINDOW", close)
loadmenu.geometry("300x300")
loadmenu.title("File Load")
frame = ScrollableFrame(loadmenu)
f = "optionsf/options.txt"
reloads()

curop = ""
with open(f,"r") as file:
  l = file.read()
  if debug: print(l)
  l = l.split(",")
  if not run.existedcalled:
    curop = l[1]
  else:
    curop = "Sample"
    run.existedcalled = True
  l[3] = "0"
  filelist = l[2]
  l = ",".join(l)
  file.close()
  
with open(f,"w") as file:
  file.write(l)
  file.close()

namelist = login_screen.read_names_json(MainUser)

curop = curop.split(".")
curop = curop[0] 



frame.pack()
errorlabel = tk.Label(loadmenu, text="")

loadfilebut(filelist,namelist)
var1 = IntVar()
errorlabel.pack()
newfilebut = tk.Button(loadmenu,text="New File", command=newfile)
newfilebut.pack(side=LEFT)
deletecheck = tk.Checkbutton(loadmenu, text="Delete", variable=var1, onvalue="1", offvalue="0",command=deletemode)
backbut = filebutton(loadmenu, RIGHT, "Back", True, loadmenu, window)
deletecheck.pack(side=LEFT)
loadmenu.withdraw()

#---------------New File Window ------------------

newfilewin = Toplevel(window)
newfilewin.protocol("WM_DELETE_WINDOW", close)
newfilewin.geometry("200x200")
newfilewin.title("File Name")
namefield = tk.Text(newfilewin, height=5, width=20)

errorsubmit = tk.Label(newfilewin,text="")
errorsubmit.pack()
namefield.pack()


submitname = tk.Button(newfilewin, text="Submit",command=getname)
submitname.pack(side=LEFT)
backbut = filebutton(newfilewin, RIGHT, "Back", True, newfilewin, loadmenu)
newfilewin.withdraw()

#------------Main Window--------------
#space labels are just to seperate items

window.title(curop.capitalize())
space = tk.Label()
space.pack()

#main number label
checknum = readnum()
if checknum != 0:
  label = tk.Label(text=str(checknum))
else:
  label = tk.Label(text="Start?")
label.config(font=fd.comic)
label.pack()


space = tk.Label()
space.pack()

#add button
add = tk.Button(text="+",command=addfunc)
add.config(font=fd.com)
add.pack()

#subtract button
sub = tk.Button(text="-", command=subtract)
sub.config(font=fd.com)
sub.pack()
space = tk.Label()
space.pack()
inp = tk.Text(height=1, width=20)
inp.pack()

#setnum button
setnum = tk.Button(text="Set #", command=numset)
setnum.pack()

#load button
load = tk.Button(text="Load", command=loadmain)
load.pack(side=LEFT)

#reset button
reset2 = tk.Button(text="Reset All", command=resetall)
reset2.pack(side=RIGHT)
reset = tk.Button(text="Reset", command=resetfunc)
reset.pack(side=RIGHT)

window.bind('<Up>',addkey)
window.bind('<Down>',subkey)
window.bind("<Key>", setkey)

#activate gui loop
window.protocol("WM_DELETE_WINDOW", on_closing)
newfilewin.protocol("WM_DELETE_WINDOW", on_closing)
loadmenu.protocol("WM_DELETE_WINDOW", on_closing)
double.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()
