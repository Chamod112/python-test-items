from tkinter import *
import pygame

pygame.mixer.init()

root = Tk()
root.title("Music Player")

def play():
    pygame.mixer.music.load("song.mp3")
    pygame.mixer.music.play()

def stop():
    pygame.mixer.music.stop()

Button(root, text="Play", command=play).pack(pady=10)
Button(root, text="Stop", command=stop).pack(pady=10)

root.mainloop()
