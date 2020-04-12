from cs50 import get_string

text = get_string("Text: ")

# Count the number of letters, words and sentences.


def main():

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    index = calc_index(letters, words, sentences)

    if index >= 1 and index <= 16:
        print("Grade ", index)

    elif index < 1:
        print("Before Grade 1")

    else:
        print("Grade 16+")


def count_letters(string):

    counter = 0
    for a in string:
        if (a.isalpha()) == True:
            counter += 1

    return counter


def count_words(string):
    counter = 0
    for a in string:
        if (a.isspace()) == True:
            counter += 1

    return counter + 1


def count_sentences(string):
    counter = 0
    for a in string:
        if a == '?' or a == '.' or a == '!':
            counter += 1

    return counter


def calc_index(l, w, s):
    av_let = l * 100 / w
    av_sen = s * 100 / w

    calc = (0.0588 * av_let) - (0.296 * av_sen) - 15.8

    return round(calc)


# Call the main function
main()
