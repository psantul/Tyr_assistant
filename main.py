from tkinter import *
import json
import pyttsx3
import os

data ={}
old_users = list()

with open('data.txt') as json_file:
    data = json.load(json_file)

for i in range(len(data['people'])):
    old_users.append(data['people'][i]['name'].lower())

engine = pyttsx3.init()

engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel')

engine.say("Hello, my name is Tyr, I am an assistant")
engine.runAndWait()

window = Tk()

window.title("Tyr Assistant App")

window.geometry('373x250+450+275')

canvas = Canvas(window, width = 373, height = 147)
canvas.pack()
img = PhotoImage(file="logo.png")
canvas.create_image(20,20, anchor=NW, image=img)
canvas.grid(column=0,row=0)

lbl = Label(window, text="What is your name?")

lbl.grid(column=0, row=1)

txt = Entry(window, width=10)

txt.grid(column=0, row=2)

def clicked():
    lbl.configure(text="Button was clicked !!")
    userName = txt.get()
    if userName.lower() in old_users:
        engine.say('Welcome back ' + userName.lower() + ', happy to be of help again, These are your options')
        engine.runAndWait()
    else:
        engine.say('Hello ' + userName.lower() + ', nice to meet you, These are your options')
        engine.runAndWait()
        data['people'].append({
            'name': userName
        })
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)
    current = {}
    current['info'] = [userName]
    with open('currentUser.txt','w') as outfile:
        json.dump(current, outfile)

    # engine.say(userName + " These are your options")
    # engine.runAndWait()

    window.iconify()
    os.system('python window2.py')

btn = Button(window, text="Click Me", command=clicked)

btn.grid(column=0, row=3)

window.mainloop()



