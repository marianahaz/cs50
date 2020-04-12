import sys
from cs50 import SQL

if len(sys.argv) != 2:
    print("Usage error.")
    sys.exit()

db = SQL("sqlite:///students.db")

# Get the house input
house = sys.argv[1]

# Select the name of each student, already ordered, and store in a variable
studentList = db.execute(f"SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house)

# Print the info to the user
for key in studentList:
    if key['middle'] == None:
        print('{} {}, born {}'.format(key['first'], key['last'], key['birth']))
    else:
        print("{} {} {}, born {}".format(key['first'], key['middle'], key['last'], key['birth']))
