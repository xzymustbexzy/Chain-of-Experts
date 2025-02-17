def blend_problem(alloys_on_market, required_elements, composition_data, desired_blend_percentage, alloy_price):
    """
    Args:
        alloys_on_market: list of integers, IDs of available alloys on the market
        required_elements: list of strings, IDs of required elements
        composition_data: 2D list of floats, percentage of each required element in each alloy
        desired_blend_percentage: list of floats, desired blend percentage for each element
        alloy_price: list of floats, price of each alloy

    Returns:
        min_cost: a float, minimum total cost to achieve the desired blend
    """
    import gurobipy as gp
    from gurobipy import GRB

    # Create a new model
    model = gp.Model()

    # Number of alloys and elements
    num_alloys = len(alloys_on_market)
    num_elements = len(required_elements)

    # Decision variables: Amount of each alloy to purchase
    # x[j]: amount of alloy j to purchase
    x = model.addVars(num_alloys, lb=0, name="x")

    # Set objective: Minimize total cost of alloys purchased
    total_cost = gp.quicksum(alloy_price[j] * x[j] for j in range(num_alloys))
    model.setObjective(total_cost, GRB.MINIMIZE)

    # Constraints:

    # 1. Desired blend percentage of each required element is met
    # For each required element i, ensure that the sum over all alloys of
    # (element percentage in alloy j) * (amount of alloy j purchased) equals
    # the desired blend percentage for element i
    for i in range(num_elements):
        model.addConstr(
            gp.quicksum(composition_data[i][j] * x[j] for j in range(num_alloys)) == desired_blend_percentage[i],
            name=f"ElementBalance_{required_elements[i]}"
        )

    # 2. Total amount of alloys purchased equals 1
    model.addConstr(
        gp.quicksum(x[j] for j in range(num_alloys)) == 1,
        name="TotalAlloyAmount"
    )

    # Optimize the model
    model.optimize()

    # Retrieve the minimum total cost
    if model.Status == GRB.OPTIMAL:
        min_cost = model.ObjVal
    else:
        # Handle infeasible or unbounded cases
        min_cost = float('inf')

    return min_cost
