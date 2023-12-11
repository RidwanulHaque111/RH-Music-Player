#created by Ridwanul Haque

import os
import pygame
from tkinter import *
from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.minsize(350, 400)

        self.listofsongs = []
        self.realnames = []

        self.v = StringVar()
        self.songlabel = Label(root, textvariable=self.v, width=35)

        self.index = 0

        label = Label(root, text='RH Music Player')
        label.pack()

        self.listbox = Listbox(root)
        self.listbox.pack()

        self.realnames.reverse()

        for items in self.realnames:
            self.listbox.insert(0, items)

        self.realnames.reverse()

        nextbutton = Button(root, text='Next Song', command=self.next_song)
        nextbutton.pack()

        previousbutton = Button(root, text='Previous Song', command=self.prev_song)
        previousbutton.pack()

        pausebutton = Button(root, text='Pause Song', command=self.pause_song)
        pausebutton.pack()

        unpausebutton = Button(root, text='Unpause Song', command=self.unpause_song)
        unpausebutton.pack()

        stopbutton = Button(root, text='Stop Music', command=self.stop_song)
        stopbutton.pack()

        nextbutton.bind("<Button-1>", self.next_song)
        previousbutton.bind("<Button-1>", self.prev_song)
        pausebutton.bind("<Button-1>", self.pause_song)
        unpausebutton.bind("<Button-1>", self.unpause_song)
        stopbutton.bind("<Button-1>", self.stop_song)

        self.songlabel.pack()

        self.directory_chooser()

    def directory_chooser(self):
        directory = askdirectory()
        os.chdir(directory)

        for files in os.listdir(directory):
            if files.endswith(".mp3"):
                realdir = os.path.realpath(files)
                audio = ID3(realdir)

                if 'TIT2' in audio:
                    self.realnames.append(audio['TIT2'].text[0])
                else:
                    self.realnames.append(files)

                self.listofsongs.append(files)
                self.listbox.insert(END, files)  # Update listbox with song names

        pygame.mixer.init()
        pygame.mixer.music.load(self.listofsongs[0])
        pygame.mixer.music.play()

    def update_label(self):
        self.v.set(self.realnames[self.index])

    def next_song(self, event=None):
        self.index += 1
        pygame.mixer.music.load(self.listofsongs[self.index])
        pygame.mixer.music.play()
        self.update_label()

    def prev_song(self, event=None):
        self.index -= 1
        pygame.mixer.music.load(self.listofsongs[self.index])
        pygame.mixer.music.play()
        self.update_label()

    def pause_song(self, event=None):
        pygame.mixer.music.pause()
        self.v.set("Song Paused")

    def unpause_song(self, event=None):
        pygame.mixer.music.unpause()
        self.v.set("Song unpaused")

    def stop_song(self, event=None):
        pygame.mixer.music.stop()
        self.v.set("")

if __name__ == "__main__":
    root = Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
