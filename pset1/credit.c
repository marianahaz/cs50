#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    long number; //declare the variable
    
    //prompts the user for a credit card number
    do
    {
        number = get_long("Number: ");
    }
    while (number < 0);
    
    long find_digits = number;
    int digits = 0;
    
    //finds out how many digits
    while (find_digits != 0)
    {
        find_digits = find_digits / 10;
        digits++;
    }
    
    
    
    int ten = 10;
    int x;
    int count1 = 0;
    long new_no = number;
    
    //sum of every other digit
    while (new_no != 0)
    {
        new_no = new_no / ten;
        x = (new_no % 10) * 2;
        
        //force to take the digits
        if (x / 10 != 0)
        {
            int a = x / 10;
            int b = x % 10;
            count1 = count1 + a + b;
        }
        else
        {
            count1 = count1 + x;
        }
        
        ten = 100;
    }
    
    //get sum of other numbers
    long n_no = number;
    int y;
    int count2 = 0;
    
    while (n_no != 0)
    {
        y = n_no % 10;
        count2 = count2 + y;
        n_no = n_no / ten;    
    }
    
    //sum everything
    int countSum = count1 + count2;
    
    
    //first 2 digits or first digit
    int first2digits = 0;
    int firstdigit = 0;
    
    //checks first digits
    
    if (digits == 15)
    {
        first2digits = number / pow(10, 13);
    }
    else if (digits == 16)
    {
        first2digits = number / pow(10, 14);
        firstdigit = number / pow(10, 15);
    }
    else if (digits == 13)
    {
        firstdigit = number / pow(10, 12);
    }
    
    //prints the final answer
    
    if (countSum % 10 != 0)
    {
        printf("INVALID\n"); //invalid if the countSum is not 0
    }
    else if (digits == 15)
    {
        if (first2digits == 34 || first2digits == 37)
        {
            printf("AMEX\n"); //AMEX per instructions
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (digits == 16 && (first2digits < 56 && first2digits > 50))
    {
        printf("MASTERCARD\n"); //mastercard per instructions
    }
    else if ((digits == 13 && firstdigit == 4) || (digits == 16 && (first2digits <= 49 && first2digits >= 40)) ||
             (digits == 16 && firstdigit == 4))
    {
        printf("VISA\n"); //visa per instructions
    }
    else
    {
        printf("INVALID\n"); //invalid if it returns a valid countSum but doesnt fit the other requirements
    }  
        
    
    
    
}
