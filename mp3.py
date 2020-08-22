from tkinter import *
import os
from pygame import mixer
import tkinter.filedialog
import tkinter.messagebox
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk
from ttkthemes import  themed_tk as tk
root=tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
statusbar=ttk.Label(root,text="Welcome to Spotify",relief=SUNKEN,anchor=W,font='Times 10 italic')
statusbar.pack(side=BOTTOM,fill=X)
menubar=Menu(root)
root.config(menu=menubar)
index=0
def about_us():
    tkinter.messagebox.showinfo('Spotify Music','This is a music player build using Python')
def browse_file():
    global filename_path
    filename_path=tkinter.filedialog.askopenfilename()
    add_to(filename_path)
def add_to(f):
    global index
    f=os.path.basename(f)
    lb1.insert(index,f)
    playlist.insert(index,filename_path)
    index+=1
def del_song():
    selected_song = lb1.curselection()
    selected_song = int(selected_song[0])
    lb1.delete(selected_song)
    playlist.pop(selected_song)



submenubar=Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=submenubar)
submenubar.add_command(label="Open",command=browse_file)
submenubar.add_command(label="Exit",command=root.destroy)
submenubar=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help",menu=submenubar)
submenubar.add_command(label="About Us",command=about_us)
playlist=[]

mixer.init()
root.title("SPOTIFY MUSIC")
root.geometry('600x350')
root.iconbitmap(r'spotify.ico')
leftframe=Frame(root)
leftframe.pack(side=LEFT,padx=10)
lb1=Listbox(leftframe)
lb1.pack()
addpht=PhotoImage(file="plus.png")
btn1=ttk.Button(leftframe,text="+Add",image=addpht,command=browse_file)
btn1.pack(side=LEFT)
delpht=PhotoImage(file="delete.png")
btn2=ttk.Button(leftframe,text="-Del",image=delpht,command=del_song)
btn2.pack(side=RIGHT)
rightframe=Frame(root)
rightframe.pack(side=LEFT)
topframe=Frame(rightframe)
topframe.pack()
textlabel=Label(topframe,text="Lets get the party started")
textlabel.pack(side=TOP,padx=5,pady=5)
lengthlabel=Label(topframe,text="Total Length:--:--")
lengthlabel.pack(padx=5,pady=5)
currenTimeLabel=Label(topframe,text="Current Time:--:--",relief=GROOVE)
currenTimeLabel.pack(padx=5,pady=5)

middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)
def start_count(t):
    global paused
    x=0
    while x<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(x, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenTimeLabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            x += 1

def show_details(play_it):
    textlabel['text'] = 'Playing' + '- ' + os.path.basename(paly_it)
    filedata=os.path.splitext(play_it)
    if filedata[1]=='.mp3':
        audio=MP3(play_it)
        tot_len=audio.info.length
    else:
        a=mixer.Sound(play_it)
        tot_len=a.get_length()
    mins,secs=divmod(tot_len,60)
    mins = round(mins)
    secs = round(secs)
    tf='{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text']="Total Length"+'-'+tf
    t1 = threading.Thread(target=start_count, args=(tot_len,))
    t1.start()


def play_music():
    global paused
    global stopped
    global paly_it
    if stopped and paused:
        statusbar['text'] = "Playing music" + ' - ' + os.path.basename(paly_it)
        selected_song=lb1.curselection()
        selected_song=int(selected_song[0])
        id=selected_song
        paly_it=playlist[selected_song]
        mixer.music.load(paly_it)
        mixer.music.play()
        stopped=False
        paused=False

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = lb1.curselection()
            selected_song = int(selected_song[0])
            paly_it = playlist[selected_song]
            mixer.music.load(paly_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(paly_it)
            show_details(paly_it)
            stopped=False
        except:
            tkinter.messagebox.showinfo('Play Error', 'You have no musics yet.')
photo=PhotoImage(file="play_s.png")
btn=ttk.Button(middleframe,image=photo,command=play_music)
btn.grid(row=0,column=1,padx=10,pady=10)


def rew_music():
    play_music()
    statusbar['text']="Music Rewind"
stopped=False
def stop_music():
    global stopped
    stopped=True
    statusbar['text']='Music Stopped'
    mixer.music.stop()
stopphoto=PhotoImage(file="stop.png")
stopbtn=ttk.Button(middleframe,image=stopphoto,command=stop_music)
stopbtn.grid(row=0,column=2,padx=10,pady=10)
paused=FALSE
def pause_music():
    global paused
    paused=True
    mixer.music.pause()
    statusbar['text']="Music Paused"

pausePhoto=PhotoImage(file='pause.png')
pausebtn =ttk.Button(middleframe,image=pausePhoto,command=pause_music)
pausebtn.grid(row=0,column=0,padx=10,pady=10)
vol=0
bottomframe = Frame(rightframe)
bottomframe.pack()

def set_vol(val):
    vol=float(val)/100
    mixer.music.set_volume(vol)
scale=ttk.Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
scale.set(30)
mixer.music.set_volume(0.3)
scale.grid(row=0,column=1,padx=5,pady=5)

rephoto=PhotoImage(file="rewind.png")
rebtn=ttk.Button(bottomframe,image=rephoto,command=rew_music)
rebtn.grid(row=0,column=0,padx=5,pady=5)
muted=FALSE
def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.5)
        mutebtn.configure(image=mute)
        scale.set(50)
        muted=FALSE
    else:
        mixer.music.set_volume(0)
        mutebtn.configure(image=unmute)
        scale.set(0)
        muted=True


mute=PhotoImage(file="mute.png")
unmute=PhotoImage(file="unmute.png")
mutebtn=ttk.Button(bottomframe,image=mute,command=mute_music)
mutebtn.grid(row=0,column=2,padx=10,pady=10)
def on_close():
    stop_music()
    root.destroy()
root.protocol("WM_DELETE_WINDOW",on_close)
root.mainloop()
