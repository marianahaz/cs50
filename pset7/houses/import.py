from cs50 import SQL
import csv
import sys

# Check the number of command line arguments
if len(sys.argv) != 2:
    print("Usage error.")
    sys.exit()

# Create the database
open(f"students.db", "w").close()
db = SQL("sqlite:///students.db")

# Define columns in the database
db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

# Write the database
with open(sys.argv[1], "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        names = row['name'].split()
        house = row['house']
        birth = row['birth']

        if (len(names) != 3):
            names.insert(1, None)

        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                   names[0], names[1], names[2], house, birth)

