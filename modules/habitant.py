#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import choice, randint
from global_vars import maxValueOfParameters, listEnemy, listHabitant, wave
from filereader import namesList, ending, heroEnding
from dice import putDice, selectPerson, choiceWithWeight

class Habitant():
	def __init__(self, ancestor = None):
		if ancestor is None:
			self.Description = { 	'Name' : choice(namesList), \
						'Patronymic' : choice(namesList) + ending, \
						'LastName' : '' }
			self.Stats = {	'Strenght'  : randint (1, maxValueOfParameters), \
					'Dexterity' : randint (1, maxValueOfParameters), \
					'Endurance' : randint (1, maxValueOfParameters), \
					'Accuracy'  : randint (1, maxValueOfParameters), \
					'Valor'     : randint (1, maxValueOfParameters), \
					'Cowardice' : randint (1, maxValueOfParameters)}
			self.Heroes = {	'Strenght'  : self, \
					'Dexterity' : self, \
					'Endurance' : self, \
					'Accuracy'  : self, \
					'Valor'     : self, \
					'Cowardice' : self}
		else:
			self.Description = { 	'Name' : choice(namesList), \
						'Patronymic' : ancestor.Description['Name'] + ending, \
						'LastName' : self.getHeroName(ancestor.Heroes) + heroEnding }
			self.Stats = { 	'Strenght'  : ancestor.Stats['Strenght'], \
					'Dexterity' : ancestor.Stats['Dexterity'], \
					'Endurance' : ancestor.Stats['Endurance'], \
					'Accuracy'  : ancestor.Stats['Accuracy'], \
					'Valor'     : ancestor.Stats['Valor'], \
					'Cowardice' : ancestor.Stats['Cowardice']}
			self.Heroes = {	'Strenght'  : ancestor.Heroes['Strenght'], \
					'Dexterity' : ancestor.Heroes['Dexterity'], \
					'Endurance' : ancestor.Heroes['Endurance'], \
					'Accuracy'  : ancestor.Heroes['Accuracy'], \
					'Valor'     : ancestor.Heroes['Valor'], \
					'Cowardice' : ancestor.Heroes['Cowardice']}

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
		print 'Str', self.Stats['Strenght'], 'Dex', self.Stats['Dexterity'], 'End', self.Stats['Endurance'], 'Acc', self.Stats['Accuracy'], 'Val', self.Stats['Valor'], 'Cow', self.Stats['Cowardice']
		print 'HP', self.HP
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
				# Check if want help to other:
				if putDice(self.Stats['Valor'], self.Stats['Cowardice']):
					# Select target to help him
					if self.IsHabitant == True:
						targetToHelp = selectPerson('Valor', listHabitant)
					else:
						targetToHelp = selectPerson('Valor', listEnemy)
					self.Target = targetToHelp.Target

	def mutate(self):
		mutationType = randint(1,5)
		if mutationType == 1:	# namelist mutation
			pass#########
		if mutationType == 2:	# mutation of ending
			pass#########
		if mutationType == 3:	# mutation of heroEnding
			pass##########
		if mutationType == 4:	# mutation of Stats
			stat = choice(self.Stats.keys())
			# 0 - nothing, 1 - delete, 2 - add, 3 - change
			mutationEvent = choiceWithWeight([1, 2, 2, 8])
			if mutationEvent == 1 and self.Stats[stat] > 1:
				self.Stats[stat] -= 1
			if mutationEvent == 2:
				self.Stats[stat] += 1
			if mutationEvent == 3 and self.Stats[stat] > 1:
					self.Stats[stat] -= 1
					# Dictionary here is relations between stats: what tuples is binded:
					self.Stats[{'Strenght' : 'Dexterity', 'Dexterity' : 'Strenght', 'Endurance' : 'Accuracy', 'Accuracy' : 'Endurance', 'Valor' : 'Cowardice', 'Cowardice' : 'Valor'}[stat]] += 1
					#.
		if mutationType == 5:	# mutation of memory about heroes
			hero = self.Heroes[choice(self.Stats.keys())]
			if hero.IsDead:
				return
			else:
				pass############

