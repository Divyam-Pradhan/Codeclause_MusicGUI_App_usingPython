import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import pygame , time
from mutagen.mp3 import MP3


root=tk.Tk()
root.geometry("480x680+440-38")    
root.title("MP3 Music Player")
root.configure(bg="white")          
root.iconbitmap("icon.ico")

def Select_Song():
    global file,song
    file = askopenfilename(initialdir='C:/Users/Music', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))     #open file
    song = file.split('/')[len(file.split('/'))-1]  #split file name from path 
    CurrentSong['text'] = song     #set song name on label


def play_time():       #this function will run as song plays
    if stopped:  #if stop button is pressed then dont
        return
    #current play time
    current_time = pygame.mixer.music.get_pos() / 1000     #get_pos() gives time in millsec so divide by 1000 to get time in sec
    converted_current_time = time.strftime('%M:%S',time.gmtime(current_time))   #convert time in readable format

    global song_length
    #total music length
    song_mut = MP3(file)
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S',time.gmtime(song_length))
    
    current_time+=1     

    if int(slider.get() == int(song_length)):
        #if slider position is at end of song
        slider.configure(value=0)
        playtime.configure(text="00:00")
       
    elif paused:
        
        pass
    
    elif int(slider.get()) == int(current_time):
    
        slider_position = int(song_length)   
        slider.configure(to=slider_position,value=int(current_time)) 
    else:
        
        slider_position = int(song_length)   
        slider.configure(to=slider_position,value=int(slider.get())) #set slider position to current time
        converted_current_time = time.strftime('%M:%S',time.gmtime(int(slider.get())))   
      
        playtime['text'] = (converted_current_time)   
        total_music_length['text'] = (converted_song_length) #set total song length above slider on right side
        next_time = int(slider.get())+1     
        slider.configure(value=next_time)

    playtime.after(1000,play_time)          

pygame.mixer.init()
def play_music():
    try:               #try clause if no exception occurs
        global stopped
        stopped=False
        playtime.configure(text="00:00")
        total_music_length.configure(text="00:00")
        slider.configure(value=0)
        pygame.mixer.music.load(file)    
        pygame.mixer.music.play(loops=0)
        play_time()     #calling play_time function    
    except(NameError):   
           CurrentSong.configure(text="No song is selected!!",font="comicsanms 20 bold")


    

global paused
paused = False             
def pause_music(is_paused):        
    global paused
    paused = is_paused           
    if paused:           
        pygame.mixer.music.unpause() 
        paused = False
    else:                
        pygame.mixer.music.pause()
        paused = True


global stopped
stopped=False
def stop_music():
    #stop song
    playtime.configure(text="00:00")
    total_music_length.configure(text="00:00")
    slider.configure(value=0)
    CurrentSong.configure(text="")
    pygame.mixer.music.stop()   #stop song
    global stopped
    stopped =True 
    

def slide(x):
    pygame.mixer.music.load(file)    
    pygame.mixer.music.play(loops=0, start=int(slider.get()))
  



play = Image.open("play.png")                  
resize_image = play.resize((100, 100))
play = ImageTk.PhotoImage(resize_image)
play_button=Button(root, image = play,borderwidth=0,bg="white",command=play_music,bd=0)
play_button.place(x=195,y=546)

pause = Image.open("pause.png")               
resize_image = pause.resize((100, 100))
pause = ImageTk.PhotoImage(resize_image)
pause_button=Button(root, image=pause, borderwidth=0,bg="white",command=lambda:pause_music(paused),bd=0)
pause_button.place(x=50,y=545)

stop = Image.open("stop.png")               
resize_image = stop.resize((100, 100))
stop = ImageTk.PhotoImage(resize_image)
stop_button=Button(root, image=stop, borderwidth=0,bg="white",command=stop_music,bd=0)
stop_button.place(x=340,y=545)

pic = Image.open("pic2.png")          
resize_image = pic.resize((210,210))
pic = ImageTk.PhotoImage(resize_image)
Label(root,image=pic,bd=0,bg="white").place(x=140,y=140)

button_border = tk.Frame(root,highlightbackground="#ffd700",highlightthickness=8,bd=0,height=80,width=300)  #select song button border
button_border.place(x=98,y=4)

selectSong = Image.open("selectSong.png")
resize_image = selectSong.resize((282,61))
selectSong = ImageTk.PhotoImage(resize_image)
selectSong_btn = Button(button_border, image=selectSong,borderwidth=0,bg="white",command=Select_Song,bd=0)
selectSong_btn.place(x=0,y=0)       

CurrentSong = Label(root, text='', width=30,font="comicsanms 20 italic",bg="white",fg="black",anchor="center")
CurrentSong.place(x=0,y=390)         #song name label

slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL,command=slide,length= 380,value=0)
slider.place(x=50,y=490)  #slider

playtime = Label(root, text= "00:00",bg="white")     
playtime.place(x=45,y=465)

total_music_length = Label(root, text= "00:00",bg="white")    
total_music_length.place(x=400,y=465)

root.mainloop()
