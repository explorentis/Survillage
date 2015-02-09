#!/usr/bin/python
# -*- coding: utf-8 -*-
from modules.translate import t
from modules.global_vars import listHabitant, listEnemy, get_time, inc_time
from modules.habitant import Habitant

listHabitant.append(Habitant({}))
listHabitant[0].IsHabitant = True

while len(listHabitant) != 0:
    print
    print(t["wave.label.game"] % ("=" * 10, get_time(), "=" * 10))
    print
    # Happy new wave!! Yo-ho-ho!!
    for habitant in listHabitant:
        enemy = Habitant({})
        listEnemy.append(enemy)
        habitant.Target = enemy
        enemy.Target = habitant
    # fight
    fightTime = 0
    while len(listHabitant) != 0 and len(listEnemy) != 0:
        fightTime += 10
        print "+" * 10, t["habitants.label.game"], "+" * 10
        for habitant in listHabitant:
            habitant.print_all()
        print "+" * 10, t["enemies.label.game"], "+" * 10
        for enemy in listEnemy:
            enemy.print_all()
        print '=' * 5, t['habitants_turn.info.game'], '=' * 5
        for habitant in listHabitant:
            habitant.hitting()
        print '=' * 7, t['enemies_turn.info.game'], '=' * 7
        for enemy in listEnemy:
            enemy.hitting()
        if len(listHabitant) == 0:
            print t['game_over.info.game']
        elif len(listEnemy) == 0:
            print t['all_enemy_die.info.game']
            print(t['battle_duration.info.game'] % fightTime)
            raw_input(t['end_battle.need_action.game'])
        else:
            raw_input(t['end_turn_of_battle.need_action.game'])
    # make love not war:
    newHabitant = []
    for habitant in listHabitant:
        habitant.HP = habitant.Stats['Endurance']
        newHabitant.append(Habitant({'ancestor': habitant}))
    listHabitant += newHabitant
    inc_time()
    if len(listHabitant) != 0:
        raw_input(t['end_wave.need_action.game'])
