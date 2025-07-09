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

# Function to calculate the total distance of a path
def calculate_total_distance(coords, path):
    return sum(calculate_distance(coords[path[i - 1]], coords[path[i]]) for i in range(len(path)))

# Function to perform simulated annealing
def simulated_annealing(coords, initial_path, initial_temp, cooling_rate, num_iterations):
    current_path = initial_path
    current_distance = calculate_total_distance(coords, current_path)
    best_path = list(current_path)
    best_distance = current_distance
    temperature = initial_temp

    for i in range(num_iterations):
        # Create a new neighboring solution by swapping two cities
        new_path = list(current_path)
        l = len(new_path) - 1
        a, b = random.sample(range(1, l), 2)
        new_path[a], new_path[b] = new_path[b], new_path[a]

        new_distance = calculate_total_distance(coords, new_path)

        # Accept the new solution with a probability dependent on the temperature and the distance difference
        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temperature):
            current_path = new_path
            current_distance = new_distance

        # Update the best solution found so far
        if current_distance < best_distance:
            best_path = current_path
            best_distance = current_distance

        # Cool down the temperature
        temperature *= cooling_rate

    return best_distance, best_path

# Function to plot the paths on a graph
def plot_path(coords, path, optimized_path=None, title="Salesman Path Comparison"):
    plt.figure(figsize=(20, 8))

    if optimized_path:
        # Plot the initial random path
        plt.subplot(1, 2, 1)
        x_random = [coords[i].x for i in path]
        y_random = [coords[i].y for i in path]
        plt.plot(x_random, y_random, marker='o', linestyle='-', linewidth=1, markersize=4, color='b')
        plt.title('Randomly Generated Salesman Path')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend(['Path'], loc='best')
        plt.grid(True)

        # Plot the optimized path
        plt.subplot(1, 2, 2)
        x_optimized = [coords[i].x for i in optimized_path]
        y_optimized = [coords[i].y for i in optimized_path]
        plt.plot(x_optimized, y_optimized, marker='o', linestyle='-', linewidth=1, markersize=4, color='b')
        plt.title('Simulated Annealing Optimized Salesman Path')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend(['Path'], loc='best')
        plt.grid(True)
    else:
        # Plot a single path
        x = [coords[i].x for i in path]
        y = [coords[i].y for i in path]
        plt.plot(x, y, marker='o', linestyle='-', linewidth=1, markersize=4, color='b')
        plt.title(title)
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend(['Path'], loc='best')
        plt.grid(True)

    plt.show()

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
    
    # Simulated annealing parameters
    initial_temp = 10000
    cooling_rate = 0.995
    num_iterations = 100000
    
    # Perform simulated annealing
    optimized_distance, optimized_path = simulated_annealing(coords, random_path, initial_temp, cooling_rate, num_iterations)

    print("Optimized Path:", optimized_path)
    print("Total Distance (Optimized Path):", optimized_distance)
    
    # Plot both paths for comparison
    plot_path(coords, random_path, optimized_path)
else:
    print("Failed to read coordinates from the file.")
