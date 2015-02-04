#!/usr/bin/python
# -*- coding: utf-8 -*-
from translate import t
from random import choice, randint
from global_vars import maxValueOfParameters, listEnemy, listHabitant, getTime
from filereader import namesList, ending, heroEnding
from dice import putDice, selectPerson, choiceWithWeight
from assistants import mutateString, removeHabitant, getThatWhoHasAliveEnemy
from math import sqrt


class Habitant():
    def __init__(self, ancestor=None):
        if ancestor is None:
            self.Description = {'LastName': choice(namesList) + heroEnding,
                                'Patronymic': choice(namesList) + ending,
                                'Name': choice(namesList)}
            self.Stats = {'Strenght': randint(1, maxValueOfParameters),
                          'Dexterity': randint(1, maxValueOfParameters),
                          'Endurance': randint(1, maxValueOfParameters),
                          'Accuracy': randint(1, maxValueOfParameters),
                          'Valor': randint(1, maxValueOfParameters),
                          'Caution': randint(1, maxValueOfParameters)}
            self.Heroes = {'Strenght': self,
                           'Dexterity': self,
                           'Endurance': self,
                           'Accuracy': self,
                           'Valor': self,
                           'Caution': self}
            self.IsHabitant = False
        else:
            self.Description = {
                'LastName': self.getHeroName(ancestor.Heroes) + heroEnding,
                'Patronymic': ancestor.Description['Name'] + ending,
                'Name': choice(namesList)}
            self.Stats = {'Strenght': ancestor.Stats['Strenght'],
                          'Dexterity': ancestor.Stats['Dexterity'],
                          'Endurance': ancestor.Stats['Endurance'],
                          'Accuracy': ancestor.Stats['Accuracy'],
                          'Valor': ancestor.Stats['Valor'],
                          'Caution': ancestor.Stats['Caution']}
            self.Heroes = {'Strenght': ancestor.Heroes['Strenght'],
                           'Dexterity': ancestor.Heroes['Dexterity'],
                           'Endurance': ancestor.Heroes['Endurance'],
                           'Accuracy': ancestor.Heroes['Accuracy'],
                           'Valor': ancestor.Heroes['Valor'],
                           'Caution': ancestor.Heroes['Caution']}
            self.IsHabitant = True

        self.IsDead = False
        self.HP = self.Stats['Endurance']
        self.Target = None
        # wave of birth (see comment to wave in global_vars):
        self.WoB = getTime()
        if ancestor is not None:
            self.mutate()
            print t["new_habitant.info.village"], self.printName(), self.printStats()

    def getHeroName(self, heroes):
        maxValue = 0
        heroName = ''
        for statName in heroes:
            # check only parameter "strenght" at strong hero, parameter
            # "dextery" at dexterous hero etc...
            if heroes[statName].Stats[statName] > maxValue:
                maxValue = heroes[statName].Stats[statName]
                heroName = heroes[statName].Description['Name']
        return heroName

    def printName(self):
        return self.Description['Name'] + ' ' + self.Description['Patronymic'] + ' ' + self.Description['LastName']

    def printStats(self):
        return 'Str', self.Stats['Strenght'], 'Dex', self.Stats['Dexterity'], \
            'End', self.Stats['Endurance'], 'Acc', self.Stats['Accuracy'], \
            'Val', self.Stats['Valor'], 'Cau', self.Stats['Caution']

    def printAllNotHeroes(self):  # пока не все параметры (например, нет WoB)
        print self.printName()
        print 'Str', self.Stats['Strenght'], 'Dex', self.Stats['Dexterity'], \
            'End', self.Stats['Endurance'], 'Acc', self.Stats['Accuracy'], \
            'Val', self.Stats['Valor'], 'Cau', self.Stats['Caution']
        print 'HP', self.HP
        print t['wob.parameter.habitant'], self.WoB
        print t['target.parameter.habitant'], self.Target.printName()
        print '-' * 20

    def goToHelp(self):
        if self.IsHabitant:
            goodList = listHabitant
            badList = listEnemy
        else:
            goodList = listEnemy
            badList = listHabitant

        if len(badList) == 0:
            print self.printName() + t['waiting_end_battle.action.habitant']
            return False

        personsInBattle = getThatWhoHasAliveEnemy(goodList)
        if len(personsInBattle) < 2:
            self.Target = choice(badList)
            return True

        self.Target = selectPerson('Valor', personsInBattle, self).Target
        return True

    def die(self):
        print self.Target.printName(), t['kill.action.habitant'], self.printName()
        self.IsDead = True
        removeHabitant(self)

    def hitting(self):
        if self.IsDead == True:
            print self.printName() + t['dead.action.habitant']
            return
        self.Target.Target = self
        if self.Target.IsDead == True:
            print self.printName(), t['look_at_body.action.habitant'], self.Target.printName()
            if putDice(self.Stats['Valor'], self.Stats['Caution']):
                if self.goToHelp():
                    print self.printName(), t['new_target.action.habitant'], \
                        self.Target.printName()
            return
        if putDice(self.Stats['Accuracy'], self.Target.Stats['Dexterity']):
            self.Target.HP -= self.Stats['Strenght']
            print self.printName(), t['hurts.action.habitant'], self.Target.printName()
            if self.Target.HP < 1:
                self.Target.die()
                if putDice(self.Stats['Valor'], self.Stats['Caution']):
                    if self.goToHelp():
                        print self.printName(), t['new_target.action.habitant'], self.Target.printName()
        else:
            print self.printName(), t['miss.action.habitant'], self.Target.printName()

    def mutate(self):
        global ending
        global heroEnding
        global maxValueOfParameters
        # 0 - nothing, 1 - name, 2 - ending, 3 - heroEnding,
        # 4 - from stats, 5 - from Heroes
        mutationType = choiceWithWeight([0, 1, 1, 1, 8, 2])
        # 0 - nothing, 1 - delete, 2 - add, 3 - change
        mutationEvent = choiceWithWeight([1, 2, 2, 8])
        if mutationType == 1:  # namelist mutation
            nameId = randint(0, len(namesList))
            namesList[nameId] = mutateString(namesList[nameId], mutationEvent).capitalize()
        elif mutationType == 2:  # mutation of ending
            ending = mutateString(ending, mutationEvent)
        elif mutationType == 3:  # mutation of heroEnding
            heroEnding = mutateString(heroEnding, mutationEvent)
        elif mutationType == 4:  # mutation of Stats
            stat = choice(self.Stats.keys())
            if mutationEvent == 1 and self.Stats[stat] > 1:
                print t["decrease.mutation.habitant"], t[stat + '.parameter.habitant']
                self.Stats[stat] -= 1
            elif mutationEvent == 2:
                print t["increase.mutation.habitant"], t[stat + '.parameter.habitant']
                self.Stats[stat] += 1
                self.replaceHero(stat)
            elif mutationEvent == 3 and self.Stats[stat] > 1:
                print(t["overrepresentation.mutation.habitant"] % t[stat + '.parameter.habitant'])
                self.Stats[stat] -= 1
                # Dictionary here is relations between stats: what tuples 
                # is binded:
                self.Stats[
                    {'Strenght': 'Dexterity', 'Dexterity': 'Strenght', 'Endurance': 'Accuracy', 'Accuracy': 'Endurance',
                     'Valor': 'Caution', 'Caution': 'Valor'}[stat]] += 1
                # .
                self.replaceHero(stat)
            elif self.Stats[stat] > maxValueOfParameters:
                maxValueOfParameters = self.Stats[stat]
        elif mutationType == 5:  # mutation of memory about heroes
            hero = self.Heroes[choice(self.Stats.keys())]
            if hero.IsDead == False:
                return
            else:
                # hero.Name, hero.Patronymic, hero.LastName, hero.Stats, hero.WoB
                mutationHeroType = randint(1, 5)
                hero.printAllNotHeroes()
                if mutationHeroType == 1:  # namelist mutation
                    hero.Description['Name'] = mutateString(hero.Description['Name'], mutationEvent).capitalize()
                elif mutationHeroType == 2:  # mutation of ending
                    hero.Description['Patronymic'] = mutateString(hero.Description['Patronymic'],
                                                                  mutationEvent).capitalize()
                elif mutationHeroType == 3:  # mutation of heroEnding
                    hero.Description['LastName'] = mutateString(hero.Description['LastName'],
                                                                mutationEvent).capitalize()
                elif mutationHeroType == 4:
                    stat = choice(hero.Stats.keys())
                    if mutationEvent == 1 and hero.Stats[stat] > 1:
                        hero.Stats[stat] -= 1
                    elif mutationEvent == 2:
                        hero.Stats[stat] += 1
                    elif mutationEvent == 3 and hero.Stats[stat] > 1:
                        hero.Stats[stat] -= 1
                        # Dictionary here is relations between stats: what tuples is binded:
                        hero.Stats[{'Strenght': 'Dexterity', 'Dexterity': 'Strenght', 'Endurance': 'Accuracy',
                                    'Accuracy': 'Endurance', 'Valor': 'Caution', 'Caution': 'Valor'}[stat]] += 1
                        # .
                    if hero.Stats[stat] > maxValueOfParameters:
                        maxValueOfParameters = hero.Stats[stat]
                elif mutationHeroType == 5:
                    hero.WoB += randint(-round(sqrt(getTime() - hero.WoB)), round(sqrt(getTime() - hero.WoB)))

    def replaceHero(self, stat):
        if self.Stats[stat] > self.Heroes[stat].Stats[stat]:
            removeHabitant(self.Heroes[stat])
            self.Heroes[stat] = self
