#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

//declares all functions

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int calc_index(float l, float w, float s);

int main(void)
{

    //prompts the user for the text
    string text = get_string("Text: ");

    //get all values from the functions: letters, words and sentences
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    //calculates the index value
    int index = calc_index(letters, words, sentences);

    //prints the corresponding grade
    if (index >= 1 && index <= 16)
    {
        printf("Grade %i\n", index);
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade 16+\n");
    }

}


int count_letters(string text)
{

    int length = strlen(text);
    int letters = 0;

    //cheks for the number of letters through the array of characters from the text
    for (int n = 0; n < length; n++)
    {
        if ((text[n] >= 65 && text[n] <= 90) || (text[n] >= 97 && text[n] <= 122))
        {
            letters++;
        }
    }
    return letters;

}


int count_words(string text)
{

    int length = strlen(text);
    int words = 1;

    //cheks for the number of words through the array of characters from the text
    for (int n = 0; n < length; n++)
    {
        if (text[n] == 32)
        {
            words++;
        }
    }
    return words;

}


int count_sentences(string text)
{

    int length = strlen(text);
    int sentences = 0;

    //cheks for the number of sentences through the array of characters from the text
    for (int n = 0; n < length; n++)
    {
        if (text[n] == 46 || text[n] == 63 || text[n] == 33)
        {
            sentences++;
        }
    }
    return sentences;

}

int calc_index(float l, float w, float s)
{

    float av_letters = l * 100 / w;
    float av_sentences = s * 100 / w;

    //uses the formula to give an index value

    float calc = (0.0588 * av_letters) - (0.296 * av_sentences) - 15.8;

    //rounds it to the nearest point

    int index = lround(calc);

    return index;

}
