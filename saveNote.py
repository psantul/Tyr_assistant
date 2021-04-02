import pymongo
import pyttsx3
from tkinter import simpledialog
from tkinter import *
import json
import os

data={}

with open('currentUser.txt') as json_file:
    data = json.load(json_file)

userName = data['info'][0]

engine = pyttsx3.init()

engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel')

window = Tk()
window.geometry("1x1+450+275")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[userName]
mycol = mydb["notes"]

title = simpledialog.askstring('Heading','Enter heading of the note : ')
if title=='':
    title='-'

note = simpledialog.askstring('Note Content','Enter note content : ')
if note=='':
    note='-'

dictionary = {'title': title, 'note': note}

mycol.insert_one(dictionary)

# window.mainloop()