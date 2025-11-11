import cvxpy as cp

def diet_problem(food_set, nutrient_set, food_cost, min_food_amount, max_food_amount, min_nutrient_amount, max_nutrient_amount, nutrient_amount):
    n_food = len(food_set)
    n_nutrient = len(nutrient_set)
    
    Buy = cp.Variable(n_food)
    
    cost = cp.sum(cp.multiply(food_cost, Buy))
    objective = cp.Minimize(cost)
    
    constraints = []
    for i in range(n_food):
        constraints.append(Buy[i]>=min_food_amount[i])
        constraints.append(Buy[i]<=max_food_amount[i])
    for i in range(n_nutrient):
        total_nutrient = cp.sum([Buy[j]*nutrient_amount[j][i] for j in range(n_food)])
        constraints.append(total_nutrient>=min_nutrient_amount[i])
        constraints.append(total_nutrient<=max_nutrient_amount[i])
        
    problem = cp.Problem(objective, constraints)
    total_cost = problem.solve()
    
    if problem.status != "optimal":
        return None

    return total_cost

