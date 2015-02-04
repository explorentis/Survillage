#!/usr/bin/python
# -*- coding: utf-8 -*-
from filereader import translation

t = {}
for string in translation:
    splitted = string.split(' ', 1)
    t[splitted[0]] = ''.join(splitted[1:])
