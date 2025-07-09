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

# Nearest Neighbor algorithm implementation
def nearest_neighbor(coords):
    n = len(coords)
    if n == 0:
        return 0, []

    # Start with a random city
    current_index = random.randint(0, n-1)
    path = [current_index]
    total_distance = 0
    unvisited = set(range(n))
    unvisited.remove(current_index)

    while unvisited:
        nearest_distance = float('inf')
        nearest_index = None

        for next_index in unvisited:
            distance = calculate_distance(coords[current_index], coords[next_index])
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_index = next_index

        path.append(nearest_index)
        unvisited.remove(nearest_index)
        total_distance += nearest_distance
        current_index = nearest_index

    # Complete the tour by returning to the starting city
    total_distance += calculate_distance(coords[path[-1]], coords[path[0]])
    path.append(path[0])

    return total_distance, path

# 2-opt optimization algorithm
def two_opt(coords, path):
    def swap_2opt(path, i, k):
        new_path = path[0:i] + path[i:k+1][::-1] + path[k+1:]
        return new_path

    n = len(path) - 1
    best_distance = calculate_total_distance(coords, path)
    improved = True

    while improved:
        improved = False
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                new_path = swap_2opt(path, i, k)
                new_distance = calculate_total_distance(coords, new_path)
                if new_distance < best_distance:
                    path = new_path
                    best_distance = new_distance
                    improved = True

    return best_distance, path

# Function to calculate the total distance of a given path
def calculate_total_distance(coords, path):
    total_distance = 0
    for i in range(1, len(path)):
        total_distance += calculate_distance(coords[path[i - 1]], coords[path[i]])
    return total_distance

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

# Main program
filename = input("Enter the filename: ").strip()

print(f"Attempting to read file: {filename}")

name, dimension_value, coords = read_tsp_file(filename)

if coords:
    total_distance, nearest_neighbor_path = nearest_neighbor(coords)

    print("Nearest Neighbor Path:", nearest_neighbor_path)
    print("Name:", name)
    print("Dimension:", dimension_value)
    print("Initial Total Distance:", total_distance)
    
    optimized_distance, optimized_path = two_opt(coords, nearest_neighbor_path)
    print("2-opt Optimized Path:", optimized_path)
    print("Optimized Total Distance:", optimized_distance)
    
    plot_paths(coords, nearest_neighbor_path, optimized_path, 'Nearest Neighbor Salesman Path', '2-opt Optimized Salesman Path')
else:
    print("Failed to read coordinates from the file.")
