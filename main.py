from classes.game import Person, bcolors, Utilities
from classes.magic import Spell
from classes.inventory import Item

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
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hi_potion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
super_potion = Item("Super-Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Replenishes the mp and hp of a party "
                                  "member", 9999)
hi_elixir = Item("Hi-Elixer", "elixir", "Replenishes the whole party's hp and "
                                       "mp", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# player inventory
player_items = [potion, hi_potion, super_potion, elixir, hi_elixir, grenade]

# Instantiate player and enemy
player = Person(450, 65, 60, 34, black_magick + white_magick, player_items)
enemy = Person(1200, 60, 45, 25, [], [])


# MAIN LOOP

running = True


print(bcolors.FAIL + bcolors.BOLD, "An enemy attacks" + bcolors.ENDC)

while running:
    print("=======================================")
    utilities = Utilities()
    player.choose_action()
    choice = input("Choose action: ")
    index = int(choice) - 1

    print("You chose: ", choice)

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("You attacked for: ", dmg, " points of damage", "Enemy HP: ",
              enemy.get_hp())

    elif index == 1:
        player.choose_magic()
        magic_choice = int(input("Choose magic: ")) - 1
        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_damage()
        current_mp = player.get_mp()

        if magic_choice == -1:
            continue

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\nNot enough mana\n" + bcolors.ENDC)
            continue

        if spell.type == "white":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\nYour spell ", spell.name, " heals ",
                  str(magic_dmg), " amount of damage\n" + bcolors.ENDC)

        elif spell.type == 'black':
            enemy.take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\nYour spell ", spell.name, " deals ",
                  str(magic_dmg), " damage to the enemy\n" + bcolors.ENDC)

        player.reduce_mp(spell.cost)

    elif index == 2:
        player.choose_item()
        item_choice = int(input("Choose item: ")) - 1
        item = player.items[item_choice]

        if item_choice == -1:
            continue
        elif item.type == 'potion':
            player.heal(item.prop)
            print(bcolors.OKGREEN + "\n" + item.name + " heals: " + str(
                item.prop) + " hit points" + bcolors.ENDC)

        elif item.type == "elixir":
            player.hp = player.maxhp
            player.mp = player.maxmp


    utilities.end_turn(player, enemy)
    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("The enemy attacks! You were hit for: ", enemy_dmg, " Yor HP is: ",
          player.get_hp())

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    elif player.get_hp() == 0:
        print(bcolors.FAIL + "You have lost!" + bcolors.ENDC)
        running = False


