import sys
import copy
import random
from io import StringIO

from dPlanner import *


def replace(pax, date, people, dict, cal):
    people.remove(pax)
    random.shuffle(people)
    people.append(pax)
    
    for pers in people:
        if date not in dict[pers]['unavail']:
            cal.list()[date-1][2] = pers
            break
        elif pax == pers:
            print(f"Error: There is nobody free on {date}")
            sys.exit()


def checkConsis(cal, dict, people):
    # Check that there is somebody on duty everyday (?)
    # Check that nobody does 2 consecutive duties
    # Check that nobody is doing duty on an unavail day
    for pax in dict:
        for date in dict[pax]['unavail']:
            if pax == cal.list()[date-1][2]:
                replace(pax, date, people, dict, cal)
    # Check that people with extras are doing them on a weekend/public holiday


def fill(cal, people):
    prev = 0
    for x in range(len(cal.cal)):
        if x == 0:
            possibleRange = list(range(0,len(people)))
            prev = random.choice(possibleRange)
            cal.update(x+1,people[prev])
        possibleRange = list(range(0,len(people)))
        possibleRange.remove(prev)
        prev = random.choice(possibleRange)
        cal.update(x+1,people[prev])


def updateD(dict, cal):
    for day in cal.list():
        dict[day[2]]['points'] += day[1]


def calcPoints(dict):
    """Based on the values in dict, calcPoints creates a new dictionary sorted by points (ascending)"""
    points = {}
    for pers in dict:
        points[pers] = float(dict[pers]['points'])
    
    points = sorted(points.items(), key=lambda item: item[1])
    return points


def duties(outgoing, cal):
    duties = []
    for day in cal.list():
        if day[2] == outgoing:
            duties.append(day[0])
    return duties


def updateP(date, outgoing, incoming, cal, dict):
    cal.list()[date-1][2] = incoming
    dict[outgoing]['points'] -= cal.list()[date-1][1]
    dict[incoming]['points'] += cal.list()[date-1][1]


def viable(date, unavailIncoming, incoming, cal):
    """Based on cal, check if incoming is doing duty on the day before/after date, and if incoming is unavail"""
    if date in unavailIncoming:
        return False
    
    try: 
        if incoming == cal[date-2][2]:
            return False
    except: 
        pass

    try: 
        if incoming == cal[date][2]:
            return False
    except: 
        pass

    return True
    

def recalibrate(cal, points, dict):
    
    outgoing = points[-1][0] # More points
    dutyOutgoing = duties(outgoing, cal)

    for i in points:
        incoming = i[0] # Less points
        unavailIncoming = dict[incoming]['unavail']

        for date in dutyOutgoing:
            if viable(date, unavailIncoming, incoming, cal) == True:
                updateP(date, outgoing, incoming, cal, dict)
                return
        
        if i == points[-1]:
            print('PLEASEEEEE DONT HAPPENNNNN :(((')
    

def main():

    # TEMPORARY -> SWITCH TO READING CSV FILE IN data/
    people = ["Josh", "Jay", "Jack", "Ken", "Korno", "Krel", "Abba", "Aby", "Andy"]
    random.shuffle(people)
    dict = {"Josh": {"unavail": [1,2], "points": 5},
            "Jay": {"unavail": [3,4], "points": 4},
            "Jack": {"unavail": [5,6], "points": 2},
            "Ken": {"unavail": [7], "points": 1},
            "Korno": {"unavail": [10,11,12,14], "points": 5},
            "Krel": {"unavail": [15,16], "points": 6},
            "Abba": {"unavail": [17], "points": 6},
            "Aby": {"unavail": [18,19,20,21,22], "points": 3}, 
            "Andy": {"unavail": [23,24,25,26,27,28], "points": 2}
    }


    # Check proper format
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py year month [output]")

    # Parse command-line arguments
    yy = int(sys.argv[1])
    mm = int(sys.argv[2])
    output = sys.argv[3] if len(sys.argv) == 4 else None

    calendar = calendarPers(yy,mm)

    fill(calendar, people)

    checkConsis(calendar, dict, people)
    
    updateD(dict, calendar)

    points = calcPoints(dict)

    while points[-1][1] - points[0][1] > 1.5:
        recalibrate(calendar, points, dict)
        points = calcPoints(dict)
        
    print(calendar)
    print(points)


if __name__ == "__main__":
    main()