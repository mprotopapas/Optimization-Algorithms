#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

#define MAX_ITEMS 10000 // Maximum number of items

typedef struct {
    int capacity;
    int value;
    int weight;
} Item;

// Read input data from file
void readInput(const char* filename, Item* items, int* totalItems, int* knapsackCapacity) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        exit(1);
    }

    // Read knapsack capacity and total number of items
    fscanf(file, "%d %d", knapsackCapacity, totalItems);

    // Read each item's weight and value (cloakers?)
    for (int i = 0; i < *totalItems; ++i) {
        fscanf(file, "%d %d", &items[i].weight, &items[i].value); // weight first, value afterward
    }

    fclose(file);
}
// Randomly select items from the list and add them to the knapsack
void knapsackRandom(Item* items, int totalItems, int knapsackCapacity) {
    int knapsackWeight = 0;
    int knapsackValue = 0;
    bool selected[totalItems];

    for (int i = 0; i < totalItems; i++)
        selected[i] = false;

    srand(time(NULL));

    printf("Items selected:\n");

    int itemsSelected = 0;

    while (knapsackWeight < knapsackCapacity && itemsSelected < totalItems) {
        bool found = false;
        int randomIndex;
        int lookingForItem = 100; // Maximum iterations without finding a new item to prevent the while loop from running forever (mas phran ta items bro)

        while (!found && lookingForItem > 0) {
            randomIndex = rand() % totalItems;
            if (!selected[randomIndex] && knapsackWeight + items[randomIndex].weight <= knapsackCapacity) {
                found = true;
            }
            lookingForItem--; // Reduce the "patience" meter for finding a new item 
        }

        if (!found) {
            // Break out of the loop if no suitable item was found (Pou einai ta items bro?)
            break;
        }

        // Add the found item to the knapsack
        printf("Item %d - Value: %d, Weight: %d\n", randomIndex + 1, items[randomIndex].value, items[randomIndex].weight);
        selected[randomIndex] = true;
        knapsackWeight += items[randomIndex].weight;
        knapsackValue += items[randomIndex].value;
        itemsSelected++;
    }

    printf("Total value: %d\n", knapsackValue);
}



// Main program
int main() {
    char filename[100]; //Assuming filename won't be longer than 100 chars
    printf("Enter filename: ");
    scanf("%s", filename);
    Item items[MAX_ITEMS];
    int totalItems, knapsackCapacity;
    clock_t starttime, endtime;
    double elapsed_time;    

    starttime = clock();

    readInput(filename, items, &totalItems, &knapsackCapacity);

    printf("Knapsack capacity: %d\n", knapsackCapacity);
    printf("Total number of items: %d\n", totalItems);

    knapsackRandom(items, totalItems, knapsackCapacity);

    endtime = clock();
    elapsed_time  = ((double) (endtime - starttime)) / CLOCKS_PER_SEC * 1000;
    printf("\n The program's elapsed time was %.2f milliseconds.\n", elapsed_time); 

    return 0;
}
