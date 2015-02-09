__author__ = 'explorentis'

from filereader import initScenario

def read_scenario():
    initParam = {}
    for line in initScenario:
        line = line.split(' ')
        initParam.update({line[0]: int(line[1])})
    return initParam