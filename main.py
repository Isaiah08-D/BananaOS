from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import filedialog
import os
import json
import requests
from apps import BananaText, SudokuGrid, Shell, Games, Shotput



class Main(Frame):
    def __init__(self, root, height, width, bg):
        Frame.__init__(self, root, height=height, width=width, bg=bg)

        self.root = root
        self.root.title('BananaOS')

        self.bg = bg
        self.height = height
        self.width = width

        # self.blankscreen = Canvas(root, width=width*50, height=500, bg=bg)
        # self.blankscreen.grid(row=0, column=0)

        self.menu = Menu(root)

        self.computer_menu = Menu(self.menu, tearoff=0)
        self.computer_menu.add_command(label="About", command=self.about)
        self.computer_menu.add_command(label="Help", command=self.help)

        self.computer_menu.add_separator()

        self.computer_menu.add_command(label="Quit", command=root.quit)

        self.menu.add_cascade(label="BananaOS", menu=self.computer_menu)

        root.config(menu=self.menu)

        self.pinned_apps = {'BananaText': [self.start_BananaText], 'Games': [self.start_games],
                            'Shell': [self.start_shell]}
        self.apps = {'BananaText': [self.start_BananaText], 'Games': [self.start_games], 'Shell': [self.start_shell]}
        self.appbar = []

        self.current_app = None

        self.draw_app_bar()

    def draw_app_bar(self):
        x = 0
        self.appbar = []

        for appname, app in self.apps.items():
            self.appbar.append(Button(command=app[0], text=appname))
            self.appbar[x].grid(row=1, column=x + 1)
            x += 1

    def close_app_bar(self):
        x = 0

        for appname, app in self.apps.items():
            self.appbar[x].grid_remove()
            x += 1


    def start_BananaText(self):
        # close the current program (if there is one)
        self.program_close()

        # remove the blank screen (currently not working)
        # self.blankscreen.grid_remove()

        # create the bananatext app and put it on the screen
        app = BananaText(self.root, self)
        app.grid(row=0, column=0)
        # change the current app.
        self.current_app = app

    def start_games(self):
        # close the current program (if there is one)
        self.program_close()

        # remove the blank screen (currently not working)
        # self.blankscreen.grid_remove()

        # create the bananatext app and put it on the screen
        app = Games(self.root, self)
        app.grid(row=0, column=0)
        # change the current app.
        self.current_app = app

    def start_sudoku(self):

        # close the current program (if there is one)
        self.program_close()


        # create the sudoku app and put it on the screen
        app = SudokuGrid(self.root)
        app.grid(row=0, column=0)
        # change the current app.
        self.current_app = app

    def start_shell(self):
        # close the current program (if there is one)
        self.program_close()

        # remove the blank screen (currently not working)
        # self.blankscreen.grid_remove()

        # create the sudoku app and put it on the screen
        app = Shell(self.root, self)
        app.grid(row=0, column=0)
        # change the current app.
        self.current_app = app

    def start_shotput(self):
        # close the current program (if there is one)
        self.program_close()



        # create the sudoku app and put it on the screen
        app = Shotput(self.root, self)
        app.grid(row=0, column=0)
        # change the current app.
        self.current_app = app

    def program_close(self):
        self.close_app_bar()
        self.apps = self.pinned_apps
        self.draw_app_bar()
        self.apps = self.pinned_apps
        if self.current_app == None:
            return
        self.current_app.close()

        current_app = None

    def about(self):
        messagebox.showinfo("About", "Created in 2020 by Isaiah Day, Isaiah Firestone and Mila Day.")

    def help(self):
        messagebox.showinfo("Help",
                            "Genral Help:\n Genral help coming soon.\nTo get more help, open the shell and type help.")


root = Tk()
main = Main(root, height=10, width=10, bg='yellow')
root.mainloop()
