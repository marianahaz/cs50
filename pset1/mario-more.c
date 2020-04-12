#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h; //declares the variable
    
    // prompting the user for a value between 1 and 8
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);
    
    for (int i = 0; i < h; i++) // number of lines
    {
        for (int s = h - 1; s > i; s--) // align right
        {
            printf (" ");
        }
        for (int w = 0; w <= i; w++) // prints first hashes
        {
            printf ("#");
        }
        
        printf ("  "); // prints the space between columns
        
        for (int w = 0; w <= i; w++) //prints second hashes
        {
            printf ("#");
        }
        
        printf ("\n"); // breaks line
    }
    
}
