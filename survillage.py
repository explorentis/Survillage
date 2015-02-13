#!/usr/bin/python
# -*- coding: utf-8 -*-
from modules.translate import t
from modules.scenario_parse import read_scenario
from modules.global_vars import listHabitant, listEnemy, get_time, inc_time, maxValueOfParameters
from modules.habitant import Habitant
from modules.village import Village
from random import choice

initScenario = read_scenario()
if initScenario is not None:
    if 'count' in initScenario:
        count = initScenario['count']
        village = Village(count, initScenario)
    else:
        village = Village(1, initScenario)
else:
    village = Village(1, {})

while village.size() != 0:
    print
    print(t["wave.label.game"] % ("=" * 10, get_time(), "=" * 10))
    print
    # Happy new wave!! Yo-ho-ho!!
    foes = Village(village.size(), {})
    village.attack(foes)
    # fight
    fightTime = 0
    while foes.size() != 0 and village.size() != 0:
        fightTime += 10
        print "+" * 10, t["habitants.label.game"], "+" * 10
        for habitant in village.Habitants:
            habitant.print_all()
        print "+" * 10, t["enemies.label.game"], "+" * 10
        for enemy in foes.Habitants:
            enemy.print_all()
        print '=' * 5, t['habitants_turn.info.game'], '=' * 5
        for habitant in village.Habitants:
            habitant.hitting()
        print '=' * 7, t['enemies_turn.info.game'], '=' * 7
        for enemy in foes.Habitants:
            enemy.hitting()
        if village.size() == 0:
            print t['game_over.info.game']
        elif foes.size() == 0:
            print t['all_enemy_die.info.game']
            print(t['battle_duration.info.game'] % fightTime)
            raw_input(t['end_battle.need_action.game'])
        else:
            raw_input(t['end_turn_of_battle.need_action.game'])
    # make love not war:
    newHabitant = []
    for habitant in village.Habitants:
        habitant.HP = habitant.Stats['Endurance']
        newHabitant.append(Habitant({'ancestor': habitant}, village))
    village.Habitants += newHabitant
    inc_time()
    if village.size() != 0:
        raw_input(t['end_wave.need_action.game'])
