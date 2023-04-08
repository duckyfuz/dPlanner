import sys
import csv
import random
import os
from io import StringIO

from dPlanner import *

# The LOWER the value of MAXDIFF, the more likely it is for a loop to occur (but it ensures a fairer outcome).
MAXDIFF = 0.5


def loadData(filename):
    """
    Takes filename as input, returns people[] and dict{}
    people[]: List of names (randomised)
    dict{}: Dictionary that links names to another dictionary with keys "unavail", "points" and 'extras'
    """
    
    # Open filename, skip headers line
    f = open(filename)
    reader = csv.reader(f)
    header = next(reader)

    # Initiate people[] and dict{}
    people = []
    dict = {}

    # Iterate through reader
    for row in reader:

        # Add name to people[]
        people.append(row[0])

        # Convert unavail dates to list of integers (Empty list if there are no unavail dates)
        if row[3] == 'NULL':
            unavailInt = []
            print(f"{row[0]} has no unavailable dates.")
        else:

            # Split row[3] into list values and convert the str values into int values
            unavail = list(row[3].split("/"))
            unavailInt = []
            for str in unavail:
                unavailInt.append(int(str))
        
        # Add clean values into dict{}
        dict[row[0]] = {"unavail": unavailInt, "points": int(row[1]), "extras": int(row[2])}

    # Shuffle people[] to ensure fairness
    random.shuffle(people)

    # Close file
    f.close()

    return people, dict

    
def fill(cal, people):
    """
    Takes cal and people as input, fill up cal with random people, ensuring that nobody is schedued for 2 consecuties duties.
    DOES NOT TAKE INTO ACCOUNT UNAVAIL DATES!!!
    """

    # Initiate prev with unimportant value
    prev = 0

    # Iterate over every single day of the month
    for x in range(len(cal.cal)):

        # For the first day, no need to take consecutive duties into account
        if x == 0:
            possibleRange = list(range(0,len(people)))
            prev = random.choice(possibleRange)
            cal.update(x+1,people[prev])
        
        # Randomly choose from all people, minus the one who is schedued for the previous day
        possibleRange = list(range(0,len(people)))
        possibleRange.remove(prev)
        prev = random.choice(possibleRange)
        cal.update(x+1,people[prev])


def checkConsis(cal, dict, people):
    """
    Replace people schedued for duty on unavail days with a random person. (Calls on replace() function)
    """

    # Iterate over everybody in dict
    for pax in dict:

        # Iterate over all unavail dates
        for date in dict[pax]['unavail']:

            # If he/she is schedued for an unavail date, call replace() to swap randomly
            if pax == cal.list()[date-1][2]:
                replace(pax, date, people, dict, cal)
    

def replace(pax, date, people, dict, cal):
    """
    Replace the specified person with somebody else who is NOT unavail on the specified date
    """

    # Shuffle people without the specified person, then add the specified person to the back of the list
    people.remove(pax)
    random.shuffle(people)
    people.append(pax)
    
    # Iterate over the random order
    for pers in people:
        
        # If the sub is avail on the date, swap the duty personnel, then break
        # Else, continue iterating over the random order of people.
        if date not in dict[pers]['unavail']:
            cal.list()[date-1][2] = pers
            break

        # If nobody is able to do duty on the date, sad lor :(
        elif pax == pers:
            print(f"Error: There is nobody free on {date}.")
            sys.exit()


def updateD(dict, cal):
    """
    Calculate the total points after doing the schedued duties.
    """

    # Iterate over each day, sum up the point for the schedued person
    for day in cal.list():
        dict[day[2]]['points'] += day[1]


def calcPoints(dict):
    """
    Based on the point values in dict, calcPoints creates a new dictionary sorted by points (ascending)
    """

    # Inititate points{}
    points = {}

    # Iterate over each person, add their names and points to points{}
    for pers in dict:
        points[pers] = float(dict[pers]['points'])
    
    # Sort points (ascending)
    points = sorted(points.items(), key=lambda item: item[1])

    return points


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


def main():

    # Check proper format
    if len(sys.argv) not in [4, 5]:
        sys.exit("Usage: python generate.py year month [input].csv [output].")

    # Parse command-line arguments
    yy,mm = int(sys.argv[1]),int(sys.argv[2])
    output = sys.argv[4] if len(sys.argv) == 5 else None

    # Load people, dict from specified file
    people, dict = loadData(sys.argv[3])

    # Create calendarPers class based on specified year and month
    calendar = calendarPers(yy,mm)

    # Fill calendarPers class with random people
    fill(calendar, people)

    # Ensure that nobody is schedued on a day that they are unavail
    checkConsis(calendar, dict, people)
    
    # Update the points in dict to reflect the schedued duties, then create points{}, a dictionary sorted by points (ascending)
    updateD(dict, calendar)
    points = calcPoints(dict)

    # While the maximum diference in points exceeds MAXDIFF, swap duties with the function recalibrate()
    while points[-1][1] - points[0][1] > MAXDIFF:
        
        # Person with the most points gives a random duty to the person with the least points
        recalibrate(calendar, points, dict)

        # Update points to reflect changes
        points = calcPoints(dict)
        
    print(calendar)
    print(points)


if __name__ == "__main__":
    main()