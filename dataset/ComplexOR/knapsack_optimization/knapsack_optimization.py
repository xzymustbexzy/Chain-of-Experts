def knapsack_optimization(item_values, item_weights, max_weight_knapsack):
    """
    Args:
        item_values: a list of integers, indicating the value of each item
        item_weights: a list of integers, indicating the weight of each item
        max_weight_knapsack: an integer, denotes the maximum weight capacity of the knapsack

    Returns:
        max_total_value: a float, denotes the maximum total value of the items in the knapsack
    """
    from gurobipy import Model, GRB, quicksum

    # Create a new Gurobi model
    m = Model()

    # Number of items
    n = len(item_values)

    # Decision variables: x[i] = 1 if item i is included in the knapsack, 0 otherwise
    x = m.addVars(n, vtype=GRB.BINARY, name="x")

    # Set the objective: maximize total value of items in the knapsack
    m.setObjective(quicksum(item_values[i] * x[i] for i in range(n)), GRB.MAXIMIZE)

    # Add the weight constraint: total weight cannot exceed max_weight_knapsack
    m.addConstr(quicksum(item_weights[i] * x[i] for i in range(n)) <= max_weight_knapsack, name="weight_constraint")

    # Optimize the model
    m.optimize()

    # Retrieve the maximum total value from the model's objective value
    max_total_value = m.objVal

    return max_total_value
