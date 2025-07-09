import pulp

# Define the data
foods = ['Apple', 'Banana', 'Milk', 'Bread', 'Egg', 'Chicken', 'Rice', 'Broccoli', 'Carrot', 'Cheese', 'Peanut Butter', 'Yogurt']
costs = {'Apple': 0.5, 'Banana': 0.3, 'Milk': 0.7, 'Bread': 0.2, 'Egg': 0.2, 'Chicken': 1.5, 'Rice': 0.3, 'Broccoli': 0.4, 'Carrot': 0.2, 'Cheese': 0.8, 'Peanut Butter': 0.6, 'Yogurt': 0.5}
calories = {'Apple': 95, 'Banana': 105, 'Milk': 150, 'Bread': 80, 'Egg': 70, 'Chicken': 335, 'Rice': 206, 'Broccoli': 55, 'Carrot': 25, 'Cheese': 113, 'Peanut Butter': 188, 'Yogurt': 100}
protein = {'Apple': 0.5, 'Banana': 1.3, 'Milk': 8, 'Bread': 3, 'Egg': 6, 'Chicken': 27, 'Rice': 4.2, 'Broccoli': 3.7, 'Carrot': 0.6, 'Cheese': 7, 'Peanut Butter': 8, 'Yogurt': 10}
fat = {'Apple': 0.3, 'Banana': 0.4, 'Milk': 8, 'Bread': 1, 'Egg': 5, 'Chicken': 19, 'Rice': 0.4, 'Broccoli': 0.6, 'Carrot': 0.1, 'Cheese': 9, 'Peanut Butter': 16, 'Yogurt': 3.5}
carbs = {'Apple': 25, 'Banana': 27, 'Milk': 11, 'Bread': 15, 'Egg': 1, 'Chicken': 0, 'Rice': 45, 'Broccoli': 11, 'Carrot': 6, 'Cheese': 1, 'Peanut Butter': 6, 'Yogurt': 14}

# Define the minimum nutritional requirements
min_calories = 2000
min_protein = 50
min_fat = 70
min_carbs = 300

# Create a linear programming problem
lp_problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)

# Define decision variables
food_vars = pulp.LpVariable.dicts("Food", foods, lowBound=0, cat='Continuous')

# Objective function: Minimize the total cost
lp_problem += pulp.lpSum([costs[i] * food_vars[i] for i in foods]), "Total Cost"

# Constraints
lp_problem += pulp.lpSum([calories[i] * food_vars[i] for i in foods]) >= min_calories, "Calories"
lp_problem += pulp.lpSum([protein[i] * food_vars[i] for i in foods]) >= min_protein, "Protein"
lp_problem += pulp.lpSum([fat[i] * food_vars[i] for i in foods]) >= min_fat, "Fat"
lp_problem += pulp.lpSum([carbs[i] * food_vars[i] for i in foods]) >= min_carbs, "Carbs"

# Solve the problem
lp_problem.solve()

# Print the results
print(f"Status: {pulp.LpStatus[lp_problem.status]}")
print("Optimal food servings per day:")
for food in foods:
    print(f"{food}: {food_vars[food].varValue:.2f} servings")
print(f"Total cost: ${pulp.value(lp_problem.objective):.2f}")
