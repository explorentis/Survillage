#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import choice, randint
from global_vars import maxValueOfParameters, listEnemy, listHabitant
from filereader import namesList, ending, heroEnding
from dice import putDice, selectPerson

maxValueOfParameters = 10
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

	def getHeroName(self, heroes):
		maxValue = 0
		heroName = ''
		for name_of_hero_and_stat in heroes:
			# check only parameter "strenght" at strong hero, parameter "dextery" at dexterous hero etc...
			if heroes[name_of_hero_and_stat].Stats[name_of_hero_and_stat] > maxValue:
				maxValue = heroes[name_of_hero_and_stat].Stats[name_of_hero_and_stat]
				heroName = heroes[name_of_hero_and_stat].Description['Name']
		return heroName

	def printAllNotHeroes(self):
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
						selectPerson('Valor', listHabitant)
					else:
						selectPerson('Valor', listEnemy)
					

