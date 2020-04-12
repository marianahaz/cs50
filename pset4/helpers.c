#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    // Iterate over each row
    for (int i = 0; i < height; i++)
    {

        // Iterate over each column in a particular row
        for (int n = 0; n < width; n++)
        {

            float average = ((float) image[i][n].rgbtRed + (float) image[i][n].rgbtGreen + (float) image[i][n].rgbtBlue) / 3;
            int roundAverage = round(average);

            image[i][n].rgbtRed = roundAverage;
            image[i][n].rgbtGreen = roundAverage;
            image[i][n].rgbtBlue = roundAverage;

        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0; i < height; i++)
    {

        for (int n = 0; n < width; n++)
        {

            int sepiaRed = round(0.393 * (float) image[i][n].rgbtRed + 0.769 * (float) image[i][n].rgbtGreen + 0.189 *
                                 (float) image[i][n].rgbtBlue);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            int sepiaGreen = round(0.349 * (float) image[i][n].rgbtRed + 0.686 * (float) image[i][n].rgbtGreen + 0.168 *
                                   (float) image[i][n].rgbtBlue);
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            int sepiaBlue = round(0.272 * (float) image[i][n].rgbtRed + 0.534 * (float) image[i][n].rgbtGreen + 0.131 *
                                  (float) image[i][n].rgbtBlue);
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[i][n].rgbtRed = sepiaRed;
            image[i][n].rgbtGreen = sepiaGreen;
            image[i][n].rgbtBlue = sepiaBlue;

        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    // Checks if the width is an even or odd number
    int halfWidth;

    if (width % 2 == 0)
    {
        halfWidth = width / 2;
    }
    else
    {
        halfWidth = round((float) width / 2);
    }

    for (int i = 0; i < height; i++)
    {

        for (int n = 0; n < halfWidth; n++)
        {

            RGBTRIPLE tmp = image[i][n];

            image[i][n] = image[i][width - 1 - n];

            image[i][width - 1 - n] = tmp;

        }

    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Creates copy of image
    RGBTRIPLE imageCopy[height][width];

    // Declares all variables it will need
    float totalRed;
    float totalGreen;
    float totalBlue;

    // Declares a variable that will divide (number of pixels around)
    float squares;

    // Iterates over rows
    for (int i = 0; i < height; i++)
    {

        // Iterates over columns
        for (int n = 0; n < width; n++)
        {

            totalRed = 0;
            totalGreen = 0;
            totalBlue = 0;
            squares = 0;

            // Iterates over nearby rows
            for (int x = -1; x < 2; x++)
            {

                // Checks if it's overflowing the rows
                if (i + x < 0 || i + x > height - 1)
                {
                    continue;
                }

                // Iterates over nearby columns
                for (int y = -1; y < 2; y++)
                {

                    // Checks if it's overflowing the columns
                    if (n + y < 0 || n + y > width - 1)
                    {
                        continue;
                    }

                    // Adds each value to a total
                    totalRed = totalRed + image[i + x][n + y].rgbtRed;
                    totalGreen = totalGreen + image[i + x][n + y].rgbtGreen;
                    totalBlue = totalBlue + image[i + x][n + y].rgbtBlue;
                    squares++;

                }


            }

            // Copies the rounded values
            imageCopy[i][n].rgbtRed = round(totalRed / squares);
            imageCopy[i][n].rgbtGreen = round(totalGreen / squares);
            imageCopy[i][n].rgbtBlue = round(totalBlue / squares);


        }

    }

    for (int i = 0; i < height; i++)
    {
        for (int n = 0; n < width; n++)
        {
            image[i][n] = imageCopy[i][n];
        }
    }

    return;
}
