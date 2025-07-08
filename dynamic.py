import time 
from tqdm import tqdm

# Classify items with their values and weights
class item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

# Function to read input data from a file
def read_input(filename):
    items = []  # initialize an empty list to store items
    with open(filename, 'r') as file:
        # Read knapsack capacity and total number of items from the first line
        knapsack_capacity, total_items = map(int, file.readline().split())
        # Read each item's weight and value
        for _ in range(total_items):
            weight, value = map(int, file.readline().split())
            items.append(item(value, weight))  # Create item obkects and add them to the list
    return knapsack_capacity, total_items, items  # Return the parsed data

# Function to solve the knapsack problem with dynamic programming
def knapsack_dynamic(items, total_items, knapsack_capacity):
    dp1 = [0] * (knapsack_capacity + 1)  # Previous row
    dp2 = [0] * (knapsack_capacity + 1)  # Current row

    # iterate over each item
    for n in tqdm(range(total_items), desc="Progress"):
        # iterate over each possible capacity of the knapsack
        for k in range(knapsack_capacity, 0, -1):
            # Checks if the current item can be included without exceeding the capacity
            if items[n].weight <= k:
                # Update the value in dp2 based on whether the current item is included or not
                dp2[k] = max(dp1[k], dp1[k - items[n].weight] + items[n].value)
        # Update the dp1 and dp2 arrays for the next iteration
        dp1, dp2 = dp2, dp1

    # Return the maximum value that can be achieved with the given knapsack capacity
    return dp1[knapsack_capacity]

# Main function
if __name__ == "__main__":
    filename = input("Enter filename: ")  
    start_time = time.time()  # Yoink starting time

    # Read input data from the file and store it in variables
    knapsack_capacity, total_items, items = read_input(filename)
    print("Knapsack capacity:", knapsack_capacity)
    print("Total number of items:", total_items)

    # Solve and get the maximum value
    max_value = knapsack_dynamic(items, total_items, knapsack_capacity)
    print("Maximum value:", max_value)

    end_time = time.time()  # Yoink end time
    elapsed_time_seconds = end_time - start_time  # Calculate the elapsed time in seconds
    elapsed_time_milliseconds = elapsed_time_seconds * 1000  # Convert elapsed time to milliseconds (should work? idk)
    print("The program's elapsed time was %.2f seconds (%.2f milliseconds)." % (elapsed_time_seconds, elapsed_time_milliseconds))

