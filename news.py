import requests
import json
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import pyttsx3

data={}

with open('newsSources.txt') as json_file:
    data = json.load(json_file)

newsSources = list()

for i in data:
    newsSources.append(i)

engine = pyttsx3.init()

engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel')

engine.say("Select one news source and press submit")
engine.runAndWait()

window = Tk()

window.title("News Source Selection")

window.geometry('250x80+450+275')

lbl = Label(window,text="Select one news source for headlines")

lbl.grid(column=0,row=0)

combo = Combobox(window)

combo['values'] = newsSources

combo.current(1)

combo.grid(column=0, row=2)

def clicked():
    source = combo.get()

    key = '<<Key>>'

    api_url = 'https://newsapi.org/v2/top-headlines?sources='+source+'&apiKey=' + key

    response = requests.get(api_url)

    data = response.json()

    news_list = ''
    for news in data['articles']:
        news_list = news_list + '\n\nNews : ' + news['title']

    messagebox.showinfo('News Headlines from '+source, news_list)

btn = Button(window,text="Submit",command=clicked)
btn.grid(column=0,row=4)

window.mainloop()

