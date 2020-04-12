// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Creates a variable for size
int wordCounter = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table (one for each letter of the alphabet)
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Hash word to find the bucket
    int bucket = hash(word);

    // Create a variable to point to the first element of the linked list
    node *cursor = table[bucket];

    if (cursor == NULL)
    {
        return false;
    }

    if (strcasecmp(cursor->word, word) == 0)
    {
        return true;
    }

    // Traverse the linked list to try and find a match. If it does, return true
    while (cursor->next != NULL)
    {
        cursor = cursor->next;

        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
    }

    // Else return false (did not find the word in the dictionary)
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Created 26 buckets, one for each letter of the alphabet
    int firstLetter = (int) tolower(word[0]);
    int bucketNumber = firstLetter - 97;

    return bucketNumber;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{

    // Open the dictionary file with fopen()
    FILE *file = fopen(dictionary, "r");

    // Check if return value is NULL; if it is, ends program
    if (file == NULL)
    {
        printf("Error loading file.\n");
        return false;
    }

    char *newWord = malloc(LENGTH + 1);
    if (newWord == NULL)
    {
        return false;
    }

    // Read strings from file until EOF
    while (fscanf(file, "%s", newWord) != EOF)
    {

        // Create a new node and check if it returns NULL
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        // Copy the dictionary word into the node
        strcpy(n->word, newWord);

        // Finds the bucket into which this word is going to be added
        int bucket = hash(newWord);

        // Points to the start of the linked list
        n->next = table[bucket];

        // Point at n as the beggining of the list
        table[bucket] = n;


        wordCounter++;

    }

    // Close the file
    fclose(file);
    free(newWord);

    return true;

    printf("%i\n", wordCounter);
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordCounter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{

    node *cursor;
    node *tmp;

    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            cursor = table[i];
            tmp = cursor;

            while (cursor->next != NULL)
            {
                cursor = cursor->next;
                free(tmp);
                tmp = cursor;
            }

            free(cursor);
        }
    }

    return true;

}
