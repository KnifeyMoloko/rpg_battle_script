#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    def end_turn(self, players, enemies):
        print("=======================================")
        for p in players:
            print(indent + bcolors.BOLD + p.name + bcolors.ENDC + "\n")
            print(indent + bcolors.OKGREEN + "|_________________________|")
            print(indent + indent + indent + str(p.get_hp()) + "/"
                  + str(p.get_max_hp()) + bcolors.ENDC)
            print(indent + bcolors.OKBLUE + "|__________|")
            print(indent + indent + str(p.get_mp()) + "/" + str(p.get_max_mp(
            )) + bcolors.ENDC + "\n")

        for e in enemies:
            print(indent + bcolors.FAIL + e.name + bcolors.ENDC + "\n")
            print(indent + bcolors.OKGREEN + "|_________________________|")
            print(indent + indent + indent + str(e.get_hp()) + "/"
                  + str(e.get_max_hp()) + bcolors.ENDC)
            print(indent + bcolors.OKBLUE + "|__________|")
            print(indent + indent + str(e.get_mp()) + "/" + str(e.get_max_mp(
            )) + bcolors.ENDC + "\n")

    def blocky_view(self, person):
        """for c in range(1,int(0x10FF)):
            print(str(c), chr(c))"""
        block_char = chr(9960)
        hp = person.get_hp()
        mp = person.get_mp()
        max_hp = person.get_max_hp()
        max_mp = person.get_max_mp()
        hp_size = int(max_hp / 10)
        mp_size = int(max_mp / 10)
        current_hp = hp_size - int(hp /10)
        current_mp = mp_size - int(mp / 10)

    #TODO: Add colors and printed ints for hp and mp, work on formatting nicely
        if current_hp != 0:
            underscore = "_"
            underscore_size = hp_size - current_hp
            underscore_size_mp = mp_size - current_mp
            print("HP ", "|" + current_hp * block_char + underscore *
                  underscore_size + "|")
        else:
            print("HP ", "|" + hp_size * block_char + "|")

        if current_mp != 0:
            print("MP ", "|" + current_mp * block_char + underscore *
                  underscore_size_mp + "|")
        else:
            print("MP ", "|" + mp_size * block_char + "|")




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
            print(indent, str(num),  i.name, ": " + i.description + " (" +
                  str(i.quantity) + ")")
            num = num + 1

