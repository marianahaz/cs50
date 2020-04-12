#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h; // creates the variable
    // creates a loop to ask the user for a certain height between 1 and 8 
    do
    {
        h = get_int("Height: "); 
    }
    while (h < 1 || h > 8);
    
    // outside for: iterates the number of lines
    // first inside for: prints the dots
    // second inside for: prints the number of #'s per line
    for (int i = 1; i <= h; i++)
    {
        
        for (int d = h - 1; d >= i; d--)
        {
            printf(" ");
        }
        for (int n = 0; n < i; n++)
        {
            printf("#");
        }
        printf("\n");
    }
    
    
}
