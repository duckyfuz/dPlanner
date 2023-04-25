import calendar


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

    def viable(self, date, unavailIncoming, incoming, untouchable):
        """
        Checks for the following:
        1. Date is not in untouchable
        2. Incoming is available on the date
        3. Incoming is not schedued for two consecutive days
        
        Returns False if any of the above are violated.

        Else, if all conditions are met, return True.
        """

        # Check for (1) and (2)
        if date in untouchable or date in unavailIncoming:
            return False
        
        # For the first and last day of the month, only need to check one adjacent date (after or before respectively)
        if date < 1:
            if incoming == self.cal[date][2]:
                return False
        elif date >= len(self.cal): 
            if incoming == self.cal[date-2][2]:
                return False
        
        # For any other date, check both adjacent days (before and after)
        else:
            if incoming == self.cal[date-2][2] or incoming == self.cal[date][2]:
                return False

        return True