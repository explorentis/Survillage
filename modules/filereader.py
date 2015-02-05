#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir
from locale import getpreferredencoding

def readFile(filename):
    with open(filename) as openedFile:
        return openedFile.read()[:-1].split('\n')


# main menu
count = 1
print "Select profile to play:"
for directory in listdir('strings'):
    codePage = readFile('strings/' + directory + '/coding.txt')[0]
    print getpreferredencoding()
    print
    print str(count) + '.', directory, '\n',
    if (getpreferredencoding() == codePage) or (codePage == "ISO_8859-1"):
        print '\n'.join(readFile('strings/' + directory + '/description.txt'))
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
