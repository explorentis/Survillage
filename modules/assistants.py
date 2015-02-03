#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint, choice
from filereader import readFile, codePage
from global_vars import listHabitant, listEnemy

if codePage == "utf-8":
    charlen = 2
else:
    charlen = 1

# for eventId look at mutate function in Habitant class
def mutateString(string, eventId):
    newLetter = choice(readFile('strings/alphabet.txt'))
    if eventId == 0:
        return string
    if eventId == 1:
        numberSymbol = charlen * randint(0, len(string.decode('utf-8')) - 1)
        return string[:numberSymbol] + string[numberSymbol + charlen:]
    elif eventId == 2:
        numberSymbol = charlen * randint(0, len(string.decode('utf-8')))
        return string[:numberSymbol] + newLetter + string[numberSymbol:]
    elif eventId == 3:
        numberSymbol = charlen * randint(0, len(string.decode('utf-8')) - 1)
        return string[:numberSymbol] + newLetter + string[numberSymbol + charlen:]


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
        if habitant.Target.IsDead != False:
            result.append(habitant)
    return result
