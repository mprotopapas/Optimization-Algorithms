import random
import math
import matplotlib.pyplot as plt

# Class to store the coordinates of a point
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Function to read a TSP file and extract the coordinates
def read_tsp_file(filename):
    coords = []
    dimension_value = 0
    name = ""

    try:
        with open(filename, 'r') as file:
            in_node_section = False
            for line in file:
                line = line.strip()
                if line.startswith("NAME"):
                    # Extract the name of the problem
                    name = line.split(":")[1].strip()
                elif line.startswith("DIMENSION"):
                    # Extract the number of nodes
                    dimension_value = int(line.split(":")[1].strip())
                elif line.startswith("NODE_COORD_SECTION"):
                    # Start reading the coordinates
                    in_node_section = True
                elif in_node_section:
                    parts = line.split()
                    if len(parts) >= 3:
                        # Extract and store the coordinates
                        x, y = map(float, parts[1:])
                        coords.append(Coordinate(x, y))
                    # Stop reading if we have reached the specified number of nodes
                    if len(coords) == dimension_value:
                        break
        return name, dimension_value, coords
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return None, None, []
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None, []

# Function to calculate the Euclidean distance between two points
def calculate_distance(coord1, coord2):
    return math.sqrt((coord1.x - coord2.x) ** 2 + (coord1.y - coord2.y) ** 2)

# Function to generate a random path and calculate its total distance
def generate_random_path(coords, seed=None):
    if seed is not None:
        random.seed(seed)

    dimension_value = len(coords)
    path = list(range(dimension_value))
    random.shuffle(path)
    path.append(path[0])  # Return to the starting point to complete the loop

    total_distance = 0
    for i in range(1, len(path)):
        total_distance += calculate_distance(coords[path[i - 1]], coords[path[i]])
    
    return total_distance, path

# Function to plot the path on a graph
def plot_paths(coords, initial_path, optimized_path, initial_title, optimized_title):
    x_initial = [coords[i].x for i in initial_path]
    y_initial = [coords[i].y for i in initial_path]
    x_optimized = [coords[i].x for i in optimized_path]
    y_optimized = [coords[i].y for i in optimized_path]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

    ax1.plot(x_initial, y_initial, marker='o', linestyle='-', linewidth=1, markersize=4, color='b')
    ax1.set_title(initial_title)
    ax1.set_xlabel('X Coordinate')
    ax1.set_ylabel('Y Coordinate')
    ax1.legend(['Path'], loc='best')
    ax1.grid(True)

    ax2.plot(x_optimized, y_optimized, marker='o', linestyle='-', linewidth=1, markersize=4, color='b')
    ax2.set_title(optimized_title)
    ax2.set_xlabel('X Coordinate')
    ax2.set_ylabel('Y Coordinate')
    ax2.legend(['Path'], loc='best')
    ax2.grid(True)

    plt.show()

# Function to perform 2-opt optimization
def two_opt(coords, path):
    def reverse_segment_if_better(path, i, k):
        new_path = path[:i] + path[i:k + 1][::-1] + path[k + 1:] 
        if calculate_total_distance(coords, new_path) < calculate_total_distance(coords, path):
            return new_path
        return path

    def calculate_total_distance(coords, path): #Calculate the total distance of the given path.
        return sum(calculate_distance(coords[path[i - 1]], coords[path[i]]) for i in range(len(path))) #Return the float

    improved = True
    while improved:
        improved = False
        for i in range(1, len(path) - 2): # Iterate over all possible pairs of indices (i, k) in the path
            for k in range(i + 1, len(path) - 1):
                new_path = reverse_segment_if_better(path, i, k) # Try to reverse the segment and check if it improves the path
                if new_path != path:
                    path = new_path # If better path is found, update it
                    improved = True # Break the loop
    return path

# Main program
filename = input("Enter the filename: ").strip()

print(f"Attempting to read file: {filename}")

name, dimension_value, coords = read_tsp_file(filename)

if coords:
    # Generate a random path
    total_distance, random_path = generate_random_path(coords, seed=42)

    print("Random Path:", random_path)
    print("Name:", name)
    print("Dimension:", dimension_value)
    print("Total Distance (Random Path):", total_distance)
    
    # Perform 2-opt optimization
    optimized_path = two_opt(coords, random_path)
    optimized_distance = sum(calculate_distance(coords[optimized_path[i - 1]], coords[optimized_path[i]]) for i in range(len(optimized_path)))

    print("Optimized Path:", optimized_path)
    print("Total Distance (Optimized Path):", optimized_distance)
    
    # Plot both paths side by side
    plot_paths(coords, random_path, optimized_path, 'Randomly Generated Salesman Path', '2-opt Optimized Salesman Path')
else:
    print("Failed to read coordinates from the file.")
