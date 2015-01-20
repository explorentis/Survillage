#!/usr/bin/python
# -*- coding: utf-8 -*-
from modules.habitant 		import Habitant
from modules.global_vars 	import listHabitant, listEnemy, wave

listHabitant.append(Habitant())
listHabitant[0].IsHabitant = True

while len(listHabitant) != 0:
	print "=" * 10, "It was", wave, "wave from foundation first village", "=" * 10
	# Happy new wave!! Yo-ho-ho!!
	for habitant in listHabitant:
		enemy = Habitant()
		listEnemy.append(enemy)
		habitant.Target = enemy
		enemy.Target = habitant
	# fight
	while len(listHabitant) != 0 and len(listEnemy) != 0:
		print "+" * 10, "Habitants", "+" * 10
		for habitant in listHabitant:
			habitant.printAllNotHeroes()
		print "-" * 10, "Enemies", "-" * 10
		for enemy in listEnemy:
			enemy.printAllNotHeroes()

		for habitant in listHabitant:
			habitant.hitting()
		for enemy in listEnemy:
			enemy.hitting()
		if len(listHabitant) == 0:
			print "All habitants was die. Game over"
		else:
			raw_input('Press any key to next turn of battle')
	# make love not war:
	newHabitant = []
	for habitant in  listHabitant:
		habitant.HP = habitant.Stats['Endurance']
		newHabitant.append(Habitant(habitant))
	listHabitant += newHabitant
	wave += 1
	raw_input('Press any key to next wave')
