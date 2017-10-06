from classes.game import Person, bcolors, Utilities
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Black Magic

fire = Spell("Fire",10,120,"black")
thunder = Spell("Thunder",10,120,"black")
blizzard = Spell("Blizzard",10,120,"black")
meteor = Spell("Meteor",20,200,"black")
quake = Spell("Quake",14,140,"black")
black_magick = [fire, thunder, blizzard, meteor, quake]

# Create White Magic

cure = Spell("Cure", 12, 120, 'white')
cura = Spell('Cura', 18, 200, 'white')
white_magick = [cure, cura]


# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50, 3)
hi_potion = Item("Hi-Potion", "potion", "Heals 100 HP", 100, 1)
super_potion = Item("Super-Potion", "potion", "Heals 500 HP", 500, 1)
elixir = Item("Elixir", "elixir", "Replenishes the mp and hp of a party "
                                  "member", 9999, 1)
hi_elixir = Item("Hi-Elixer", "elixir", "Replenishes the whole party's hp and "
                                       "mp", 9999, 1)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500, 2)

# player inventory
player_items = [potion, hi_potion, super_potion, elixir, hi_elixir, grenade]

# Instantiate player and enemy
player_Boromir = Person("Boromir", 450, 65, 60, 34, black_magick + white_magick,
                player_items)
player_Rohomir = Person("Rohomir", 420, 85, 20, 34, black_magick + white_magick,
                player_items)
player_Bob = Person("Bob", 150, 150, 300, 34, black_magick + white_magick,
                player_items)

players = [player_Boromir, player_Rohomir, player_Bob]

enemy_Nazgul = Person("Nazgul", 1200, 60, 45, 25, [], [])
enemy_Klex = Person("Klex", 1200, 60, 45, 25, [], [])

enemies = [enemy_Nazgul,enemy_Klex]


# MAIN LOOP

running = True

print("\n", "\n")
utilities = Utilities()


while running:
    if utilities.team_status(players):
        utilities.end_turn(players, enemies)
        utilities.player_turn(players, enemies, running)
        if utilities.team_status(enemies) == False:
            running = False
        utilities.enemy_turn(players, enemies, running)
        if utilities.team_status(players) == False:
            running = False


#TODO make choose target error proof
#TODO: smooth out the win and loose printouts, avoid duplicating