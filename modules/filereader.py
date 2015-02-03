#!/usr/bin/python
# -*- coding: utf-8 -*-

def readFile(filename):
    with open(filename) as openedFile:
        return openedFile.read()[:-1].split()

#######for import#######
# list of names for persons
namesList = readFile('strings/names.txt')
# ending for partonymic
ending = readFile('strings/ending.txt')[0]
# end for last name
heroEnding = readFile('strings/heroending.txt')[0]
####for translate:####
codePage = readFile('strings/coding.txt')[0]
