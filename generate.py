from dPlanner import *
from classes import *


MAXDIFF = 0.5


def main():

    # Check proper format
    if len(sys.argv) not in [4, 5]:
        sys.exit("Usage: python generate.py year month [input].csv [output].csv")

    # Parse command-line arguments
    yy,mm = int(sys.argv[1]),int(sys.argv[2])
    output = sys.argv[4] if len(sys.argv) == 5 else None

    # Load people, dict from specified file
    people, dict = loadData(sys.argv[3])

    # Create calendarPers class based on specified year and month
    calendar = calendarPers(yy,mm)

    while True:

        # Initiate a list for the dates extras are being cleared on
        untouchable = []

        # Fill calendarPers class with random people
        fill(calendar, people, dict, untouchable)

        # Ensure that nobody is schedued on a day that they are unavail
        checkConsis(calendar, dict, people)
        
        # Update the points in dict to reflect the schedued duties, then create points{}, a dictionary sorted by points (ascending)
        updateD(dict, calendar, untouchable)
        points = calcPoints(dict)

        # Initiate counter
        counter = 0
        # While the maximum diference in points exceeds MAXDIFF, swap duties with the function recalibrate()
        while points[-1][1] - points[0][1] > MAXDIFF:
            
            # Person with the most points gives a random duty to the person with the least points
            recalibrate(calendar, points, dict, untouchable)

            # Update points and counter to reflect changes
            points = calcPoints(dict)
            counter += 1

            # If recalibrate() is called 20 times, restart loop as it is PROBABLY looping
            if counter >= 20:
                print("Looping. Attempting to resolve...")
                randomSwap(calendar, untouchable, people, dict)
                counter = 0

        # If user did not specify an output, exit
        if output == None:
            for day in calendar.cal:
                print(f"{day[0]}: {day[2]}")
            sys.exit("Completed." + "\n" + "For a more convenient format, please specify an output. (eg. [output].csv)" + "\n" + "Usage: python generate.py year month [input].csv [output].csv")

        writeTo(output, calendar, people, points, mm, yy, dict)

        sys.exit(f"Completed. Please view {output}")


if __name__ == "__main__":
    main()