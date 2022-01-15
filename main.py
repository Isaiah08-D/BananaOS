from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
import json 
import requests
from apps import Screen, BananaText


class Main(Frame): 
    def __init__(self, root, height, width, color):
        Frame.__init__(self, root, height=height, width=width, bg=color)
        
        self.root = root
        self.root.title('Banana0S')

        self.color = color
        self.height = height
        self.width = width

        self.menu = Menu(root) #make the upper menu

        self.computer_menu = Menu(self.menu, tearoff=0) # create the computer menu
        self.computer_menu.add_command(label="About", command=self.about)
        self.computer_menu.add_command(label="Help", command=self.help)
        self.computer_menu.add_separator()
        self.computer_menu.add_command(label="Quit", command=self.quit)

        self.menu.add_cascade(label="BananaOS", menu=self.computer_menu) # add the computer menu to the upper menu

        root.config(menu=self.menu) # initialize the upper menu

        self.app_font = font.Font(family='Helvetica', size=17)


        self.pinned_apps = {'🌐':[self.start_BananaWeb], '📝': [self.start_BananaText], '🕹️': [self.start_Games], '👨‍💻': [self.start_Shell]}
        self.apps = {'🌐':[self.start_BananaWeb], '📝': [self.start_BananaText], '🕹️': [self.start_Games], '👨‍💻': [self.start_Shell]}

        self.draw_appbar()
        self.draw_screen()

    def draw_appbar(self):
        """Draws the appbar
        """
        apps_drawn = 0
        self.appbar = []

        for appname, app in self.apps.items():
            self.appbar.append(Button(command=app[0], text=appname, font=self.app_font))
            self.appbar[apps_drawn].grid(row=1, column=apps_drawn + 1)
            apps_drawn += 1

    def close_app(self, app):
        app.grid_remove()
        self.draw_screen()

    def draw_screen(self):
        """Draws blank screen
        """
        self.app = Screen(self.root, self)
        self.app.grid(row=0, column=0)
    
    def close_screen(self):
        """Closes the blank screen. Run this before you first in the start_<app> function. """
    

    def about(self):
        messagebox.showinfo("About", "Created in 2020-2021 by Isaiah Day.\nGithub: Isaiah08-D")

    def help(self):
        messagebox.showinfo("Help",
                            "Genral Help:\n Genral help coming soon.\nTo get more help, open the shell and type help.")    
    
    
    def start_BananaText(self):
        self.close_screen() # close the blank screen

        self.current_app = BananaText(self.master, self) # run the bananatext app
        self.current_app.grid(row=0, column=0, rowspan=self.width)
        
    def start_Games(self): pass

    def start_Shell(self): pass

    def start_BananaWeb(self): pass


root = Tk()
main = Main(root, height=10, width=10, color='yellow')
root.mainloop()