#!/usr/bin/python
# -*- coding: utf-8 -*-
# Habitants measure time in waves, not years or days:

wave = 0


def get_time():
    global wave
    return wave


def inc_time():
    global wave
    wave += 1

# Highest value of any stat parameters which has been in this run of game.
maxValueOfParameters = 1

listHabitant = []
listEnemy = []
