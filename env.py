from objets import *

def create(tile, x, y):
    if tile == '#':
        return Wall(x, y)
    elif tile == '.':
        return Free(x, y)
    else:
        return Void(x, y)

def dist (player, obj):
    return ((((player.x - obj.x) * 2) ** 2 + (player.y - obj.y) ** 2) ** 0.5)


class Env:
    def __init__(self):
        self.tours = 0
        self.score = 0
        self.map = ["#########################       #############              ",
                    "#.......................#       #...........#              ",
                    "#.......................#########...........#              ",
                    "#...........................................#    ##########",
                    "#.......................#########...........#    #........#",
                    "#.......................#       #...........######........#",
                    "###########..############       #.........................#",
                    "          #..#                  #...........######........#",
                    "          #..#                  #...........#    #........#",
                    "###########..#####              #####..######    #........#",
                    "#................#                  #..#         ####..####",
                    "#................#                  #..#            #..#   ",
                    "#................#          #########..#####        #..#   ",
                    "#................#          #..............#     ####..####",
                    "#................############..............#     #........#",
                    "#..........................................#     #........#",
                    "#................############..............#######........#",
                    "#................#          #.............................#",
                    "#................#          #..............#######........#",
                    "##################          ################     ##########"]

        self.init_map()
    
    def init_map(self):
        self.field = []
        for x, row in enumerate(self.map):
            self.field.append([[create(tile, x, y)] for y, tile in enumerate(row)])

    def add_monsters(self, monsters):
        self.monster = monsters
        for m in self.monster:
            self.field[m.x][m.y].append(m)

    def add_treasures(self, treasures):
        self.treasure = treasures
        for t in self.treasure:
            self.field[t.x][t.y].append(t)

    def turn(self, stdscr, player):
        self.tours += 1
        for m in self.monster:
            if (m.state == 'awaken'):
                m.followPlayer(stdscr, player, self.field)
            elif (dist(player, m) <= m.sensitivity):
                m.state = 'awaken'

