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

    // Read each item's weight and value
    for (int i = 0; i < *totalItems; ++i) {
        fscanf(file, "%d %d", &items[i].weight, &items[i].value);
    }

    fclose(file);
}
//  Compare the items passed on their Weight to value ratio  
int compareItems(const void* a, const void* b) {
    double ratioA = ((double)(((Item*)a)->value)) / (((Item*)a)->weight); 
    double ratioB = ((double)(((Item*)b)->value)) / (((Item*)b)->weight);
    if (ratioA < ratioB) // if less than b, places a after b
        return 1;
    else if (ratioA > ratioB) // if greater than b, place before b
        return -1;
    else
        return 0; // else equal
}

// Knapsack Greedy technique
void knapsackGreedy(Item* items, int totalItems, int knapsackCapacity) {
    int knapsackWeight = 0;
    int knapsackValue = 0;

    // Create a copy of items to track original positions so it prints the original item's position instead of the sorted one
    Item itemsCopy[MAX_ITEMS];
    for (int i = 0; i < totalItems; ++i) {
        itemsCopy[i] = items[i];
    }

    // Sort items based on their value-to-weight ratio in non-increasing order (Euxaristo qsort)
    qsort(items, totalItems, sizeof(Item), compareItems);

    printf("Items selected:\n");

    for (int i = 0; i < totalItems; ++i) {
        // Find the original position of the item
        int originalPos;
        for (originalPos = 0; originalPos < totalItems; ++originalPos) {
            if (itemsCopy[originalPos].value == items[i].value && itemsCopy[originalPos].weight == items[i].weight) {
                break;
            }
        }

        if (knapsackWeight + items[i].weight <= knapsackCapacity) {
            // If adding the item doesn't exceed knapsack capacity, add it
            printf("Item %d - Value: %d, Weight: %d, Value/Weight: %.2f\n", originalPos + 1, items[i].value, items[i].weight, (double)items[i].value / items[i].weight);
            knapsackWeight += items[i].weight;
            knapsackValue += items[i].value;
        }
    }

    printf("Total value: %d\n", knapsackValue);
}

// Main program
int main() {
    char filename[100]; //Assuming filename won't be longer than 100 chars
    printf("Enter filename: ");
    scanf("%s", filename); // Read the file from user
    Item items[MAX_ITEMS];
    int totalItems, knapsackCapacity;
    clock_t starttime, endtime; // Initiate time variables
    double elapsed_time;

    starttime = clock() ; // Yoink start time

    readInput(filename, items, &totalItems, &knapsackCapacity);

    printf("Knapsack capacity: %d\n", knapsackCapacity);
    printf("Total number of items: %d\n", totalItems);

    knapsackGreedy(items, totalItems, knapsackCapacity);

    endtime = clock(); // Yoink end time
    elapsed_time  = ((double) (endtime - starttime)) / CLOCKS_PER_SEC * 1000; // Time in ms
    printf("\n The program's elapsed time was %.2f milliseconds.\n", elapsed_time);

    return 0;
}
