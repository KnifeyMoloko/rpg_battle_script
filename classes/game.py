import random
from .magic import Spell

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
        pass

    def end_turn(self, player, enemy):
        print("=======================================")
        print("\nPlayer HP is: " + bcolors.OKGREEN + str(player.get_hp()) +
              "\\" + str(player.get_max_hp()) + bcolors.ENDC)

        print("\nPlayer MP is: " + bcolors.OKBLUE + str(player.get_mp()) +
              "\\" + str(player.get_max_mp()) + bcolors.ENDC)

        print("\nEnemy HP is: " + bcolors.FAIL + str(enemy.get_hp()) +
              "\\" + str(enemy.get_max_hp()) + bcolors.ENDC)

        print("\nEnemy MP is: " + bcolors.OKBLUE + str(enemy.get_mp()) +
              "\\" + str(enemy.get_max_mp()) + bcolors.ENDC + "\n")


class Person:
    def __init__(self, hp, mp, atk, df, magic, items):
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

    def choose_action(self):
        print(bcolors.OKGREEN + bcolors.BOLD + "Actions : " + bcolors.ENDC)

        i = 1

        for action in self.actions:
            print(str(i) + " : " + action)
            i += 1

    def choose_magic(self):
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "Magic : " + bcolors.ENDC)

        num = 1

        for i in self.magic:
            print(indent, str(num) + ": " + i.name, "(" + "cost: " + str(
                i.cost) + ")")
            num = num + 1

    def choose_item(self):
        num = 1

        print("\n" + bcolors.OKGREEN + "ITEMS:" + "\n" + bcolors.ENDC)

        for i in self.items:
            print(indent, str(num),  i.name, ": " + i.description)
            num = num + 1

