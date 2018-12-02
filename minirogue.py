from objets import *
from title import *
from env import *
import curses
import random

env = Env()

#Add new Monsters Here
env.add_monsters([
#		x  y  symbole name HP strength sensitivity xp state
Monster(6, 36, 'R', "Rat",  2,    5,    		8,	10),
Monster(6, 12, 'B', "Chauve-Souris", 5, 8, 10),
Monster(11, 3, 'D', "Dragon", 40, 25, 5, 70),
Monster(6, 54, 'G', "Golbargh", 100, 15, 2, 150),

])

#Add new Treasures Here
env.add_treasures([

Treasure(5, 8, '&', "Sacoche en Cuir", 12),
Treasure(14, 3, '\'', "Dent d'ours", 8),
Treasure(17, 35, '$', "Piece d'or", 20),
Treasure(3, 15, '*', "Viande avariée", 2),
Treasure(16, 51, '/', "Courte Dague", 14, 'Weapon', 3),
Treasure(2, 42, '|', "Longue Epee", 14, 'Weapon', 6),
Treasure(18, 8, '^', "Casque en Os", 14, 'Armor', 4),
Treasure(1, 1, 'i', "Torche humide", 3, 'Light', 3)
])

def init_curse():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(False)
    stdscr.nodelay(False)
    return stdscr

def exit_homescreen(stdscr):
    stdscr.erase()
    stdscr.addstr('Pretty Scary, Eh ?')
    stdscr.addstr(2, 0, 'Press any key to continue..')
    stdscr.getch()
    stdscr.refresh()
    end_curse(stdscr) 

def exit_game(stdscr, player, death):
    stdscr.erase()
    if (death == 1):
        stdscr.addstr(0, 0, "You tried hard to survive but, still, you died from Death after " + str(env.tours) + " Turns, earning " + str(env.score) + " Points and reaching level " + str(player.level) + " (" + str(player.xp) + " XP). Well Done Though !\n")
    else:
        stdscr.addstr(0, 0, "You've played " + str(env.tours) + " Turns, earned " + str(env.score) + " Points and reached level " + str(player.level) + " (" + str(player.xp) + " XP). Congratulations !\n")
    stdscr.addstr(2, 0, 'Press any key to continue..')
    stdscr.getch()
    stdscr.refresh()
    end_curse(stdscr)

def end_curse(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    exit(0)

def show_tile(stdscr, tile, player):
    if dist(player, tile) <= player.vision:
        tile.discover = True
        stdscr.addch(tile.x, tile.y, tile.sy, curses.A_BOLD)
    elif (tile.discover) and (tile.alive):
        stdscr.addch(tile.x, tile.y, '.' , curses.A_DIM)
    elif (tile.discover):
        stdscr.addch(tile.x, tile.y, tile.sy , curses.A_DIM)
    else:
        stdscr.addch(tile.x, tile.y, ' ')

def show_map(stdscr, player):
    stdscr.erase()
    for x, row in enumerate(env.field):
        for y, tile in enumerate(row):
            show_tile(stdscr, tile[-1], player)
    stdscr.addch(player.x, player.y, '@')

def pick_item(stdscr, player):
    if (env.field[player.x][player.y][-1].type == 'treasure'):
        for t in env.treasure:
            if (t.x == player.x and t.y == player.y):
                 stdscr.addstr(20, 0, 'You found a ' + t.name + ' !')             
                 stdscr.getch()
                 stdscr.refresh()
                 player.get_treasure(t)
                 env.score += t.points
                 env.treasure.remove(t)
                 env.field[t.x][t.y].pop()

def show_inventory(stdscr, player):
    stdscr.move(20, 0)
    for s in player.equipment:
        stdscr.addstr(s.name + '\n')
    stdscr.addstr('\nPress any key to continue..')
    stdscr.getch()
    stdscr.refresh()

def player_turn(stdscr, player):
    c = stdscr.getch()
    if (c == 27):
        exit_game(stdscr, player, 0)
    elif (c == curses.KEY_LEFT or c == curses.KEY_RIGHT or c == curses.KEY_UP or c == curses.KEY_DOWN or (c >= ord('1') and c <= ord('9') and c != ord('5'))):
        player.move(stdscr, c, env)
    elif (c == ord('g')): 
        pick_item(stdscr, player)
    elif (c == ord('i')):
        show_inventory(stdscr, player)

def random_place(field):
    pos = [0, 0]
    while (field[pos[0]][pos[1]][0].sy != '.' and field[pos[0]][pos[1]][-1].type != 'monster' ):
        pos = [random.randrange(1, 18), random.randrange(1, 55)]
    return (pos)

def display_info(stdscr, player):
    win = stdscr.getmaxyx()
    stdscr.addstr(win[0] - 1, 0, 'Lvl: ' + str(player.level) + ' HP: ' + str(player.hp) + ' Strength: ' + str(player.strength) + ' Armor: ' + str(player.resistance) + ' XP: ' + str(player.xp))

def main():
    stdscr = init_curse()
    Class = choose(stdscr)
    if (Class == None):
       exit_homescreen(stdscr)
    pos = random_place(env.field)
    player = Class(pos[0], pos[1])
    while (1):
        show_map(stdscr, player)
        display_info(stdscr, player)
        player_turn(stdscr, player)
        env.turn(stdscr, player)
        if (player.hp <= 0):
            exit_game(stdscr, player, 1)

if __name__ == '__main__':
    main()

