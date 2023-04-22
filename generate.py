from dPlanner import *
from classes import *


MAXDIFF = 0.5


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

        # Create new format for points
        pointsP = []
        for person in points:
            pointsP.append(person[0] + ": " + str(person[1]) + "pts")
        
        print(pointsP)

        # If user did not specify an output, exit
        if output == None:
            sys.exit()

        # Open a new file to write in
        with open(output, 'w', newline='') as f:
            writer = csv.writer(f)

            # Write introductory lines
            writer.writerow(["Hello all", ""])
            writer.writerow(["These are the duties for the " + str(mm) + "th month of " + str(yy) + ":"])
            writer.writerow([])

            # Iterate through each day and add a new line for each day
            for day in calendar.list():
                writer.writerow([str(day[0]) + ". " + day[2]])
            writer.writerow([])

            # Add introcutory line
            writer.writerow(["As of now", ""])

            # Iterate through each person and add a new line for each person with outstanding extras
            for person in people:
                if dict[person]['leftovers'] == 0:
                    continue
                writer.writerow([person + " still has " + str(dict[person]['leftovers']) + " outstanding extras to clear."])


        sys.exit()


if __name__ == "__main__":
    main()