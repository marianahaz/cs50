import sys
import csv

# Command line arguments: ensure that there are 3 arguments
if len(sys.argv) != 3:
    print("Usage: python dna.py database.csv sequence.txt")
    sys.exit()

# Get the DNA sequence from the txt file
sequenceFile = open(sys.argv[2], "r")
sequence = sequenceFile.read()

# Load the database to a dictionary and get the keys
database = {}
with open(sys.argv[1], "r") as databaseFile:
    for line in databaseFile:
        name, keys = line.strip().split(",", 1)
        database[name] = keys.split(",")

keys = database.get('name')

# print(keys)

# Create a dict to store each key's value to compare
finalNumberKey = {}

for i in range(len(keys)):
    key = keys[i]
    max_number = 0
    current = 0

    for j in range(len(sequence)):

        if key == sequence[j: j + len(key)]:
            if sequence[j - len(key): j] == sequence[j: j + len(key)]:
                current += 1
                j += len(key)

        elif current != 0:
            continue
        else:
            current = 1

        if max_number < current:
            max_number = current

    # print(max_number)
    finalNumberKey[key] = max_number

# for i in range(len(totalValues))

finalValues = list(finalNumberKey.values())
# print(finalValues)

# for i in range(len(database)):
database.pop('name')


for key in database.keys():
    dna = list(database[key])
    dna = list(map(int, dna))
    # print(dna)
    if dna == finalValues:
        print(key)
        exit()

print("No match")


# Close all files
sequenceFile.close()
databaseFile.close()

