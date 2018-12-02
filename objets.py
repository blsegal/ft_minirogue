import curses
import random

class Tile:
    def __init__(self, x, y, type = 'map', symbole = ' ', alive = False):
        self.x = x
        self.y = y
        self.type = type
        self.sy = symbole
        self.alive = alive
        self.discover = False

class Void(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, x, y)

class Free(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, x, y, 'map', '.')

class Wall(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, x, y, 'map', '#')

class Treasure(Tile):
    def __init__(self, x, y, symbole, name, points, kind = 'Garbage', bonus = 0):
        Tile.__init__(self, x, y, 'treasure', symbole)
        self.name = name
        self.points = points
        self.kind = kind
        self.bonus = bonus 

class Monster(Tile):
    def __init__(self, x, y, symbole, name, healthPoints, strength, sensitivity, xp = 20, state = 'asleep'):
        Tile.__init__(self, x, y, 'monster', symbole, True)
        self.hp = healthPoints
        self.name = name
        self.strength = strength
        self.sensitivity = sensitivity
        self.xp = xp
        self.state = state

    def followPlayer(self, stdscr, player, field):
        dx = player.x - self.x
        dy = player.y - self.y
        field[self.x][self.y].pop()
        if ((abs(dx) == 1 and abs(dy) == 1) or (abs(dx) == 1 and dy == 0) or (dx == 0 and abs(dy) == 1)):
            self.hitplayer(stdscr, player)
        elif (abs(dx) > abs(dy)):
                if (dx > 0 and field[self.x + 1][self.y][0].sy == '.' and field[self.x + 1][self.y][-1].type != 'monster'):
                    self.x += 1
                elif (dx < 0 and field[self.x - 1][self.y][0].sy == '.' and field[self.x + 1][self.y][-1].type != 'monster'):
                    self.x -= 1
        elif (abs(dx) < abs(dy)):
                if (dy > 0 and field[self.x][self.y + 1][0].sy == '.' and field[self.x + 1][self.y][-1].type != 'monster'):
                    self.y += 1
                elif (dy < 0 and field[self.x][self.y - 1][0].sy == '.' and field[self.x + 1][self.y][-1].type != 'monster'):
                    self.y -= 1
        elif (abs(dx) == abs(dy)):
                if (dx > 0 and dy > 0 and field[self.x + 1][self.y + 1][0].sy == '.' and field[self.x + 1][self.y][-1].type != 'monster'):
                    self.x += 1
                    self.y += 1
                elif (dx > 0 and dy < 0 and field[self.x + 1][self.y - 1][0].sy == '.' and field[self.x + 1][self.y][-1].type != 'monster'):
                    self.x += 1
                    self.y -= 1
                elif (dx < 0 and dy > 0 and field[self.x - 1][self.y + 1][0].sy == '.' and field[self.x + 1][self.y][-1].type != 'monster'):
                    self.x -= 1
                    self.y += 1
                elif (dx < 0 and dy < 0 and field[self.x - 1][self.y - 1][0].sy == '.' and field[self.x + 1][self.y][-1].type != 'monster'):
                    self.x -= 1
                    self.y -= 1
        field[self.x][self.y].append(self)

    def hitplayer(self, stdscr, player):
        if (random.randrange(2) == 1):
            stdscr.addstr(22, 0, 'The ' + self.name + ' hits you! You\'ve lost ' + str(self.strength - player.resistance) + ' HP.')
            player.hp -= (self.strength - player.resistance)
            if (player.hp <= 0):
                stdscr.addstr(23, 0, 'This ' + self.name + ' just got your back. So bad...')

        else:
            stdscr.addstr(22, 0, 'The ' + self.name + ' misses you!')
        stdscr.refresh()
        stdscr.getch()

class Player(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, x, y, 'player', '@', True)
        self.equipment = []
        self.level = 1
        self.xp = 0
 
    def get_treasure(self, tresor):
        self.equipment.append(tresor)
        if tresor.kind == 'Armor':
            self.resistance += tresor.bonus
        elif tresor.kind == 'Weapon':
            self.strength += tresor.bonus
        elif tresor.kind == 'Light':
            self.vision += tresor.bonus

    def move(self, stdscr, c, env):
         if (c == ord('7') and env.field[self.x - 1][self.y - 1][0].sy == '.'):
             if (env.field[self.x - 1][self.y - 1][-1].type == 'monster'):
                 self.hitmonster(stdscr, env, self.x - 1, self.y - 1)
             else:
                 self.x -= 1
                 self.y -= 1
         elif ((c == ord('8') or c == curses.KEY_UP) and env.field[self.x - 1][self.y][0].sy == '.'):
             if (env.field[self.x - 1][self.y][-1].type == 'monster'):
                 self.hitmonster(stdscr, env, self.x - 1, self.y)
             else:
                 self.x -= 1
         elif (c == ord('9') and env.field[self.x - 1][self.y + 1][0].sy == '.'):
             if (env.field[self.x - 1][self.y + 1][-1].type == 'monster'):
                 self.hitmonster(stdscr, env, self.x - 1, self.y + 1)
             else:
                 self.x -= 1
                 self.y += 1
         elif ((c == ord('4') or c == curses.KEY_LEFT) and env.field[self.x][self.y - 1][0].sy == '.'):
             if (env.field[self.x][self.y - 1][-1].type == 'monster'):
                 self.hitmonster(stdscr, env, self.x, self.y - 1)
             else:
                 self.y -= 1
         elif ((c == ord('6') or c == curses.KEY_RIGHT) and env.field[self.x][self.y + 1][0].sy == '.'):
             if (env.field[self.x][self.y + 1][-1].type == 'monster'):
                 self.hitmonster(stdscr, env, self.x, self.y + 1)
             else:
                 self.y += 1
         elif (c == ord('1') and env.field[self.x + 1][self.y - 1][0].sy == '.'):
             if (env.field[self.x + 1][self.y - 1][-1].type == 'monster'):
                 self.hitmonster(stdscr, env, self.x + 1, self.y - 1)
             else:
                 self.x += 1
                 self.y -= 1
         elif ((c == ord('2') or c == curses.KEY_DOWN) and env.field[self.x + 1][self.y][0].sy == '.'):
             if (env.field[self.x + 1][self.y][-1].type == 'monster'):
                 self.hitmonster(stdscr, env, self.x + 1, self.y)
             else:
                 self.x += 1
         elif (c == ord('3') and env.field[self.x + 1][self.y + 1][0].sy == '.'):
             if (env.field[self.x + 1][self.y + 1][-1].type == 'monster'):
                 self.hitmonster(stdscr, env, self.x + 1, self.y + 1)
             else:
                 self.x += 1
                 self.y += 1


    def hitmonster(self, stdscr, env, x, y):
        for m in env.monster:
            if(m.x == x and m.y == y):
                m.hp -= self.strength
                stdscr.addstr(22, 0, 'You hit the ' +  m.name + '. It losts ' + str(self.strength) + ' HP')
                if (m.hp <= 0):
                    stdscr.addstr(' and is dead now. Its blood starts spreading all over the place...')
                    self.xp += m.xp
                    self.levelup(stdscr)
                    env.monster.remove(m)
                    env.field[x][y].pop()
        stdscr.refresh()
        stdscr.getch()

    def levelup(self, stdscr):
        if (self.level == 1 and self.xp >= 20):
            self.level += 1
            stdscr.addstr(23, 0, 'Welcome to level 2 !')
        if (self.level == 2 and self.xp >= 50):
            self.level += 1
            stdscr.addstr(23, 0, 'Welcome to level 3 !')
        if (self.level == 3 and self.xp >= 100):
            self.level += 1
            stdscr.addstr(23, 0, 'Welcome to level 4 !')
        if (self.level == 3 and self.xp >= 200):
            self.level += 1
            stdscr.addstr(23, 0, 'Welcome to level 5 !')

class Fighter(Player):
    STRENGTH = 10       # to hit monsters
    RESISTANCE = 3      # to stand against Monster hit (damage_taken = monster.attack - self.RESISTANCE)
    VISION = 4          # to see in the gloomy corridors...
 
    def __init__(self, x = 1, y = 1, healthPoints = 40):
        Player.__init__(self, x, y)
        self.hp = healthPoints
        self.strength = self.STRENGTH
        self.resistance = self.RESISTANCE
        self.vision = self.VISION


class Dwarf(Player):
    MAX_HP = 30
    STRENGTH = 8
    RESISTANCE = 5
    VISION = 4

    def __init__(self, x = 1, y = 1, healthPoints = 30):
        Player.__init__(self, x, y)
        self.hp = healthPoints
        self.strength = self.STRENGTH
        self.resistance = self.RESISTANCE
        self.vision = self.VISION
# Heal by walking (until MAX_HP is reached) and get free beers!

class Thief(Player):
    STRENGTH = 7
    RESISTANCE = 2
    VISION = 6

    def __init__(self, x = 1, y = 1, healthPoints = 25):
        Player.__init__(self, x, y)
        self.hp = healthPoints
        self.strength = self.STRENGTH
        self.resistance = self.RESISTANCE
        self.vision = self.VISION
#Can Unlock Doors and much more

class Wizard(Player):
    STRENGTH = 5
    RESISTANCE = 0
    VISION = 7

    def __init__(self, x = 1, y = 1, healthPoints = 20):
        Player.__init__(self, x, y)
        self.hp = healthPoints
        self.strength = self.STRENGTH
        self.resistance = self.RESISTANCE
        self.vision = self.VISION

#Can use Magic!
