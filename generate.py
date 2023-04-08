import sys
import csv
import random
import os
from io import StringIO

from dPlanner import *

# The LOWER the value of MAXDIFF, the more likely it is for a loop to occur (but it ensures a fairer outcome).
MAXDIFF = 0.5

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
    print(f"Swapped {outgoing} with {incoming} on {date}")


def viable(date, unavailIncoming, incoming, cal):
    """Based on cal, check if incoming is doing duty on the day before/after date, and if incoming is unavail"""
    if date in unavailIncoming:
        return False
    
    if date < 1:
        if incoming == cal.list()[date][2]:
            return False
        
    elif date >= len(cal.list()): 
        if incoming == cal.list()[date-2][2]:
            return False
    
    else:
        if incoming == cal.list()[date-2][2]:
            return False
        if incoming == cal.list()[date][2]:
            return False

    return True
    

def recalibrate(cal, points, dict):
    outgoing = points[-1][0] # More points
    dutyOutgoing = duties(outgoing, cal)
    random.shuffle(dutyOutgoing)

    for i in points:
        incoming = i[0] # Less points
        unavailIncoming = dict[incoming]['unavail']

        for date in dutyOutgoing:
            if viable(date, unavailIncoming, incoming, cal) == True:
                updateP(date, outgoing, incoming, cal, dict)
                return
        
        if i == points[-1]:
            print('PLEASEEEEE DONT HAPPENNNNN :(((')
    

def loadData(filename):
    f = open(filename)
    reader = csv.reader(f)
    header = next(reader)
    dict = {}
    people = []
    for row in reader:
        people.append(row[0])

        unavail = list(row[3].split("/"))
        unavailInt = []
        for str in unavail:
            unavailInt.append(int(str))
        
        dict[row[0]] = {"unavail": unavailInt, "points": int(row[1])}

    random.shuffle(people)
    f.close()
    return people, dict


def main():

    # Check proper format
    if len(sys.argv) not in [4, 5]:
        sys.exit("Usage: python generate.py year month [input].csv [output].")

    # Parse command-line arguments
    yy,mm = int(sys.argv[1]),int(sys.argv[2])

    people, dict = loadData(sys.argv[3])

    output = sys.argv[4] if len(sys.argv) == 5 else None

    calendar = calendarPers(yy,mm)

    fill(calendar, people)

    checkConsis(calendar, dict, people)
    
    updateD(dict, calendar)

    points = calcPoints(dict)

    while points[-1][1] - points[0][1] > MAXDIFF:
        recalibrate(calendar, points, dict)
        points = calcPoints(dict)
        
    print(calendar)
    print(points)


if __name__ == "__main__":
    main()