#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint, choice
from filereader import readFile

# for eventId look at mutate function in Habitant class
def mutateString(string, eventId):
	newLetter = choice(readFile('strings/alphabet.txt'))
	# TODO: Trooble with size of utf-8 coding characters: its have a 2 byte and i need in correcting address of symbol. But for other coding pages it is not need. I must have in mind it.
	if eventId == 0:
		return string
	if eventId == 1:
		numberSymbol = 2 * randint(0, len(string.decode('utf-8')) - 1)
		return string[:numberSymbol] + string[numberSymbol + 2:]
	elif eventId == 2:
		numberSymbol = 2 * randint(0, len(string.decode('utf-8')))
		return string[:numberSymbol] + newLetter + string[numberSymbol:]
	elif eventId == 3:
		numberSymbol = 2 * randint(0, len(string.decode('utf-8')) - 1)
		return string[:numberSymbol] + newLetter + string[numberSymbol + 2:]
