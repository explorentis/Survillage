#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint, choice
from filereader import readFile, codePage, alphabet
from global_vars import listHabitant, listEnemy
from translate import t

if codePage == "utf-8":
    charlen = 2
else:
    charlen = 1


# for eventId look at mutate function in Habitant class
def mutateString(string, eventId):
    newChar = choice(alphabet)
    if eventId == 0:
        return string
    if eventId == 1:
        numChar = charlen * randint(0, len(string.decode('utf-8')) - 1)
        return string[:numChar] + string[numChar + charlen:]
    elif eventId == 2:
        numChar = charlen * randint(0, len(string.decode('utf-8')))
        return string[:numChar] + newChar + string[numChar:]
    elif eventId == 3:
        numChar = charlen * randint(0, len(string.decode('utf-8')) - 1)
        return string[:numChar] + newChar + string[numChar + charlen:]


def removeHabitant(hero):
    if hero.IsDead == False:
        return
    for habitant in listHabitant:
        for heroes in habitant.Heroes:
            if heroes == hero:
                return
    for habitant in listHabitant:
        if hero == habitant:
            listHabitant.remove(hero)
    for habitant in listEnemy:
        if hero == habitant:
            listEnemy.remove(hero)


def getThatWhoHasAliveEnemy(listAlly):
    result = []
    for habitant in listAlly:
        if habitant.Target.IsDead == False:
            result.append(habitant)
    return result


