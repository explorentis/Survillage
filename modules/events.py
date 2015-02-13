__author__ = 'explorentis'
from random import choice, randint
from village import Village
from dice import incremental_count
from global_vars import maxValueOfParameters
from translate import t

def attack_weak(village):
    army_count = 0
    print t['weak_enemy.attack.village']
    for habitant in village.Habitants:
        army_count += randint(0, village.size())
    if army_count == 0:
        army_count = 1
    return Village(army_count, {'modifyMaxValue': 1/float(village.size())})


def attack_equal(village):
    army_count = 0
    print t['equal_enemy.attack.village']
    for habitant in village.Habitants:
        # 3 and 2 because probability of True = 3/(3+2) = 60%, so chance for army_count = 0 is 40%, chance
        # for 2 is 60% * 60% = 36%. Its too close each to each.
        army_count += incremental_count(3, 2)
    if army_count == 0:
        army_count = 1
    return Village(army_count, {})

def attack_strong(village):
    print t['strong_enemy.attack.village']
    army_count = incremental_count(3, 2)
    if army_count == 0:
        army_count = 1
    return Village(army_count, {'modifyMaxValue': float(village.size())})


def peace_time():
    pass


def war_time(village):
    return choice([attack_weak, attack_equal, attack_strong])(village)
    #return attack_equal(village)


def next_event(village):
    # choice([peace_time, war_time])(village)
    return war_time(village)
