from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import filedialog
import random


class Games(Frame):
    def __init__(self, master, submaster):
        Frame.__init__(self, master, height=9, width=10, bg='white')
        self.games = dict(Sudoku=submaster.start_sudoku, Shotput=submaster.start_shotput)
        self.draw_display()

    def draw_display(self):
        row, column = 0, 0
        for name, command in self.games.items():
            Button(self, text=name, command=command).grid(row=row, column=column)
            column += 1
            if column == 4:
                column = 0
                row += 1

    def draw_games(self):
        row, column = 0, 0
        for name, command in self.games.items():
            Button(self, text=name, command=command).grid(row=row, column=column)
            column += 1
            if column < 4:
                column = 0
                row += 1

    def close(self):
        self.grid_remove()


class BananaText(Frame):
    def __init__(self, master, submaster):
        Frame.__init__(self, master, height=9, width=10, bg='white')
        self.txt_edit = Text(master)
        self.master = master
        self.submaster = submaster
        self.txt_edit = Text(master)

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

    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.txt_edit.get(1.0)
            output_file.write(text)

    def close(self):
        self.txt_edit.grid_remove()
        self.submaster.menu.delete(2)
        self.grid_remove()

    def open_file(self):
        filepath = askopenfilename(filetypes=[("Text Files", '*.txt.'), ('All Files', '*.*')])
        if not filepath:
            return None
        self.txt_edit.delete("1.0")
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.txt_edit.insert(END, text)


class Shell(Frame):
    def __init__(self, master, submaster):
        Frame.__init__(self, bg='white')
        self.master = master
        self.submaster = submaster

        self.filemenu = Menu(submaster.menu, tearoff=0)
        self.filemenu.add_command(label="Close", command=self.close)

        submaster.menu.add_cascade(label="File", menu=self.filemenu)

        helpmenu = Menu(submaster.menu, tearoff=0)
        # helpmenu.add_command(label="Help Index", command=donothing)
        # helpmenu.add_command(label="About...", command=donothing)
        # submaster.menu.add_cascade(label="Help", menu=helpmenu)

        self.columnnum = 0

        self.text = StringVar()
        self.rownum = 0
        self.prompt = Entry(self, textvariable=self.text)
        self.prompt.grid(column=0, row=self.rownum)
        self.run_button = Button(self, command=self.run, text='run')
        self.run_button.grid(row=self.rownum, column=1)
        master.config(menu=submaster.menu)

    def run(self):
        x = self.text.get()
        if x == 'help':
            self.display('HELP\nHelp comming in V2.')
        else:
            self.display('Error: command not found.')

    def display(self, message):
        self.rownum += 2
        Label(self, text=message).grid(column=0, row=self.rownum)
        self.rownum += 1
        self.update()

    def update(self):
        self.prompt.grid_remove()
        self.prompt.grid(row=self.rownum, column=0)

        self.run_button.grid_remove()
        self.run_button.grid(row=self.rownum, column=1)

    def close(self):
        self.submaster.menu.delete(2)
        self.grid_remove()


class SudokuCell(Label):
    '''represents a Sudoku cell'''

    def __init__(self, master, coord):
        '''SudokuCell(master,coord) -> SudokuCell
        creates a new blank SudokuCell with (row,column) coord'''
        Label.__init__(self, master, height=1, width=2, text='', \
                       bg='white', font=('Arial', 24))
        self.coord = coord  # (row,column) coordinate tuple
        self.number = 0  # 0 represents an empty cell
        self.readOnly = False  # starts as changeable
        self.highlighted = False  # starts unhighlighted
        self.possibles = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # set of possible fills
        # set up listeners
        self.bind('<Button-1>', self.highlight)
        self.bind('<Key>', self.change)

    def get_coord(self):
        '''SudokuCell.get_coord() -> tuple
        returns the (row,column) coordinate of the cell'''
        return self.coord

    def get_number(self):
        '''SudokuCell.get_number() -> int
        returns the number in the cell (0 if empty)'''
        return self.number

    def is_read_only(self):
        '''SudokuCell.is_read_only() -> boolean
        returns True if the cell is read-only, False if not'''
        return self.readOnly

    def is_highlighted(self):
        '''SudokuCell.is_highlighted() -> boolean
        returns True if the cell is highlighted, False if not'''
        return self.highlighted

    def set_number(self, number, readOnly=False):
        '''SudokuCell.set_number(number,[readonly])
        sets the number in the cell and unhighlights
        readOnly=True sets the cell to be read-only'''
        self.number = number
        self.readOnly = readOnly
        self.unhighlight()  # unhighlight the cell after setting it
        # update the cell and check if we created any bad cells
        self.master.update_cells()

    def update_display(self, badCell=False):
        '''SudokuCell.update_display()
        displays the number in the cell
        displays as:
          empty if its value is 0
          black if user-entered and legal
          gray if read-only and legal
          red when badCell is True'''
        if self.number == 0:  # cell is empty
            self['text'] = ''
        else:  # cell has a number
            self['text'] = str(self.number)  # display the number
            # set the color
            if badCell:
                self['fg'] = 'red'
            elif self.readOnly:
                self['fg'] = 'dim gray'
            else:
                self['fg'] = 'black'

    def highlight(self, event):
        '''SudokuCell.highlight(event)
        handler function for mouse click
        highlights the cell if it can be edited (non-read-only)'''
        if not self.readOnly:  # only act on non-read-only cells
            self.master.unhighlight_all()  # unhighlight any other cells
            self.focus_set()  # set the focus so we can capture key presses
            self.highlighted = True
            self['bg'] = 'lightgrey'

    def unhighlight(self):
        '''SudokuCell.unhighlight()
        unhighlights the cell (changes background to white)'''
        self.highlighted = False
        self['bg'] = 'white'

    def change(self, event):
        '''SudokuCell.change(event)
        handler function for key press
        only works on editable (non-read-only) and highlighted cells
        if a number key was pressed: sets cell to that number
        if a backspace/delete key was pressed: deletes the number'''
        # only act if the cell is editable and highlighted
        if not self.readOnly and self.highlighted:
            if '1' <= event.char <= '9':  # number press -- set the cell
                self.set_number(int(event.char))
            elif event.keysym in ['BackSpace', 'Delete', 'KP_Delete']:
                # delete the cell's contents by setting it to 0
                self.set_number(0)

    def set_possibles(self, value):
        '''SudokuCell.set_possibles()
        sets the set of possible fills'''
        self.possibles = value

    def get_possibles(self):
        '''SudokuCell.get_possibles()
        gets the set of possible fills'''
        return self.possibles


class SudokuUnit:
    '''represents a Sudoku unit (row, column, or box)'''

    def __init__(self, cells):
        '''SudokuUnit(cells) -> SudokuUnit
        creates a new SudokuUnit with the SudokuCells in dict cells'''
        self.cells = cells  # store dict of SudokuCell's

    def get_coord_list(self):
        '''SudokuUnit.get_coord_list() -> list
        returns list of (row,column) tuples for cells'''
        return list(self.cells.keys())

    def get_cell_list(self):
        '''SudokuUnit.get_cell_list() -> list
        returns list of SudokuCells'''
        return list(self.cells.values())

    def contains_coord(self, coord):
        '''SudokuUnit.contains_coord(coord) -> bool
        returns True if (row,column) tuple is in unit, otherwise False'''
        return coord in self.cells  # looks for coord in keys

    def fill_in_only_possibles(self):
        '''SudokuUnit.fill_in_only_possibles() -> bool
        fills in any number with only one possible cell
        returns True if any get filled in, False if none get filled in'''
        makingProgress = False
        for number in range(1, 10):  # try each number
            possibleCells = []
            for cell in self.cells.values():
                # look at possible list for blank cells
                if cell.get_number() == 0 and \
                        number in cell.get_possibles():
                    possibleCells.append(cell)
            # see if we got only one cell
            if len(possibleCells) == 1:
                # place the number!
                possibleCells[0].set_number(number)
                makingProgress = True  # we're making progress!
        return makingProgress


class SudokuGrid(Frame):
    """object for a Sudoku grid"""

    def __init__(self, master):
        '''SudokuGrid(master)
        creates a new blank Sudoku grid'''
        # initialize a new Frame
        Frame.__init__(self, master, bg='black')
        self.grid()
        # put in lines between the cells
        # (odd numbered rows and columns in the grid)
        for n in range(1, 17, 2):
            self.rowconfigure(n, minsize=1)
            self.columnconfigure(n, minsize=1)
        # thicker lines between 3x3 boxes and at the bottom
        self.columnconfigure(5, minsize=3)
        self.columnconfigure(11, minsize=3)
        self.rowconfigure(5, minsize=3)
        self.rowconfigure(11, minsize=3)
        self.rowconfigure(17, minsize=1)  # space at the bottom
        # create buttons
        self.buttonFrame = Frame(self, bg='white')  # new frame to hold buttons
        Button(self.buttonFrame, text='Load Grid', command=self.load_grid).grid(row=0, column=0)
        Button(self.buttonFrame, text='Save Grid', command=self.save_grid).grid(row=0, column=1)
        Button(self.buttonFrame, text='Solve', command=self.solve).grid(row=0, column=2)
        Button(self.buttonFrame, text='Reset', command=self.reset).grid(row=0, column=3)
        self.buttonFrame.grid(row=18, column=0, columnspan=17)
        # create the cells
        self.cells = {}  # set up dictionary for cells
        for row in range(9):
            for column in range(9):
                coord = (row, column)
                self.cells[coord] = SudokuCell(self, coord)
                # cells go in even-numbered rows/columns of the grid
                self.cells[coord].grid(row=2 * row, column=2 * column)
        # set up units
        self.units = []  # set up list for units
        # do rows and columns at the same time
        for m in range(9):
            rowCells = {}  # dict of cells in row m
            columnCells = {}  # dict of cells in column m
            for n in range(9):  # loop through each row/column
                rowCells[(m, n)] = self.cells[(m, n)]
                columnCells[(n, m)] = self.cells[(n, m)]
            self.units.append(SudokuUnit(rowCells))  # add row unit
            self.units.append(SudokuUnit(columnCells))  # add column unit
        # create units for boxes
        for row in [0, 3, 6]:
            for column in [0, 3, 6]:
                boxCells = {}  # dict of cells in this box
                # loop over 3x3 region
                for i in range(3):
                    for j in range(3):
                        boxCells[(row + i, column + j)] = self.cells[(row + i, column + j)]
                self.units.append(SudokuUnit(boxCells))  # add box unit

    def unhighlight_all(self):
        '''SudokuGrid.unhighlight_all()
        unhighlight all the cells in the grid'''
        for cell in self.cells.values():
            cell.unhighlight()

    def find_units(self, coord):
        '''SudokuGrid.find_units(coord) -> list
        returns a list SudokuUnits containing (row,column) tuple coord'''
        return [unit for unit in self.units if unit.contains_coord(coord)]

    def update_cells(self):
        """SudokuGrid.update_cells()
        check for good/bad cells and update their color"""
        for coord in self.cells:
            cell = self.cells[coord]
            number = cell.get_number()
            foundBad = False
            # empty cell can't be bad
            if number == 0:
                cell.update_display(False)
                continue
            # check all units containing this cell
            for unit in self.find_units(coord):
                # loop through each cell in the unit
                for otherCoord in unit.get_coord_list():
                    if otherCoord == coord:  # skip this cell
                        continue
                    if self.cells[otherCoord].get_number() == number:
                        foundBad = True
            # update the cell
            cell.update_display(foundBad)

    def load_grid(self):
        '''SudokuGrid.load_grid()
        loads a Sudoku grid from a file'''
        # get filename using tkinter's open file pop-up
        filename = filedialog.askopenfilename(defaultextension='.txt')
        # make sure they chose a file and didn't click "cancel"
        if filename:
            # open the file and read rows into a list
            sudokufile = open(filename, 'r')
            rowList = sudokufile.readlines()
            sudokufile.close()
            # process file data
            for row in range(9):
                for column in range(9):
                    # get column'th character from line row
                    value = int(rowList[row][column])
                    # set the cell
                    # if value is nonzero, cell is read-only
                    self.cells[(row, column)].set_number(value, value != 0)

    def save_grid(self):
        '''SudokuGrid.save_grid()
        saves the Sudoku grid to a file'''
        # get filename using tkinter's save file pop-up
        filename = filedialog.asksaveasfilename(defaultextension='.txt')
        # make sure they chose a file and didn't click "cancel"
        if filename:
            sudokufile = open(filename, 'w')  # open file for writing
            for row in range(9):
                for column in range(9):
                    # add cell to file
                    sudokufile.write(str(self.cells[(row, column)].get_number()))
                sudokufile.write('\n')  # new row
            sudokufile.close()

    def reset(self):
        '''SudokuGrid.reset()
        clears all non-read-only cells'''
        for cell in self.cells.values():
            # only clear non-read-only cells
            if not cell.is_read_only():
                cell.set_number(0)

    def solve(self):
        '''SudokuGrid.solve()
        solves the Sudoku grid (if possible)
        pops up dialog box at the end indicating the solved status'''
        makingProgress = True
        while makingProgress:
            makingProgress = self.fill_in_no_brainers() or self.fill_in_only_possibles()

    def fill_in_no_brainers(self):
        '''SudokuGrid.fill_in_no_brainers() -> boolean
        fills in all the "no-brainer" squares: those squares can that
          take only one possible number
        returns True if any get filled in, False if none get filled in.'''
        makingProgress = False  # will get set to True if we fill something
        # set the possibles for each cell
        self.set_possibles()
        # loop through grid
        for cell in self.cells.values():
            # only consider blank cells
            if cell.get_number() == 0:
                continue
            possibles = cell.get_possibles()
            # check if only one number
            if len(possibles) == 1:
                num = possibles.pop()  # get the number
                cell.set_number(num)  # set the number
                makingProgress = True  # we've made progress!
        return makingProgress

    def set_possibles(self):
        '''SudokuGrid.set_possibles()
        sets the possibles set for each cell'''
        # loop through grid
        for coord in self.cells:
            cell = self.cells[coord]  # get the Sudoku cell
            # only consider blank cells
            if cell.get_number() != 0:
                continue
            # initialize with all numbers possible
            possibleNumbers = set(range(1, 10))
            # loop through each unit containing this cell
            for unit in self.find_units(coord):
                # loop through cells in that unit
                for unitCell in unit.get_cell_list():
                    possibleNumbers.discard(unitCell.get_number())
            cell.set_possibles(possibleNumbers)

    def fill_in_only_possibles(self):
        '''SudokuGrid.fill_in_only_possibles() -> boolean
        fills in any number with only one possible cell
        returns True if any get filled in, False if none get filled in'''
        makingProgress = False  # will get set to True if we fill something
        # set the possibles for each cell
        self.set_possibles()
        # loop through each row, column, and box
        for unit in self.units:
            makingProgress = makingProgress or unit.fill_in_only_possibles()
        return makingProgress

    def close(self):
        self.grid_remove()

class GUIDie(Canvas):
    '''6-sided Die class for GUI'''

    def __init__(self, master, valueList=[1, 2, 3, 4, 5, 6], colorList=['black'] * 6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self, master, width=60, height=60, bg='white', \
                        bd=5, relief=GROOVE)
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1

    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top - 1]

    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1, 7)
        self.draw()

    def draw(self):
        '''GUIDie.draw()
        draws the pips on the die'''
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [[(1, 1)],
                   [(0, 0), (2, 2)],
                   [(0, 0), (1, 1), (2, 2)],
                   [(0, 0), (0, 2), (2, 0), (2, 2)],
                   [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
                   [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)]]
        for location in pipList[self.top - 1]:
            self.draw_pip(location, self.colorList[self.top - 1])

    def draw_pip(self, location, color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx, centery) = (17 + 20 * location[1], 17 + 20 * location[0])  # center
        self.create_oval(centerx - 5, centery - 5, centerx + 5, centery + 5, fill=color)

    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)


class Shotput(Frame):
    '''frame for a game of 400 Meters'''

    def __init__(self, master, name):
        '''Decath400MFrame(master,name) -> Decath400MFrame
        creates a new 400 Meters frame
        name is the name of the player'''
        # set up Frame object
        Frame.__init__(self, master)
     
        # set up score, attempt,
        self.scoreLabel = Label(self, text='Attempt #1 Score: 0', font=('Arial', 18))
        self.scoreLabel.grid(row=0, column=3, columnspan=2)
        self.highscoreLabel = Label(self, text='Highscore: 0', font=('Arial', 18))
        self.highscoreLabel.grid(row=0, column=5, columnspan=3, sticky=E)
        # initialize game data
        self.score = 0
        self.highscore = 0
        self.attempt = 1
        self.gameround = 0
        # set up dice
        self.dice = []

        for n in range(8):
            self.dice.append(GUIDie(self, [1, 2, 3, 4, 5, 6], ['red'] + ['black'] * 5))
            self.dice[n].grid(row=1, column=n)
        # set up buttons
        self.rollButton = Button(self, text='Roll', command=self.roll)
        self.rollButton.grid(row=2, columnspan=1)
        self.stopButton = Button(self, text='Stop', state=DISABLED, command=self.stop)
        self.stopButton.grid(row=3, columnspan=1)

    def roll(self):
        '''Decath400MFrame.roll()
        handler method for the roll button click'''
        # roll the die!
        if self.gameround < 7:
            self.dice[self.gameround].roll()
            self.keep()
        elif self.gameround == 7:
            self.dice[self.gameround].roll()
            self.keep()
            self.stopButton.grid_remove()
            self.rollButton.grid_remove()
        else:
            self.stop()
        # if it's the first round of this attempt, enable the stop button
        if self.stopButton['state'] == DISABLED:
            self.stopButton['state'] = ACTIVE

    def keep(self):
        '''Decath400MFrame.keep()
        handler method for the keep button click'''
        # add dice to score and update the scoreboard
        die = self.dice[self.gameround].get_top()
        if die == 1:
            self.rollButton['state'] = DISABLED
            self.score = 0
            self.scoreLabel['text'] = 'Fouled attempt'
            self.stopButton['text'] = 'FOUL'
        else:
            self.score += die
            self.scoreLabel['text'] = 'Attempt #' + str(self.attempt) + 'Score: ' + str(self.score)
            self.gameround += 1  # go to next round
            self.rollButton.grid(row=2, column=self.gameround, columnspan=1)
            self.stopButton.grid(row=3, column=self.gameround, columnspan=1)

    def stop(self):
        self.rollButton['state'] = ACTIVE

        self.attempt += 1
        if self.highscore < self.score:
            self.highscore = self.score
            self.highscoreLabel['text'] = 'Highscore: ' + str(self.highscore)
        self.score = 0
        if self.attempt == 4:
            self.scoreLabel['text'] = 'Game over'
            self.rollButton.grid_remove()
            self.stopButton.grid_remove()
        else:

            self.scoreLabel['text'] = 'Attempt #' + str(self.attempt) + 'Score: ' + str(self.score)
            for n in self.dice:
                n.erase()

            # reset the score for the new attempt
            score = 0
            # reset the round for the new attempt
            self.gameround = 0
            # bring the buttons back to the start position
            self.stopButton['text'] = 'Stop'
            self.rollButton.grid(row=2, column=self.gameround, columnspan=2)

            self.stopButton.grid(row=3, column=self.gameround, columnspan=2)
    def close(self):
        self.grid_remove()

