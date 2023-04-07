import calendar

class Person():

    def __init__(self, name, unavail, points):
        """Create a new person with name(str), unavail(list), points(int)"""
        self.name = name
        self.unavail = unavail
        self.points = points

        self.duties = []

    def __hash__(self):
        return hash(self.name, self.unavail, self.points)

    def __eq__(self, other):
        return (
            (self.name == other.name) and
            (self.unavail == other.unavail) and
            (self.points == other.points)
        )

    def __str__(self):
        return f"{self.name}{chr(10)}{self.unavail}{chr(10)}{self.points}"

    def __repr__(self):
        name = repr(self.name)
        return f"Person({name}, {self.unavail}, {self.points})"


class calendarPers():

    def __init__(self, yy, mm):
        """Create a list of lists(date,MTWT/Fri/Sat/Sun,person)"""
        self.cal = []
        for x in range(calendar.monthrange(yy,mm)[1]):

            # Find out which day it is
            MTWT = [0,1,2,3]
            if int(calendar.weekday(yy,mm,x+1)) in MTWT:
                day = 1
            elif int(calendar.weekday(yy,mm,x+1)) == 4:
                day = 1.5
            elif int(calendar.weekday(yy,mm,x+1)) == 5:
                day = 2
            elif int(calendar.weekday(yy,mm,x+1)) == 6:
                day = 2               

            self.cal.append([x+1,day,None])

    def __repr__(self): 
        return f"{self.cal}"
    
    def list(self):
        return self.cal

    def update(self, date, pers):
        """Given a date and a name, update the calendar to reflect as such"""
        self.cal[date-1][2] = pers