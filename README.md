<p align="center">

██████╗░██████╗░██╗░░░░░░█████╗░███╗░░██╗███╗░░██╗███████╗██████╗░
██╔══██╗██╔══██╗██║░░░░░██╔══██╗████╗░██║████╗░██║██╔════╝██╔══██╗
██║░░██║██████╔╝██║░░░░░███████║██╔██╗██║██╔██╗██║█████╗░░██████╔╝
██║░░██║██╔═══╝░██║░░░░░██╔══██║██║╚████║██║╚████║██╔══╝░░██╔══██╗
██████╔╝██║░░░░░███████╗██║░░██║██║░╚███║██║░╚███║███████╗██║░░██║
╚═════╝░╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
</p>

### Sample command: python3 generate.py 2023 5 data/may.csv data/output.csv
### REMINDER: Add the first day of the month as an unavail date for the person who did duty on the last day of the previous month

## Background:
This program was created to automate the process of creating a duty list, under the assumption that ONE person must be schedued for each day.

### Futher Assumptions:
Doing duty rewards one with points, and the amount of points awarded depends on the type of day it is.
#### As of now:
Monday - Thurday: 1 point 
Friday: 1.5 points
Saturday, Sunday: 2 points

### Features: 
(1) Extras - Punishments carried out on Saturday / Sunday. Clearing an extra means forfeiting the 2 points that usually come with doing duty on the day.
(2) Extras-to-be-done - Individuals do not have to clear all their extras in one month. Each person can indicate how many extras they want to clear in a single month.
(3) Points History - Points awarded from previous months are taken into account when planning. 
(4) Points Equity - After finishing the schedue, the person with the most points and the person with the least points will only differ by MAXDIFF, a global variable in generate.py.
(5) Availability - Duty schedue will be planned around each person's availability. 

## Pending Issues:

1. Some edge cases will stop the program entirely. Attempt to autonate a restart such that the user does not have to input their values again.
2. Extras cannot be cleared on a public holiday. 
3. Public holidays do not award one with 2 points. 