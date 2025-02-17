def steel4(products, stages, rate, profit, commit, market, avail):
    """
    Args:
        products: list of products
        stages: list of stages
        rate: 2D list indicating the production rate of each product at each stage
        profit: list indicating profit per ton for each product
        commit: list indicating minimum production (lower limit) for each product
        market: list indicating maximum production (upper limit) for each product
        avail: list indicating hours available per week at each stage

    Returns:
        total_profit: float, the maximum total profit
    """
    from gurobipy import Model, GRB

    # Create a new model
    m = Model()

    # Decision variables: Tons to produce for each product
    x = {}
    for i, p in enumerate(products):
        x[p] = m.addVar(lb=commit[i], ub=market[i], name=f"x_{p}")

    # Set the objective: Maximize total profit
    m.setObjective(
        sum(profit[i] * x[products[i]] for i in range(len(products))),
        GRB.MAXIMIZE
    )

    # Add constraints: Time available at each stage should not be exceeded
    for j, s in enumerate(stages):
        m.addConstr(
            sum(
                x[products[i]] / rate[i][j] if rate[i][j] > 0 else 0
                for i in range(len(products))
            ) <= avail[j],
            name=f"Stage_{s}_Time"
        )

    # Optimize the model
    m.optimize()

    # Retrieve the total profit
    total_profit = m.objVal

    return total_profit
