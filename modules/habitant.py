#!/usr/bin/python
# -*- coding: utf-8 -*-
from translate import t
from random import choice, randint
from global_vars import maxValueOfParameters, listEnemy, listHabitant, get_time
from filereader import names_list, ending, heroEnding
from dice import putDice, selectPerson, choiceWithWeight
from assistants import mutate_string, remove_habitant, getThatWhoHasAliveEnemy
from math import sqrt


# initParam: ancestor, maxValue
class Habitant():
    def __init__(self, initParam):
        global maxValueOfParameters
        if not 'maxValue' in initParam:
            initParam.update({'maxValue': maxValueOfParameters})
        if not 'ancestor' in initParam:
            self.Description = {
                'LastName': choice(names_list).capitalize() + heroEnding,
                'Patronymic': choice(names_list).capitalize() + ending,
                'Name': choice(names_list).capitalize()}
            self.Stats = {'Strenght': randint(1, initParam['maxValue']),
                          'Dexterity': randint(1, initParam['maxValue']),
                          'Endurance': randint(1, initParam['maxValue']),
                          'Accuracy': randint(1, initParam['maxValue']),
                          'Valor': randint(1, initParam['maxValue']),
                          'Caution': randint(1, initParam['maxValue'])}
            for stat in self.Stats:
                if self.Stats[stat] > maxValueOfParameters:
                    maxValueOfParameters = self.Stats[stat]
            self.Heroes = {'Strenght': self,
                           'Dexterity': self,
                           'Endurance': self,
                           'Accuracy': self,
                           'Valor': self,
                           'Caution': self}
            self.IsHabitant = False
        else:
            self.Description = {
                'LastName': self.get_heroname(initParam['ancestor'].Heroes) + heroEnding,
                'Patronymic': initParam['ancestor'].Description['Name'] + ending,
                'Name': choice(names_list).capitalize()}
            self.Stats = {'Strenght': initParam['ancestor'].Stats['Strenght'],
                          'Dexterity': initParam['ancestor'].Stats['Dexterity'],
                          'Endurance': initParam['ancestor'].Stats['Endurance'],
                          'Accuracy': initParam['ancestor'].Stats['Accuracy'],
                          'Valor': initParam['ancestor'].Stats['Valor'],
                          'Caution': initParam['ancestor'].Stats['Caution']}
            self.Heroes = {'Strenght': initParam['ancestor'].Heroes['Strenght'],
                           'Dexterity': initParam['ancestor'].Heroes['Dexterity'],
                           'Endurance': initParam['ancestor'].Heroes['Endurance'],
                           'Accuracy': initParam['ancestor'].Heroes['Accuracy'],
                           'Valor': initParam['ancestor'].Heroes['Valor'],
                           'Caution': initParam['ancestor'].Heroes['Caution']}
            self.IsHabitant = True

        self.IsDead = False
        self.HP = self.Stats['Endurance']
        self.Target = None
        # wave of birth (see comment to wave in global_vars):
        self.WoB = get_time()
        if 'ancestor' in initParam:
            self.mutate()
            print t["new_habitant.info.village"], self.print_name(), self.print_stats()

    def get_heroname(self, heroes):
        max_value = 0
        hero_name = ''
        for statName in heroes:
            # check only parameter "strength" at strong hero, parameter
            # "dexterity" at dexterous hero etc...
            if heroes[statName].Stats[statName] > max_value:
                max_value = heroes[statName].Stats[statName]
                hero_name = heroes[statName].Description['Name']
        return hero_name

    def print_name(self):
        return self.Description['Name'] + ' ' + self.Description['Patronymic'] + ' ' + self.Description['LastName']

    def print_stats(self):
        return 'Str', self.Stats['Strenght'], 'Dex', self.Stats['Dexterity'], \
            'End', self.Stats['Endurance'], 'Acc', self.Stats['Accuracy'], \
            'Val', self.Stats['Valor'], 'Cau', self.Stats['Caution']

    def print_all(self):  # пока не все параметры
        print self.print_name()
        print 'Str', self.Stats['Strenght'], 'Dex', self.Stats['Dexterity'], \
            'End', self.Stats['Endurance'], 'Acc', self.Stats['Accuracy'], \
            'Val', self.Stats['Valor'], 'Cau', self.Stats['Caution']
        print 'HP', self.HP
        print t['wob.parameter.habitant'], self.WoB
        print t['target.parameter.habitant'], self.Target.print_name()
        print '-' * 20

    def go_to_help(self):
        if self.IsHabitant:
            good_list = listHabitant
            bad_list = listEnemy
        else:
            good_list = listEnemy
            bad_list = listHabitant

        if len(bad_list) == 0:
            print self.print_name() + t['waiting_end_battle.action.habitant']
            return False

        persons_in_battle = getThatWhoHasAliveEnemy(good_list)
        if len(persons_in_battle) < 2:
            self.Target = choice(bad_list)
            return True

        self.Target = selectPerson('Valor', persons_in_battle, self).Target
        return True

    def die(self):
        print self.Target.print_name(), t['kill.action.habitant'], self.print_name()
        self.IsDead = True
        remove_habitant(self)

    def hitting(self):
        if self.IsDead:
            print self.print_name() + t['dead.action.habitant']
            return
        self.Target.Target = self
        if self.Target.IsDead:
            print self.print_name(), t['look_at_body.action.habitant'], self.Target.print_name()
            if putDice(self.Stats['Valor'], self.Stats['Caution']):
                if self.go_to_help():
                    print self.print_name(), t['new_target.action.habitant'], \
                        self.Target.print_name()
            return
        if putDice(self.Stats['Accuracy'], self.Target.Stats['Dexterity']):
            self.Target.HP -= self.Stats['Strenght']
            print self.print_name(), t['hurts.action.habitant'], self.Target.print_name()
            if self.Target.HP < 1:
                self.Target.die()
                if putDice(self.Stats['Valor'], self.Stats['Caution']):
                    if self.go_to_help():
                        print self.print_name(), t['new_target.action.habitant'], self.Target.print_name()
        else:
            print self.print_name(), t['miss.action.habitant'], self.Target.print_name()

    def mutate(self):
        global ending
        global heroEnding
        global maxValueOfParameters
        # 0 - nothing, 1 - name, 2 - ending, 3 - heroEnding,
        # 4 - from stats, 5 - from Heroes
        mutation_type = choiceWithWeight([0, 1, 1, 1, 8, 2])
        # 0 - nothing, 1 - delete, 2 - add, 3 - change
        mutation_event = choiceWithWeight([1, 2, 2, 8])
        if mutation_type == 1:  # namelist mutation
            name_id = randint(0, len(names_list))
            names_list[name_id] = mutate_string(names_list[name_id], mutation_event).capitalize()
        elif mutation_type == 2:  # mutation of ending
            ending = mutate_string(ending, mutation_event)
        elif mutation_type == 3:  # mutation of heroEnding
            heroEnding = mutate_string(heroEnding, mutation_event)
        elif mutation_type == 4:  # mutation of Stats
            stat = choice(self.Stats.keys())
            if mutation_event == 1 and self.Stats[stat] > 1:
                print t["decrease.mutation.habitant"], t[stat + '.parameter.habitant']
                self.Stats[stat] -= 1
            elif mutation_event == 2:
                print t["increase.mutation.habitant"], t[stat + '.parameter.habitant']
                self.Stats[stat] += 1
                self.replace_hero(stat)
            elif mutation_event == 3 and self.Stats[stat] > 1:
                print(t["overrepresentation.mutation.habitant"] % t[stat + '.parameter.habitant'])
                self.Stats[stat] -= 1
                # Dictionary here is relations between stats: what tuples 
                # is binded:
                self.Stats[
                    {'Strenght': 'Dexterity', 'Dexterity': 'Strenght', 'Endurance': 'Accuracy', 'Accuracy': 'Endurance',
                     'Valor': 'Caution', 'Caution': 'Valor'}[stat]] += 1
                # .
                self.replace_hero(stat)
            if self.Stats[stat] > maxValueOfParameters:
                maxValueOfParameters = self.Stats[stat]
        elif mutation_type == 5:  # mutation of memory about heroes
            hero = self.Heroes[choice(self.Stats.keys())]
            if not hero.IsDead:
                return
            else:
                # hero.Name, hero.Patronymic, hero.LastName, hero.Stats, hero.WoB
                mutation_hero_type = randint(1, 5)
                hero.print_all()
                if mutation_hero_type == 1:  # namelist mutation
                    hero.Description['Name'] = mutate_string(hero.Description['Name'], mutation_event).capitalize()
                elif mutation_hero_type == 2:  # mutation of ending
                    hero.Description['Patronymic'] = mutate_string(hero.Description['Patronymic'],
                                                                   mutation_event).capitalize()
                elif mutation_hero_type == 3:  # mutation of heroEnding
                    hero.Description['LastName'] = mutate_string(hero.Description['LastName'],
                                                                 mutation_event).capitalize()
                elif mutation_hero_type == 4:
                    stat = choice(hero.Stats.keys())
                    if mutation_event == 1 and hero.Stats[stat] > 1:
                        hero.Stats[stat] -= 1
                    elif mutation_event == 2:
                        hero.Stats[stat] += 1
                    elif mutation_event == 3 and hero.Stats[stat] > 1:
                        hero.Stats[stat] -= 1
                        # Dictionary here is relations between stats: what tuples is binded:
                        hero.Stats[{'Strenght': 'Dexterity', 'Dexterity': 'Strenght', 'Endurance': 'Accuracy',
                                    'Accuracy': 'Endurance', 'Valor': 'Caution', 'Caution': 'Valor'}[stat]] += 1
                        # .
                    if hero.Stats[stat] > maxValueOfParameters:
                        maxValueOfParameters = hero.Stats[stat]
                elif mutation_hero_type == 5:
                    hero.WoB += randint(-round(sqrt(get_time() - hero.WoB)), round(sqrt(get_time() - hero.WoB)))

    def replace_hero(self, stat):
        if self.Stats[stat] > self.Heroes[stat].Stats[stat]:
            remove_habitant(self.Heroes[stat])
            self.Heroes[stat] = self
