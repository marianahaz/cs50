from cs50 import get_float

change = get_float("Change owed: ")

while change < 0:
    change = get_float("Change owed: ")

# Round the value to an integer
value = int(change * 100)

# Quarter is 25 cents
quarters = int(value / 25)
rest_quarters = int(value % 25)

# Dime is 10 cents
dimes = int(rest_quarters / 10)
rest_dimes = int(rest_quarters % 10)

# Nickel is 5 cents
nickels = int(rest_dimes / 5)

# Penny is 1 cent
pennies = int(rest_dimes % 5)

total = quarters + dimes + nickels + pennies

print(total)
