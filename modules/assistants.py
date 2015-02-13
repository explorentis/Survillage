#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint, choice
from filereader import codePage, alphabet
from global_vars import listHabitant, listEnemy

if codePage == "UTF-8":
    charlen = 2
else:
    charlen = 1


# for eventId look at mutate function in Habitant class
def mutate_string(string, event_id):
    new_char = choice(alphabet)
    if event_id == 0:
        return string
    if event_id == 1:
        num_char = charlen * randint(0, len(string.decode('utf-8')) - 1)
        return string[:num_char] + string[num_char + charlen:]
    elif event_id == 2:
        num_char = charlen * randint(0, len(string.decode('utf-8')))
        return string[:num_char] + new_char + string[num_char:]
    elif event_id == 3:
        num_char = charlen * randint(0, len(string.decode('utf-8')) - 1)
        return string[:num_char] + new_char + string[num_char + charlen:]


def remove_habitant(hero, home):
    if hero.IsDead == False:
        return
    for habitant in home.Habitants:
        for heroes in habitant.Heroes:
            if heroes == hero:
                return
    for habitant in home.Habitants:
        if hero == habitant:
            home.Habitants.remove(hero)

def getThatWhoHasAliveEnemy(listAlly):
    result = []
    for habitant in listAlly:
        if habitant.Target.IsDead == False:
            result.append(habitant)
    return result


