#!/usr/bin/python
# -*- coding: utf-8 -*-
from random		import choice, randint
from global_vars	import maxValueOfParameters, listEnemy, listHabitant, wave
from filereader 	import namesList, ending, heroEnding
from dice 		import putDice, selectPerson, choiceWithWeight
from assistants 	import mutateString, removeHabitant
from math		import sqrt

class Habitant():
	def __init__(self, ancestor = None):
		if ancestor is None:
			self.Description = { 	'Name' : choice(namesList), \
						'Patronymic' : choice(namesList) + ending, \
						'LastName' : choice(namesList) + heroEnding }
			self.Stats = {	'Strenght'  : randint (1, maxValueOfParameters), \
					'Dexterity' : randint (1, maxValueOfParameters), \
					'Endurance' : randint (1, maxValueOfParameters), \
					'Accuracy'  : randint (1, maxValueOfParameters), \
					'Valor'     : randint (1, maxValueOfParameters), \
					'Caution' : randint (1, maxValueOfParameters)}
			self.Heroes = {	'Strenght'  : self, \
					'Dexterity' : self, \
					'Endurance' : self, \
					'Accuracy'  : self, \
					'Valor'     : self, \
					'Caution' : self}
		else:
			self.Description = { 	'Name' : choice(namesList), \
						'Patronymic' : ancestor.Description['Name'] + ending, \
						'LastName' : self.getHeroName(ancestor.Heroes) + heroEnding }
			self.Stats = { 	'Strenght'  : ancestor.Stats['Strenght'], \
					'Dexterity' : ancestor.Stats['Dexterity'], \
					'Endurance' : ancestor.Stats['Endurance'], \
					'Accuracy'  : ancestor.Stats['Accuracy'], \
					'Valor'     : ancestor.Stats['Valor'], \
					'Caution' : ancestor.Stats['Caution']}
			self.Heroes = {	'Strenght'  : ancestor.Heroes['Strenght'], \
					'Dexterity' : ancestor.Heroes['Dexterity'], \
					'Endurance' : ancestor.Heroes['Endurance'], \
					'Accuracy'  : ancestor.Heroes['Accuracy'], \
					'Valor'     : ancestor.Heroes['Valor'], \
					'Caution' : ancestor.Heroes['Caution']}

		self.IsDead = False
		self.HP = self.Stats['Endurance']
		self.IsHabitant = False
		self.Target = None
		# wave of birth (see comment to wave in global_vars):
		self.WoB = wave
		self.mutate()

	def getHeroName(self, heroes):
		maxValue = 0
		heroName = ''
		for name_of_hero_and_stat in heroes:
			# check only parameter "strenght" at strong hero, parameter "dextery" at dexterous hero etc...
			if heroes[name_of_hero_and_stat].Stats[name_of_hero_and_stat] > maxValue:
				maxValue = heroes[name_of_hero_and_stat].Stats[name_of_hero_and_stat]
				heroName = heroes[name_of_hero_and_stat].Description['Name']
		return heroName

	def printAllNotHeroes(self): # пока не все параметры (например, нет WoB)
		print '-' * 20
		print self.Description['Name'], self.Description['Patronymic'], self.Description['LastName']
		print 'Str', self.Stats['Strenght'], 'Dex', self.Stats['Dexterity'], 'End', self.Stats['Endurance'], 'Acc', self.Stats['Accuracy'], 'Val', self.Stats['Valor'], 'Cau', self.Stats['Caution']
		print 'HP', self.HP
		print 'Wave of Birth', self.WoB
		if self.IsDead:
			print 'It is dead'
		else:
			print 'It is alive'
		if self.IsHabitant:
			print 'It is habitant'
		else:
			print 'It is enemy'
		print '-' * 20

	def hitting(self, target):
		if self.IsDead == True:
			return
		if putDice(self.Stats['Accuracy'], target.Stats['Dexterity']):
			target.HP -= self.Stats['Strenght']
			if target.HP < 1:
				target.IsDead = True
				removeHabitant(target)
				# Check if want help to other:
				if putDice(self.Stats['Valor'], self.Stats['Caution']):
					# Select target to help him
					if self.IsHabitant == True:
						targetToHelp = selectPerson('Valor', listHabitant)
					else:
						targetToHelp = selectPerson('Valor', listEnemy)
					self.Target = targetToHelp.Target

	def mutate(self):
		global ending
		global heroEnding
		# 0 - nothing, 1 - name, 2 - ending, 3 - heroEnding, 4 - from stats, 5 - from Heroes
		mutationType = choiceWithWeight([0, 1, 1, 1, 8, 2])
		# 0 - nothing, 1 - delete, 2 - add, 3 - change
		mutationEvent = choiceWithWeight([1, 2, 2, 8])
		if mutationType == 1:	# namelist mutation
			nameId = randint(0, len(namesList))
			namesList[nameId] = mutateString(namesList[nameId], mutationEvent).capitalize()
		if mutationType == 2:	# mutation of ending
			ending = mutateString(ending, mutationEvent)
		if mutationType == 3:	# mutation of heroEnding
			heroEnding = mutateString(heroEnding, mutationEvent)
		if mutationType == 4:	# mutation of Stats
			stat = choice(self.Stats.keys())
			if mutationEvent == 1 and self.Stats[stat] > 1:
				self.Stats[stat] -= 1
			if mutationEvent == 2:
				self.Stats[stat] += 1
				self.replaceHero(stat)
			if mutationEvent == 3 and self.Stats[stat] > 1:
				self.Stats[stat] -= 1
				# Dictionary here is relations between stats: what tuples is binded:
				self.Stats[{'Strenght' : 'Dexterity', 'Dexterity' : 'Strenght', 'Endurance' : 'Accuracy', 'Accuracy' : 'Endurance', 'Valor' : 'Caution', 'Caution' : 'Valor'}[stat]] += 1
				#.
				self.replaceHero(stat)
		if mutationType == 5:	# mutation of memory about heroes
			hero = self.Heroes[choice(self.Stats.keys())]
			if hero.IsDead == False:
				return
			else:
				# hero.Name, hero.Patronymic, hero.LastName, hero.Stats, hero.WoB
				mutationHeroType = randint(1,5)
				hero.printAllNotHeroes()
				if mutationHeroType == 1:	# namelist mutation
					hero.Description['Name'] = mutateString(hero.Description['Name'], mutationEvent).capitalize()
				if mutationHeroType == 2:	# mutation of ending
					hero.Description['Patronymic'] = mutateString(hero.Description['Patronymic'], mutationEvent).capitalize()
				if mutationHeroType == 3:	# mutation of heroEnding
					hero.Description['LastName'] = mutateString(hero.Description['LastName'], mutationEvent).capitalize()
				if mutationHeroType == 4:
					stat = choice(hero.Stats.keys())
					if mutationEvent == 1 and hero.Stats[stat] > 1:
						hero.Stats[stat] -= 1
					if mutationEvent == 2:
						hero.Stats[stat] += 1
					if mutationEvent == 3 and hero.Stats[stat] > 1:
						hero.Stats[stat] -= 1
					# Dictionary here is relations between stats: what tuples is binded:
						hero.Stats[{'Strenght' : 'Dexterity', 'Dexterity' : 'Strenght', 'Endurance' : 'Accuracy', 'Accuracy' : 'Endurance', 'Valor' : 'Caution', 'Caution' : 'Valor'}[stat]] += 1
					#.
				if mutationHeroType == 5:
					hero.WoB += randint(-round(sqrt(wave - hero.WoB)), round(sqrt(wave - hero.WoB)))

	def replaceHero(self, stat):
		if self.Stats[stat] > self.Heroes[stat].Stats[stat]:
			removeHabitant(self.Heroes[stat])
			self.Heroes[stat] = self

