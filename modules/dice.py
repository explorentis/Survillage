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
Use parameter @stat@ from Stats as weight and rely on it select random person
from list @listPersons@
Parameters:
(string) stat - name of parameter of person (from Stats) which will be used
as weight (statistical expectation)
(list of class Habitant instances) listPerson - list of person where from
select random person
Return values:
Returns person (pointer to it)
'''


def selectPerson(stat, listAlly, itself):
    personsInBattle = []
    weightSum = 0
    for person in listAlly:
        if (person.Target.IsDead == False) and (person.IsDead == False) and (itself != person):
            weightSum += person.Stats[stat]
            personsInBattle.append(person)
    score = randint(0, weightSum)
    for person in personsInBattle:
        if score > person.Stats[stat]:
            score -= person.Stats[stat]
        else:
            return person


def choiceWithWeight(elements):
    score = randint(1, sum(elements) - 1)
    counter = 0
    while score > elements[counter]:
        score -= elements[counter]
        counter += 1
    return counter

'''
While random number catched by good_interval, increment result by 1
'''
def incremental_count(good_interval, bad_interval):
    result = 0
    while putDice(good_interval, bad_interval):
        result += 1
    return result
