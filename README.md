***ft_minirogue Project in Python3***

**Window**
--> handled with Ncurses 										[OK]

**ENV**

-->	Handle interactions between Player and rest of the game		[OK]
--> Count Turns													[OK]
1 turn equals to:
	--> Moving (Hitting monsters) or interacting with the Dungeon
	--> Inventory Action
--> Keep track of the score 									[OK]
--> If (HP == 0) trigger ENDGAME;								[OK]
--> Save the game ?													[KO]

**Map**

--> Randomly Generated												[KO]
--> Hardcoded													[OK]

--> Store Every Objects Position on the Map						[OK]

=TILE=
* Empty ' '
* Free '.'
* Wall '#'
* Player '@'
* Monster '[A-Z]'
* Treasure '!$%^\&\*'

2 states:														[OK]
* explored
	--> visible
* unexplored
	--> hidden

**Player**

--> different Classes											[OK]
	--> Fighter
	--> Thief
	--> Dwarf
	--> Wizard
		--> Magic!

--> Position													[OK]

--> XP	(Level)													[OK]
--> Health Points												[OK]
--> Strength (Attack Points, more with weapons)					[OK]
--> Defense Points (Upgraded by the Equipment)					[OK]
--> Vision (upgraded with torches)								[OK]

--> Inventory (*i*)												[OK]
	--> Use One-Time Item (Potion, Magic Scroll...)
	--> Equip Equipment (Armor...)

=METHODS=

* Move around, in 4/8 directions								[OK]
	--> Can't go through Walls
	--> Hit Monsters if Any
* Get an object lying on the ground (*g*)						[OK]

**Monsters**

2 States:														[OK]
* Asleep
	--> Don't move
* Awaken
	--> Will Follow The Player and try to hit him

--> Strength													[OK]
--> Position													[OK]
	--> Random														[KO]
--> HP															[OK]
--> XPoints														[OK]

=METHODS=
* FollowPlayer(playerPos)										[OK]
	--> triggered when Monster'State is Awaken
* HitPlayer														[OK]
	--> triggered when one tile near player


**Treasures**

--> Position													[OK]
	--> Random														[KO]
--> Points														[OK]
--> Type														[WIP]
	--> Equipment (Weapons, torches...)
	--> One-Use Items (Potion...)
	--> Magic Stuff
	-->	Garbage to sell
	--> ...

NPC						[MAYBE]
--> Shops?
--> Storytellers...


Mettre de la couleur
Faire Scroller l'écran en fonction des salles ?
