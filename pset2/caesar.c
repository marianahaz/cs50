#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{

    int key = 0; //creates a variable for key

    if (argc != 2) //if the user doesnt write 2 arguments
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < strlen(argv[1]); i++) //iterates over the string
        {
            if (isdigit(argv[1][i]) == 0)
            {
                printf("Usage: ./caesar key\n");
                return 1; //terminates the program if it is not a digit
            }
            else
            {
                key = atoi(argv[1]); //if everything is okay, stores the key
            }
        }

        string plaintext = get_string("plaintext: "); //prompts user for key

        printf("ciphertext: ");

        for (int i = 0; i < strlen(plaintext); i++) //iterates over the plaintext
        {
            if (plaintext[i] >= 65 && plaintext[i] <= 90) //for uppercase
            {
                int new_character = ((plaintext[i] - 64 + key) % 26) + 64; //finds the place from 1-25 where it should be, then adds 64 to go back
                printf("%c", new_character);
            }
            else if (plaintext[i] >= 97 && plaintext[i] <= 122) //for lowercase
            {
                int new_character = ((plaintext[i] - 96 + key) % 26) + 96;
                printf("%c", new_character);
            }
            else
            {
                printf("%c", plaintext[i]); //prints the char if its not a letter
            }

        }

        printf("\n");

    }


}
