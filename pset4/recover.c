#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE; // Declares a variable that can hold an 8-bit positive int

int main(int argc, char *argv[])
{

    // Error if there is no command line argument
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open the file for reading
    FILE *memoryCard = fopen(argv[1], "r");

    // Make sure the file is not NULL
    if (memoryCard == NULL)
    {
        printf("Error\n");
        return 1;
    }

    // Read through the file using fread
    BYTE buffer[512];
    int counter = 0;
    char *imageFile = malloc(8);
    FILE *image;
    while (fread(buffer, 512, 1, memoryCard))
    {

        // Search for JPEGs
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {

            if (counter > 0)
            {
                fclose(image);
            }

            // Start by creating the JPEG file
            sprintf(imageFile, "%03i.jpg", counter); // Create file name (with the numbers)
            image = fopen(imageFile, "w"); // Opens a new file pointer for writing

            // Increases the next file name number
            counter++;

        }

        // Effectively writes the file
        if (counter > 0)
        {
            fwrite(buffer, 512, 1, image);
        }

    }

    // Free memory
    free(imageFile);

    // Close the file
    fclose(image);
    fclose(memoryCard);
    return 0;

}
