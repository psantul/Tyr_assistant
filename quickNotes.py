import pymongo
import pyttsx3
from tkinter import simpledialog
from tkinter import *
from tkinter import messagebox

engine = pyttsx3.init()

engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel')

window = Tk()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database_tyr_1"]
mycol = mydb["notes"]

notes = mycol.find({})

c = 1
notes_list = ''
temp_note_listings = list()
for i in notes:
    txt = '['+str(c) + '] - ' + i['title'] + '\n' + i['note']+'\n\n'
    temp_note_listings.append(i['title'])
    c += 1
    notes_list = notes_list + txt

engine.say('Here are all the notes')
engine.runAndWait()
messagebox.showinfo('These are the notes',notes_list)

window.mainloop()