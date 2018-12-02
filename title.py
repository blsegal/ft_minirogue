from objets import *
import curses

TITLE   = '''
           __ __ ___      ____ 
          / // /|__ \    / __ \____  ____ ___  _____
         / // /___/ /   / /_/ / __ \/ __ `/ / / / _ \\
        /__  __/ __/   / _, _/ /_/ / /_/ / /_/ /  __/
          /_/ /____/  /_/ |_|\____/\__, /\__,_/\___/
                                  /____/'''

CURSOR  = 'ᐅ  '
CLASS   = 'Choose your class :'
ENTER   = 'Press Enter to choose'
NAMES = ['Fighter', 'Dwarf', 'Thief', 'Wizard']
CLASSES = [Fighter, Dwarf, Thief, Wizard]

def show_classes(stdscr, choose):
    for i, c in enumerate(NAMES):
        if i != choose:
            stdscr.addstr(12 + i, 12, c, curses.A_DIM)
        else:
            stdscr.addstr(12 + i, 9, CURSOR + c, curses.A_BOLD)

def choose(stdscr):
    choose = 0
    stop = True
    while (stop):
        stdscr.erase()
        show_title(stdscr)
        show_classes(stdscr, choose)
        key = stdscr.getch()
        if (key == 10):
            stop = False
        elif (key == 27):
            return None
        elif (key == curses.KEY_UP):
            choose -= 1
        elif (key == curses.KEY_DOWN):
            choose += 1
        choose %= 4
    return CLASSES[choose]

def show_title(stdscr):
    stdscr.addstr(TITLE)
    stdscr.addstr(10, 3, CLASS)
    stdscr.addstr(18, 3, ENTER)
