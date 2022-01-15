from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import filedialog
import random

class Screen(Frame):
    def __init__(self, master, submaster):
        Frame.__init__(self, master, height=submaster.height, width=submaster.width, bg=submaster.color)
        self.screen = []
        for i in range(submaster.width):
            screen = Message(master, text="")
            screen.grid(row=0, column=i)
            self.screen.append(screen)

class BananaText(Frame):
    def __init__(self, master, submaster):
        Frame.__init__(self, master, height=submaster.height, width=submaster.width)
        self.txt_edit = Text(master)
        self.master = master
        self.submaster = submaster
        self.txt_edit = Text(master)

        master.bind('<Control-s>', self.save_file) # run self.save_file when ctrl s is pressed
        master.bind('<Control-o>', self.open_file) # run self.open_file when ctrl o is pressed
        master.bind('<Control-q>', self.close) # run self.close when ctrl q is pressed

        self.filemenu = Menu(submaster.menu, tearoff=0)
        # self.filemenu.add_command(label="New", command=donothing)
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.filemenu.add_command(label="Save", command=self.save_file)
        self.filemenu.add_command(label="Close", command=self.close)

        submaster.menu.add_cascade(label="File", menu=self.filemenu)

        helpmenu = Menu(submaster.menu, tearoff=0)
        # helpmenu.add_command(label="Help Index", command=donothing)
        # helpmenu.add_command(label="About...", command=donothing)
        # submaster.menu.add_cascade(label="Help", menu=helpmenu)

        master.config(menu=submaster.menu)
        self.txt_edit.grid(row=0, column=1)

    def save_file(self, *args, **kwargs): # *args and **kwargs are just there for key binding. only way it works.
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.txt_edit.get(1.0, 1000.0)
            output_file.write(text)

    def close(self, *args, **kwargs): # *args and **kwargs are just there for key binding. only way it works.
        self.txt_edit.grid_remove()
        self.submaster.menu.delete(2)
        self.grid_remove()

    def open_file(self, *args, **kwargs): # *args and **kwargs are just there for key binding. only way it works.
        filepath = askopenfilename(filetypes=[('All Files', '*.*')])
        if not filepath:
            return None
        self.txt_edit.delete("1.0")
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.txt_edit.insert(END, text)     

#class Shell(Frame):
    