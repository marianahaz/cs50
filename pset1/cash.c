#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    
    float change; //creates the variable    
    //prompt the user for a positive value    
    do
    {
        change = get_float("Change owed: "); 
    }
    while (change < 0);


    int value = round(change * 100); //rounds the value to an integer
    
// how many 25 cents coins owed

    int quarter = value / 25;

    int rest_quarter = value % 25;

// how many 10 cents coins owed

    int dime = rest_quarter / 10;

    int rest_dime = rest_quarter % 10;

// how many 5 cents coins owed

    int nickel = rest_dime / 5;
    
    int penny = rest_dime % 5;
    
    int total_coins = quarter + dime + nickel + penny; //calculates total coins
    
    
    printf("%i\n", total_coins);

}
