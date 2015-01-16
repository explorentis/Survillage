#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint

'''
putDice
Description:
"Throw dice" and check in which interval did he go
Parameter:
(int) goodInterval - width of "good interval"
(int) badInterval - width of "bad interval"
Return values:
Returns True if dice drop at goodInterval and False if else
'''
def putDice(goodInterval, badInterval):
	return randint(0, goodInterval + badInterval) < goodInterval

'''
selectPerson
Description:
Use parameter @stat@ from Stats as weight and rely on it select random person from list @listPersons@
Parameters:
(string) stat - name of parameter of person (from Stats) which will be used as weight (statistical expectation)
(list of class Habitant instances) listPerson - list of person where from select random person
Return values:
Returns person (pointer to it)
'''
def selectPerson(stat, listPersons):
	weightSum = 0
	for i in listPersons:
		weightSum += i.Stats[stat]
	score = randint(0, weightSum)
	for i in listPersons:
		if score > i.Stats[stat]:
			score -= i.Stats[stat]
		else:
			return i

def choiceWithWeight(elements):
	score = randint(1, sum(elements) - 1)
	counter = 0
	while score > elements[counter]:
		score -= elements[counter]
		counter += 1
	return counter
