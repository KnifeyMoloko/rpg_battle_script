

import random
from .magic import Spell
from collections import OrderedDict

indent = "    "

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Utilities:
    def __init__(self):
        self.running = True

    def end_turn(self, players, enemies):
        print(bcolors.BOLD + "=======================================" +
              bcolors.ENDC, "\n")

        for player in players:
            player.is_dead(players)
            self.blocky_view(player)

        for enemy in enemies:
            enemy.is_dead(enemies)
            self.blocky_view(enemy)

    def blocky_view(self, person):
        """for c in range(1,int(0x10FF)):
            print(str(c), chr(c))"""
        block_char = chr(9960)
        underscore = "_"
        hp = person.get_hp()
        mp = person.get_mp()
        max_hp = person.get_max_hp()
        max_mp = person.get_max_mp()

        hp_size = int(max_hp / 20)
        mp_size = int(max_mp / 10)

        print(bcolors.BOLD + person.name + bcolors.ENDC)

        if hp != max_hp:
            current_hp = hp_size -(hp_size - int(hp / 20))
            underscore_size = hp_size - current_hp
            print(indent, bcolors.OKGREEN + bcolors.BOLD + "|" + current_hp *
                  block_char + underscore * underscore_size + "|" +
                  bcolors.ENDC)

        else:
            print(indent, bcolors.OKGREEN + "|" + hp_size * block_char + "|"
                  + bcolors.ENDC)

        print(indent, bcolors.OKGREEN + bcolors.BOLD
              + "HP: " + str(hp) + "/" + str(max_hp) + bcolors.ENDC)

        if mp != max_mp:
            current_mp = mp_size - (mp_size - int(mp / 10))
            underscore_size_mp = mp_size - current_mp
            print(indent, bcolors.BOLD + bcolors.OKBLUE + "|" + current_mp *
                  block_char + underscore * underscore_size_mp + "|" +
                  bcolors.ENDC)
        else:
            print(indent, bcolors.BOLD + bcolors.OKBLUE + "|" + mp_size *
                  block_char + "|" + bcolors.ENDC)

        print(indent, bcolors.OKBLUE + bcolors.BOLD + "MP: " + str(mp) +
              "/" + str(max_mp) + bcolors.ENDC + "\n")

    def team_status(self, lst):
        if len(lst) != 0:
            for element in lst:
                element.is_dead(lst)
                if len(lst) == 0:
                    self.running = False
                    return False
                else:
                    return True

        else:
            self.running = False
            return False

    def player_turn(self, players, enemies):
        # check if there's a win or loose condition occurring
        self.win_or_loose(players, enemies)

        for player in players:
            if self.running:
                print(bcolors.BOLD + player.name + bcolors.ENDC + "\n")
                player.choose_action(players, enemies, self)
                self.win_or_loose(players, enemies)

    def enemy_turn(self, players, enemies):

        for enemy in enemies:
            if self.running:
                enemy_dmg = enemy.generate_damage()
                who_to_attack = random.choice(players)
                who_to_attack.take_damage(enemy_dmg)
                print("The enemy attacks!" + "\n" + "You were hit for: " +
                      bcolors.FAIL + str(enemy_dmg) + bcolors.ENDC +
                      " points of damage" + "\n")
                enemy.choose_action(players, enemies, self)
                self.win_or_loose(players, enemies)

    def win_or_loose(self, players, enemies):
        """checks for win condition: all enemies dead or loose condition:
        player team dead"""

        if not self.team_status(players):
            print(bcolors.BOLD + bcolors.FAIL + "All of your heroes are "
                                                "dead! You have lost to "
                                                "your enemies" +
                  bcolors.ENDC)

        if not self.team_status(enemies):
            print("\n" + bcolors.BOLD + bcolors.HEADER + "You're "
            "foes lie slain before you! You are victorious!" + bcolors.ENDC)

    def input_check(self, input_value, value_range, callback, *args):
        """generic checker function that checks if input is numeric and is in a
        given range, otherwise throws an error prompt and executes a callback
        (usually the same function) over with an arbitrary arg list"""
        while input_value.isnumeric() is False or int(input_value) - 1 not in \
                value_range:
            print("Your input is incorrect. You should be ashamed. Try "
                  "again." + "\n")
            return callback(*args)
        else:
            return True


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ("Attack", "Magic", "Items")

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg

        if self.hp <= 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self, players, enemies, utility):
        print(bcolors.OKGREEN + bcolors.BOLD + "Actions : " + bcolors.ENDC)

        i = 1

        for action in self.actions:
            print(str(i) + " : " + action)
            i += 1

        choice = input("Choose action: ")

        if utility.input_check(choice, range(0, len(self.actions)),
                               self.choose_action, players, enemies, utility):
            choice_index = int(choice) - 1
            print("You chose: ", choice)

            if choice_index == 0:
                dmg = self.generate_damage()
                target = self.choose_target(enemies, utility)
                print(type(target))
                print(target)
                enemies[target].take_damage(dmg)
                print("You attacked for:",
                      bcolors.FAIL + str(dmg) + bcolors.ENDC
                      + " points of damage" + "\n")
                enemies[target].is_dead(enemies)

            elif choice_index == 1:
                self.choose_magic(players, enemies, utility)

            elif choice_index == 2:
                self.choose_item(players, enemies, utility)

    def choose_magic(self, players, enemies, utility):
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "Magic : " + bcolors.ENDC)

        num = 1

        for i in self.magic:
            print(indent, str(num) + ": " + i.name, "(" + "cost: " + str(
                i.cost) + ")")
            num = num + 1

        magic_choice = input("Choose magic: ")

        if utility.input_check(magic_choice, range(0, len(self.magic)),
                               self.choose_magic, players, enemies, utility):

            magic_choice = int(magic_choice) - 1
            spell = self.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = self.get_mp()

            if magic_choice == -1:
                self.choose_magic(players, enemies, utility)

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough mana\n" + bcolors.ENDC)
                self.choose_magic(players, enemies, utility)

            if spell.type == "white":
                target = self.choose_target(players, utility)
                players[target].heal(magic_dmg)
                print(bcolors.OKBLUE + "\nYour spell ", spell.name,
                      " heals ", players[target].name, "for ", str(magic_dmg),
                      " amount of hit points" + bcolors.ENDC)
                self.reduce_mp(spell.cost)

            elif spell.type == 'black':
                target = self.choose_target(enemies, utility)
                enemies[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\nYour spell ", spell.name,
                      " deals ", str(magic_dmg), " damage to " +
                      enemies[target].name + "\n" + bcolors.ENDC)
                self.reduce_mp(spell.cost)
                enemies[target].is_dead(enemies)

    def choose_item(self, players, enemies, utility):
        num = 1

        print("\n" + bcolors.OKGREEN + "ITEMS:" + "\n" + bcolors.ENDC)

        for i in self.items:
            print(indent, str(num),  i.name, ": " + i.description + " (" +
                  str(i.quantity) + ")")
            num = num + 1

        item_choice = input("Choose item: ")

        if utility.input_check(item_choice, range(0, len(self.items)),
                            self.choose_item, players, enemies, utility):
            item_choice = int(item_choice) - 1
            item = self.items[item_choice]

            if item_choice == -1:
                self.choose_item(players, enemies, utility)
            elif item.quantity == 0:
                print(
                    bcolors.WARNING + "You don't have any items of this type in"
                                      "your inventory" + bcolors.ENDC)
                self.choose_item(players, enemies, utility)

            elif item.type == 'potion':
                self.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals: " + str(
                    item.prop) + " hit points" + bcolors.ENDC)

            elif item.type == "elixir":
                self.hp = self.maxhp
                self.mp = self.maxmp
                item.reduce_quantity(1)
                print(bcolors.OKGREEN + "HP and MP fully restored" + "\n" +
                      bcolors.ENDC)
                print(bcolors.BOLD + "You have " + str(item.quantity) + "of" +
                      item.name + " left in your inventory" + bcolors.ENDC)

            elif item.type == 'attack':
                target = self.choose_target(enemies, utility)
                enemies[target].take_damage(item.prop)
                item.reduce_quantity(1)
                print(bcolors.FAIL + "The enemy was hit by your " + item.name +
                      " for " + str(item.prop) + " hit points" + bcolors.ENDC)
                print(bcolors.BOLD + "You have " + str(item.quantity) + " of " +
                      item.name + " left in your inventory." + "\n" +
                      bcolors.ENDC)
                enemies[target].is_dead(enemies)

    def choose_target(self, arr, utility):
        print(self.name, " choose your target: \n")
        i = 1

        for element in arr:
            print(indent, str(i), element.name)
            i += 1

        target_index = input("Your choice is: ")

        if utility.input_check(target_index, range(0, len(arr)),
                               self.choose_target, arr, utility):
            target_index = int(target_index) - 1
            return target_index
        else:
            return LookupError

    def is_dead(self, lst):
        if self.hp <= 0:
            print(indent, bcolors.BOLD + bcolors.FAIL + self.name +
                  " has died in battle!" + "\n" + bcolors.ENDC)
            lst.remove(self)
            return True
        else:
            return False


class Enemy(Person):
    def __init__(self, name, hp, mp, atk, df, magic, items, behavioral_model):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ("Attack", "Magic", "Items")
        self.behavior = behavioral_model


    def choose_action(self, players, enemies, utility):
        # collect data for the decision

        own_health = (self.hp / self.maxhp) * 100

        print(own_health)

        # plug data into algorithm

        if own_health < 35:
            # if health is low and enemy has access to healing magic, heal himself
            pass
            #print("Low health alert:", self.name)

        else:
            # call the method for the chosen action
            target = self.choose_target(players)


    def choose_target(self, arr):
        heroes = []
        heroes_max_hp_sum = 0
        heroes_current_hp_sum = 0
        heroes_atkh_sum = 0

        for hero in arr:
            #heroes.append((hero.name, hero.get_max_hp(), hero.get_hp(), hero.atkh - random.randrange(0, 15)))
            heroes_max_hp_sum += hero.get_max_hp()
            heroes_current_hp_sum += hero.get_hp()
            heroes_atkh_sum += hero.atkh

        for hero in arr:
            hero_atkh_to_team_atkh = (hero.atkh - random.randrange(0, 15)) / heroes_atkh_sum * 100
            hero_hp_to_team_hp = hero.get_hp() / heroes_current_hp_sum * 100
            hero_hp_level = hero.get_hp() / hero.get_max_hp() * 100
            hero_hurt = True if hero_hp_level < 100 else False
            hero_range_ceiling = 100 / len(arr)

            #heroes.append((hero.name, hero_hp_to_team_hp, hero_atkh_to_team_atkh, hero_hp_level, hero_hurt))

            heroes.append({"name": hero.name,
                           "hp_to_team_hp": hero_hp_to_team_hp,
                           "atkh_to_team_atkh": hero_atkh_to_team_atkh,
                           "hp_level": hero_hp_level,
                           "hurt": hero_hurt,
                           "range_ceiling": hero_range_ceiling
                           })

        # sorted target lists

        # lowest hp to team hp ratio first
        weakest_target = sorted(heroes, key=lambda k: k["hp_to_team_hp"], reverse=False)

        # lowest hp to own max hp first
        most_damaged_target = sorted(heroes, key=lambda l: l["hp_level"], reverse=False)

        # highest atkh to team atkh
        most_dangerous_target = sorted(heroes, key=lambda x: x["atkh_to_team_atkh"], reverse=True)

        # debug prints
        #print("Weakest target is:", weakest_target, "\n")
        #print("Most damaged target is:", most_damaged_target, "\n")
        #print("Most dangerous target is:", most_dangerous_target, "\n")


        for hero in heroes:
            """ behavioral variables sets - these multipliers modify the weight of different factors depending on the 
            Enemies behavioral characteristics
            The multipliers are in sequence: weakest_target var, most_damaged_target var, most_dangerous_target var
            """
            coward = [2, 2, 1]


            hrc = hero["range_ceiling"]
            #TODO: Break up this calculation into chunks and deduct the divided number of the result from other's ceilings
            hrc = hrc \
                  + hrc / (weakest_target.index(hero) + 1) / 1/ coward[0] \
                  + hrc / (most_damaged_target.index(hero) + 1) / 1/ coward[1] \
                  + hrc / (most_dangerous_target.index(hero) + 1) / 1 / coward[2]
            print(hero["name"], "hrc value is:", hrc)
            # use the index value in weakest_target and hardest_hitter to calculate the range for randrange
            #range_weak = 100 - (100 / (weakest_target.index(hero) + 1))
            #range_hit = 100 - (100 / (hardest_hitter.index(hero) + 1))

            #whatever we add to the output for a given hero should be divided by the number of the compliment and
            #subtrackted from the complimentary team members

        #print(weakest_target, "\n", hardest_hitter)

        #TODO:find random target
        #TODO:Challenge: make the variables in the target calculation codependent and limited to the 0-100 range
        #TODO:Challenge: make the algo work with a team of whatever size

        # pick target

        # pick attack or magic, if enemy has black magic

        # if magic, pick attack spell

