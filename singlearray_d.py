import time 
from tqdm import tqdm 

class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

def read_input(filename):
    items = []  # Initialize an empty list to store items
    with open(filename, 'r') as file:  

        # Read knapsack capacity and total number of items from the first line
        knapsack_capacity, total_items = map(int, file.readline().split())

        # Read each item's weight and value 
        for _ in range(total_items):
            weight, value = map(int, file.readline().split())
            items.append(Item(value, weight))  # Create Item obkects and add them to the list
    return knapsack_capacity, total_items, items  

def knapsack_dynamic(items, total_items, knapsack_capacity):
    dp = [0] * (knapsack_capacity + 1)
    for n in tqdm(range(total_items), desc="Progress"):  # Iterate over each item
        for k in range(knapsack_capacity, 0, -1):  # Iterate over each capacity
            if items[n].weight <= k:  # If the current item can be included
                # Update the dynamic programming array with the maximum value
                dp[k] = max(dp[k], dp[k - items[n].weight] + items[n].value)
    return dp[knapsack_capacity]  

# Main program
if __name__ == "__main__":
    filename = input("Enter filename: ")  
    start_time = time.time()  # Yoink start time
    knapsack_capacity, total_items, items = read_input(filename)  # Read input data from the file
    print("Knapsack capacity:", knapsack_capacity)  
    print("Total number of items:", total_items)  
    max_value = knapsack_dynamic(items, total_items, knapsack_capacity) 
    print("Maximum value:", max_value)  # Print the maximum value for the knapsack
    end_time = time.time()  # Get the end time
    elapsed_time_seconds = end_time - start_time  # Time in seconds
    elapsed_time_milliseconds = elapsed_time_seconds * 1000  # Time to milliseconds
    print("The program's elapsed time was %.2f seconds (%.2f milliseconds)." % (elapsed_time_seconds, elapsed_time_milliseconds))
# End
