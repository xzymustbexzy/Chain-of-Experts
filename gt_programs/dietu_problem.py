import pulp

def dietu_problem(cost, f_min, f_max, n_min, n_max, amt):
    # number of foods and nutrients
    num_foods = len(cost)
    num_nutri = len(n_min)

    # declare a linear program
    prob = pulp.LpProblem('DietProblem', pulp.LpMinimize)

    # define the decision variables
    food_vars = pulp.LpVariable.dicts("Buy", range(num_foods), f_min, f_max)

    # objective function: total cost of foods
    prob += pulp.lpSum([cost[j] * food_vars[j] for j in range(num_foods)])

    # constraints
    for i in range(num_nutri):
        prob += pulp.lpSum([amt[i][j] * food_vars[j] for j in range(num_foods)]) >= n_min[i]
        prob += pulp.lpSum([amt[i][j] * food_vars[j] for j in range(num_foods)]) <= n_max[i] 
        
    # optimize
    prob.solve()

    # total cost
    total_cost = pulp.value(prob.objective)
    return total_cost