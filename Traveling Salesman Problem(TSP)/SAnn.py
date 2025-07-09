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

# Nearest Neighbor algorithm implementation starting at the given node
def nearest_neighbor(coords, start_node):
    n = len(coords)
    if n == 0:
        return 0, []

    current_index = start_node
    path = [current_index]
    total_distance = 0
    unvisited = set(range(n)) - {start_node}

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

    total_distance += calculate_distance(coords[path[-1]], coords[path[0]])
    path.append(path[0])

    return total_distance, path

# Function to calculate the total distance of a path
def calculate_total_distance(coords, path):
    return sum(calculate_distance(coords[path[i - 1]], coords[path[i]]) for i in range(len(path)))

# Function to perform simulated annealing with enhanced swapping mechanism
def simulated_annealing(coords, initial_path, initial_temp, cooling_rate, num_iterations):
    current_path = initial_path[:]
    current_distance = calculate_total_distance(coords, current_path)
    best_path = list(current_path)
    best_distance = current_distance
    temperature = initial_temp

    for i in range(num_iterations):
        # Create a new neighboring solution by swapping or reversing a segment
        new_path = list(current_path)
        l = len(new_path) - 1
        move_type = random.choice(["swap", "reverse", "shift"])
        if move_type == "swap":
            a, b = random.sample(range(1, l), 2)  # Ensure we don't swap the first node
            new_path[a], new_path[b] = new_path[b], new_path[a]
        elif move_type == "reverse":
            a, b = sorted(random.sample(range(1, l), 2))
            new_path[a:b+1] = reversed(new_path[a:b+1])
        elif move_type == "shift":
            a, b = sorted(random.sample(range(1, l), 2))
            new_path[a:b+1] = new_path[a+1:b+1] + new_path[a:a+1]

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

        # Debugging output
        if i % (num_iterations // 10) == 0:
            print(f"Iteration {i}: Current Distance = {current_distance}, Best Distance = {best_distance}")

    return best_distance, best_path

# Function to plot the paths on a graph
def plot_path(coords, path, optimized_path=None, title="Salesman Path Comparison"):
    plt.figure(figsize=(20, 8))

    if optimized_path:
        # Plot the initial NN path
        plt.subplot(1, 2, 1)
        x_initial = [coords[i].x for i in path]
        y_initial = [coords[i].y for i in path]
        plt.plot(x_initial, y_initial, marker='o', linestyle='-', linewidth=2, markersize=4, color='k')
        plt.title('Nearest Neighbor Salesman Path')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend(['Path'], loc='best')
        plt.grid(True)

        # Plot the optimized SA path
        plt.subplot(1, 2, 2)
        x_optimized = [coords[i].x for i in optimized_path]
        y_optimized = [coords[i].y for i in optimized_path]
        plt.plot(x_optimized, y_optimized, marker='o', linestyle='-', linewidth=2, markersize=4, color='k')
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
    best_sa_distance = float('inf')
    best_sa_path = []
    best_start_node = 0

    # Threshold distance for early stopping
    threshold_distance = 500  # Example value

    for start_node in range(len(coords)):
        # Nearest Neighbor algorithm
        nn_total_distance, nn_path = nearest_neighbor(coords, start_node)
        print(f"Starting Node {start_node} - Nearest Neighbor Path: {nn_path}")
        print(f"Total Distance (Nearest Neighbor): {nn_total_distance}")

        # Simulated annealing parameters
        initial_temp = 100000
        cooling_rate = 0.9995
        num_iterations = 200000

        # Perform simulated annealing starting from the nearest neighbor path
        sa_total_distance, sa_path = simulated_annealing(coords, nn_path, initial_temp, cooling_rate, num_iterations)
        print(f"Starting Node {start_node} - Simulated Annealing Path: {sa_path}")
        print(f"Total Distance (Simulated Annealing): {sa_total_distance}")

        # Update the best solution found so far
        if sa_total_distance < best_sa_distance:
            best_sa_distance = sa_total_distance
            best_sa_path = sa_path
            best_start_node = start_node

        # Early stopping if the threshold is reached
        if best_sa_distance < threshold_distance:
            print(f"Threshold distance reached with start node {start_node}. Stopping early.")
            break

    print(f"Best Starting Node: {best_start_node}")
    print("Best Simulated Annealing Path:", best_sa_path)
    print("Total Distance (Best Simulated Annealing):", best_sa_distance)

    # Plot the best paths for comparison
    nn_total_distance, nn_path = nearest_neighbor(coords, best_start_node)
    plot_path(coords, nn_path, best_sa_path)
else:
    print("Failed to read coordinates from the file.")
