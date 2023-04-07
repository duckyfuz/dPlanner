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
            print(cal.list()[date-1])
            
            break
        elif pax == pers:
            print(f"Error: There is nobody free on {date}")
            sys.exit()

    print(f"DOO on {date}, {pax}, was replaced with {pers}")


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

    print(calendar)
    print(dict)


if __name__ == "__main__":
    main()