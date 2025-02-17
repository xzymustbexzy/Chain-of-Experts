def diet_problem(food_set, nutrient_set, food_cost, min_food_amount, max_food_amount, min_nutrient_amount, max_nutrient_amount, nutrient_amount):
    """
    Args:
        food_set: List of strings, each representing a type of food.
        nutrient_set: List of strings, each representing a type of nutrient.
        food_cost: List of floats, cost of each type of food, indexed by food_set.
        min_food_amount: List of floats, minimum amount we can buy for each type of food, indexed by food_set.
        max_food_amount: List of floats, maximum amount we can buy for each type of food, indexed by food_set.
        min_nutrient_amount: List of floats, minimum required amount for each type of nutrient, indexed by nutrient_set.
        max_nutrient_amount: List of floats, maximum allowed amount for each type of nutrient, indexed by nutrient_set.
        nutrient_amount: 2D list of floats, nutrient content in each type of food, indexed by [food_set][nutrient_set].
        
    Returns:
        total_cost: The minimized total cost to satisfy the nutrient requirements.
    """
    import gurobipy as gp
    from gurobipy import GRB

    # Create a new model
    model = gp.Model('diet_problem')

    # Create variables for the amount of each food to buy
    amount_vars = {}
    for idx, food in enumerate(food_set):
        amount_vars[food] = model.addVar(lb=min_food_amount[idx], ub=max_food_amount[idx], name=food)

    # Set the objective to minimize total cost
    model.setObjective(
        gp.quicksum(food_cost[idx] * amount_vars[food] for idx, food in enumerate(food_set)),
        GRB.MINIMIZE
    )

    # Add constraints for each nutrient
    for n_idx, nutrient in enumerate(nutrient_set):
        nutrient_amount_total = gp.quicksum(
            nutrient_amount[f_idx][n_idx] * amount_vars[food]
            for f_idx, food in enumerate(food_set)
        )
        # Add minimum nutrient amount constraint
        model.addConstr(
            nutrient_amount_total >= min_nutrient_amount[n_idx],
            name=f"min_{nutrient}"
        )
        # Add maximum nutrient amount constraint
        model.addConstr(
            nutrient_amount_total <= max_nutrient_amount[n_idx],
            name=f"max_{nutrient}"
        )

    # Optimize the model
    model.optimize()

    # Retrieve the minimized total cost
    total_cost = model.ObjVal
    return total_cost
