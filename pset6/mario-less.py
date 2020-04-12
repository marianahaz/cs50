from cs50 import get_int


height = get_int("Height: ")

while height < 1 or height > 8:
    height = get_int("Height: ")

for i in range(height):

    for j in range((height-1), i, -1):
        print(" ", end="")
    for k in range(0, i+1, 1):
        print("#", end="")

    print()
