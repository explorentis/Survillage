#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir
from locale import getpreferredencoding


def read_file(filename):
    try:
        with open(filename) as openedFile:
            return openedFile.read()[:-1].split('\n')
    except:
        print "FILE NOT FOUND:", filename


# main menu
count = 1
print "Select profile to play:"
for directory in listdir('strings'):
    codePage = read_file('strings/' + directory + '/coding.txt')[0]
    print
    print str(count) + '.', directory.replace('.', ' (', 1).replace('_', ' ') + ')\n',
    if (getpreferredencoding() == codePage) or (codePage == "ISO_8859-1"):
        print '\n'.join(read_file('strings/' + directory + '/description.txt'))
    else:
        print "WARNING: may be this profile is unsupportable."
    count += 1
while True:
    try:
        profilePath = 'strings/' + listdir('strings')[int(raw_input("I'm select profile number: ")) - 1]
    except ValueError:
        pass
    else:
        break
# .

# ======for import======
alphabet = read_file(profilePath + '/alphabet.txt')
# list of names for persons
names_list = read_file(profilePath + '/names.txt')
# ending for partonymic
ending = read_file(profilePath + '/ending.txt')[0]
# end for last name
heroEnding = read_file(profilePath + '/heroending.txt')[0]
# =====for translate=====
codePage = read_file(profilePath + '/coding.txt')[0]
translation = read_file(profilePath + '/translate.txt')

initScenario = read_file(profilePath + '/scenario.rc')