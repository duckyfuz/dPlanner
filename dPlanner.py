import sys
import csv
import random
import os

from time import sleep
from io import StringIO

from classes import *

def loadData(filename):
    """
    Takes filename as input, returns people[] and dict{}
    people[]: List of names (randomised)
    dict{}: Dictionary that links names to another dictionary with keys "unavail", "points", 'extras' and 'leftovers'
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

        else:

            # Split row[3] into list values and convert the str values into int values
            unavail = list(row[3].split("/"))
            unavailInt = []
            for str in unavail:
                unavailInt.append(int(str))

        clear = 0
        if int(row[2]) > 0:
            clear = int(input(f"{row[0]} has {row[2]} extra(s). How many to clear this month? "))
        
        # Add clean values into dict{}
        dict[row[0]] = {"unavail": unavailInt, 
                        "points": int(row[1]), 
                        "extras": clear, 
                        "leftovers": int(row[2]) - clear}

    # Shuffle people[] to ensure fairness
    random.shuffle(people)

    # Close file
    f.close()

    return people, dict


def fill(cal, people, dict, untouchable):
    """
    Takes cal and people as input, fill up cal with random people, ensuring that nobody is schedued for 2 consecuties duties.
    DOES NOT TAKE INTO ACCOUNT UNAVAIL DATES!!!
    """

    # Create dict of people: extras
    extras = {}
    for person in dict:
        if dict[person]['extras'] == 0:
            continue
        extras[person] = dict[person]['extras']

    # Fill up extras
    for person in extras:
        for _ in range(extras[person]):
            for day in cal.cal:

                # Skip all dates that fall on a weekday
                if day[1] != 2 or day[2] != None:
                    continue

                if cal.viable(day[0], dict[person]['unavail'], person, untouchable):
                    day[2] = person
                    untouchable.append(day[0])
                    break

    # Fill up the rest of the days
    for day in cal.cal:
        random.shuffle(people)
        for incoming in people:
            if not cal.viable(day[0], dict[incoming]['unavail'], incoming, untouchable):
                continue
            day[2] = incoming

    return


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


def updateD(dict, cal, untouchable):
    """
    Calculate the total points after doing the schedued duties.
    """

    # Iterate over each day, sum up the point for the schedued person
    for day in cal.cal:
        if day[0] in untouchable:
            continue
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


def recalibrate(cal, points, dict, untouchable):
    """
    Selects the person with the most points, choose a random duty, gives it to the person with the least points. Choose another date if the person is unavail on the first date.
    """

    # Outgoing is the person with the most points
    outgoing = points[-1][0]

    # Call the function duties() to create a list of the duties schedued for the aforementioned person
    dutyOutgoing = duties(outgoing, cal)

    # Shuffle the duties to add an element of randomness
    random.shuffle(dutyOutgoing)

    # Iterate through everybody, starting with the person with the least points
    for i in points:

        # Choose somebody with low points
        incoming = i[0]

        # Iterate through all the dates the outgoing is schedued for
        for date in dutyOutgoing:

            # If incoming is availible, update the cal
            if viable(date, dict[incoming]['unavail'], incoming, cal, untouchable) == True:

                # Calls on updateP() to swap outgoing with incoming on the date, then return
                updateP(date, outgoing, incoming, cal, dict)

                return
        
        # If nobody is able to do the duty on ALL dates that the outgoing is schedued for, return an error message
        if i == points[-1]:
            sys.exit("Please restart the program.")


def duties(outgoing, cal):
    """
    Create a list consisting of the dates that the specified person is schedued for
    """

    # Initiate duties[]
    duties = []

    # Iterate over each day in cal
    for day in cal.list():

        # If the specified person is schedued on that day, add it to the list
        if day[2] == outgoing:
            duties.append(day[0])

    return duties


def updateP(date, outgoing, incoming, cal, dict):

    """
    Swap outgoing with incoming on the specified date, then update dict{} with the new points. 
    POINTS{} IS NOT UPDATED. CALL ON calcPoints() after this function to update points{}.
    """

    # Schedue duty on the specified date for the incoming
    cal.list()[date-1][2] = incoming

    # Subtract points from outgoing and add points to incoming
    dict[outgoing]['points'] -= cal.list()[date-1][1]
    dict[incoming]['points'] += cal.list()[date-1][1]


def viable(date, unavailIncoming, incoming, cal, untouchable):
    """
    Based on cal, check if incoming is doing duty on the day before/after date, and if incoming is unavail
    """

    # Check if the date is untouchable
    if date in untouchable:
        return False

    # Check if incoming is unavail on the date
    if date in unavailIncoming:
        return False
    
    # If the date is the first or last day of the month, only need to check one adjacent date (after or before respectively)
    if date < 1:
        if incoming == cal.list()[date][2]:
            return False
    elif date >= len(cal.list()): 
        if incoming == cal.list()[date-2][2]:
            return False
    
    # For any other date, check both adjacent days (before and after)
    else:
        if incoming == cal.list()[date-2][2]:
            return False
        if incoming == cal.list()[date][2]:
            return False

    return True


def randomSwap(cal, untouchable, people, dict):

    touchable = []
    for date in cal.list():
        if date[0] in untouchable:
            continue
        touchable.append(date[0])

    random.shuffle(touchable)
    random.shuffle(people)

    for date in touchable:
        for incoming in people:
            if incoming == cal.list()[date - 1][2]:
                continue
            if not viable(date, dict[incoming]['unavail'], incoming, cal, untouchable):
                continue
            cal.list()[date - 1][2] = incoming
            return