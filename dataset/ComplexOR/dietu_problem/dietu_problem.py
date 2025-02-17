def dietu_problem(cost, f_min, f_max, n_min, n_max, amt):
    """
    Args:
        cost: list of costs for each food item, length is the number of foods
        f_min: list of minimum amounts to buy for each food item, length is the number of foods
        f_max: list of maximum amounts to buy for each food item, length is the number of foods
        n_min: list of minimum nutrient requirements, length is the number of nutrients
        n_max: list of maximum nutrient requirements, length is the number of nutrients
        amt: 2D list where amt[i][j] is the amount of nutrient i in food j, dimensions are nutrients x foods

    Returns:
        total_cost: the minimal total cost to meet the diet requirements
    """
    from gurobipy import Model, GRB, quicksum

    # Initialize the model
    model = Model('diet_problem')
    model.setParam('OutputFlag', 0)  # Disable solver output

    num_foods = len(cost)
    num_nutrients = len(n_min)

    foods = range(num_foods)
    nutrients = range(num_nutrients)

    # Create dictionaries for variables and parameters
    f_min_dict = {j: f_min[j] for j in foods}
    f_max_dict = {j: f_max[j] for j in foods}
    cost_dict = {j: cost[j] for j in foods}

    # Create decision variables x_j
    x = model.addVars(foods, lb=f_min_dict, ub=f_max_dict, obj=cost_dict, name='x')

    # Set the objective to minimize total cost
    model.ModelSense = GRB.MINIMIZE

    # Add nutrient constraints
    for i in nutrients:
        expr = quicksum(amt[i][j] * x[j] for j in foods)
        # Minimum requirement constraint
        model.addConstr(expr >= n_min[i], name='n_min[%d]' % i)
        # Maximum requirement constraint
        model.addConstr(expr <= n_max[i], name='n_max[%d]' % i)

    # Optimize the model
    model.optimize()

    # Check if the model has an optimal solution
    if model.Status == GRB.OPTIMAL:
        total_cost = model.ObjVal
    else:
        total_cost = None  # Handle infeasibility or other statuses as needed

    return total_cost
