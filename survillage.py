#!/usr/bin/python
# -*- coding: utf-8 -*-
from modules.translate import t
from modules.global_vars import listHabitant, listEnemy, getTime, incTime
from modules.habitant import Habitant

listHabitant.append(Habitant())
listHabitant[0].IsHabitant = True

while len(listHabitant) != 0:
    print
    print "=" * 10, "It was",
    print getTime(), "wave from foundation village", "=" * 10
    print
    # Happy new wave!! Yo-ho-ho!!
    for habitant in listHabitant:
        enemy = Habitant()
        listEnemy.append(enemy)
        habitant.Target = enemy
        enemy.Target = habitant
    # fight
    fightTime = 0
    while len(listHabitant) != 0 and len(listEnemy) != 0:
        fightTime += 10
        print "+" * 10, "Habitants", "+" * 10
        for habitant in listHabitant:
            habitant.printAllNotHeroes()
        print "+" * 10, "Enemies", "+" * 10
        for enemy in listEnemy:
            enemy.printAllNotHeroes()
        print '=' * 5, 'Habitants strikes', '=' * 5
        for habitant in listHabitant:
            habitant.hitting()
        print '=' * 7, 'Enemy strikes', '=' * 7
        for enemy in listEnemy:
            enemy.hitting()
        if len(listHabitant) == 0:
            print "All habitants is die. Game over"
        elif len(listEnemy) == 0:
            print "All enemy is die"
            print "Fight duration " + str(fightTime) + " sec."
            raw_input("Battle end, press any key")
        else:
            raw_input('Press any key to next turn of battle')
    # make love not war:
    newHabitant = []
    for habitant in listHabitant:
        habitant.HP = habitant.Stats['Endurance']
        newHabitant.append(Habitant(habitant))
    listHabitant += newHabitant
    incTime()
#    raw_input('Press any key to next wave')
    raw_input(t['game.need_action.end_wave'])
