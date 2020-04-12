#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string name = get_string("What's your name?\n"); //asks user for their name
    printf("hello, %s\n", name); //prints user's name with variable
}
