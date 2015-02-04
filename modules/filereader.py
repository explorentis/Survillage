#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir

def readFile(filename):
    with open(filename) as openedFile:
        return openedFile.read()[:-1].split('\n')


# main menu
count = 1
print "Select profile to play:"
for directory in listdir('strings'):
    print
    print str(count) + '.', directory, '\n', '\n'.join(readFile('strings/' + directory + '/description.txt'))
    count += 1
profilePath = 'strings/' + listdir('strings')[int(raw_input("I'm select profile number:")) - 1]
#.

#######for import#######
alphabet = readFile(profilePath + '/alphabet.txt')
# list of names for persons
namesList = readFile(profilePath + '/names.txt')
# ending for partonymic
ending = readFile(profilePath + '/ending.txt')[0]
# end for last name
heroEnding = readFile(profilePath + '/heroending.txt')[0]
####for translate:####
codePage = readFile(profilePath + '/coding.txt')[0]
translation = readFile(profilePath + '/translate.txt')
