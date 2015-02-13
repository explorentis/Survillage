#!/usr/bin/python
__author__ = 'explorentis'
from random import choice
from filereader import names_list
from habitant import Habitant


class Village():
    def __init__(self, count, init_param):
        self.Name = choice(names_list)
        self.Habitants = [Habitant(init_param, self) for i in range(0, count)]
        self.FightWith = None

    def size(self):
        return len(self.Habitants)

    def remove_habitant(self, removed_habitant):
        if not removed_habitant.IsDead:
            return
        for habitant in self.Habitants:
            if removed_habitant in habitant.Heroes:
                return
        for habitant in self.Habitants:
            if removed_habitant == habitant:
                self.Habitants.remove(removed_habitant)

    def attack(self, enemy_village):
        self.FightWith = enemy_village
        enemy_village.FightWith = self
        for i in range(0, self.size()):
            self.Habitants[i].Target = enemy_village.Habitants[i]
            enemy_village.Habitants[i].Target = self.Habitants[i]