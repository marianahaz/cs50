#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2) //error if there is no command line input
    {
        printf("Usage: ./substitution key.\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26) //error if key is not 26 characters long
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < 26; i++)
        {
            if (argv[1][i] < 65 || (argv[1][i] > 90 && argv[1][i] < 97) || argv[1][i] > 122) //error if it contains anything other than a letter
            {
                printf("Key must contain only alphabetical characters.\n");
                return 1;
            }
            else
            {
                for (int n = 0; n < strlen(argv[1]); n++)  //error if there are repeated characters
                {
                    if (n == i)
                    {
                        continue;
                    }
                    if (argv[1][i] == argv[1][n])
                    {
                        printf("Key must not contain repeated characters.\n");
                        return 1;
                    }
                }

            }
        }
    }

    string key = argv[1];

    string plain = get_string("plaintext: "); //prompts the user for a text

    for (int c = 0; c < strlen(plain); c++)
    {
        if (plain[c] >= 97 && plain[c] <= 122) //lowercase check
        {
            plain[c] = tolower(key[(plain[c] - 97)]); //assigns the keyed character to the actual plain text
        }
        else if (plain[c] >= 65 && plain[c] <= 90) //uppercase check
        {
            plain[c] = toupper(key[(plain[c] - 65)]);
        }
    }

    printf("ciphertext: %s\n", plain);
    return 0;



}
