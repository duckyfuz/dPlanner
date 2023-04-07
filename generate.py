import sys
import copy

from dPlanner import *


def checkConsis():
    pass
    # Check that there is somebody on duty everyday (?)
    # Check that nobody does 2 consecutive duties
    # Check that nobody is doing duty on an unavail day
    # Check that people with extras are doing them on a weekend/public holiday


def fill(cal):

    

def main():

    # TEMPORARY -> SWITCH TO READING CSV FILE IN data/
    people = ["Josh", "Jay"]
    Josh = Person("Josh",[1,2],5)
    Jay = Person("Jay",[4,5],3)

    # Check proper format
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py year month [output]")

    # Parse command-line arguments
    yy = int(sys.argv[1])
    mm = int(sys.argv[2])
    output = sys.argv[3] if len(sys.argv) == 4 else None

    calendar = calendarPers(yy,mm)

    calandar = fill(calendar)

    print(calendar)


if __name__ == "__main__":
    main()