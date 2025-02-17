def multi(supply, demand, limit, cost):
    """
    Args:
        supply: a 2D list, supply[i][p] indicates the amount of product p available at origin i
        demand: a 2D list, demand[p][j] indicates the amount of product p required at destination j
        limit: a 2D list, limit[i][j] indicates the maximum total amount of all products that can be shipped from origin i to destination j
        cost: a 3D list, cost[i][j][p] indicates the shipment cost per unit of product p from origin i to destination j

    Returns:
        total_cost: a float, the minimized total cost of shipping all products
    """
    from gurobipy import Model, GRB, quicksum

    # Indices
    Origins = range(len(supply))               # Origins i
    Products = range(len(supply[0]))           # Products p
    Destinations = range(len(demand[0]))       # Destinations j

    # Create a new model
    model = Model('MultiCommodityTransportation')

    # Variables: x[i,j,p] is the amount of product p shipped from origin i to destination j
    x = {}
    for i in Origins:
        for j in Destinations:
            for p in Products:
                x[i, j, p] = model.addVar(name=f"x_{i}_{j}_{p}", lb=0)

    # Objective: Minimize total shipping cost
    model.setObjective(
        quicksum(x[i, j, p] * cost[i][j][p] for i in Origins for j in Destinations for p in Products),
        GRB.MINIMIZE
    )

    # Constraints

    # Supply constraints: The total amount of each product shipped from each origin cannot exceed its supply
    for i in Origins:
        for p in Products:
            model.addConstr(
                quicksum(x[i, j, p] for j in Destinations) <= supply[i][p],
                name=f"Supply_{i}_{p}"
            )

    # Demand constraints: The total amount of each product shipped to each destination must satisfy its demand
    for p in Products:
        for j in Destinations:
            model.addConstr(
                quicksum(x[i, j, p] for i in Origins) == demand[p][j],
                name=f"Demand_{p}_{j}"
            )

    # Limit constraints: The total amount of all products shipped from each origin to each destination cannot exceed the limit
    for i in Origins:
        for j in Destinations:
            model.addConstr(
                quicksum(x[i, j, p] for p in Products) <= limit[i][j],
                name=f"Limit_{i}_{j}"
            )

    # Optimize the model
    model.optimize()

    # Retrieve the minimized total cost
    total_cost = model.objVal

    return total_cost
