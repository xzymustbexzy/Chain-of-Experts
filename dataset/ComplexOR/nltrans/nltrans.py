def nltrans(supply, demand, rate, limit):
    """
    Args:
        supply: a list of integers, each indicates the amount of goods available at an origin
        demand: a list of integers, each indicates the amount of goods required at a destination
        rate: a 2D list of integers, the shipment costs per unit from each origin to each destination
        limit: a 2D list of integers, the limit on units shipped from each origin to each destination

    Returns:
        total_cost: an integer, denotes the minimum total cost of shipping goods
    """
    import gurobipy as gp
    from gurobipy import GRB

    num_origins = len(supply)
    num_destinations = len(demand)

    # Create model
    m = gp.Model()

    # Create variables for units shipped from each origin to each destination
    x = m.addVars(num_origins, num_destinations, lb=0, name="x")

    # Supply constraints: total units shipped from each origin cannot exceed its supply
    m.addConstrs(
        (gp.quicksum(x[i, j] for j in range(num_destinations)) <= supply[i]
         for i in range(num_origins)),
        name="Supply"
    )

    # Demand constraints: total units received at each destination must meet its demand
    m.addConstrs(
        (gp.quicksum(x[i, j] for i in range(num_origins)) >= demand[j]
         for j in range(num_destinations)),
        name="Demand"
    )

    # Shipping limit constraints: units shipped from origin i to destination j cannot exceed limit[i][j]
    m.addConstrs(
        (x[i, j] <= limit[i][j]
         for i in range(num_origins)
         for j in range(num_destinations)),
        name="Limit"
    )

    # Objective: minimize total shipping cost
    total_cost_expr = gp.quicksum(
        rate[i][j] * x[i, j]
        for i in range(num_origins)
        for j in range(num_destinations)
    )
    m.setObjective(total_cost_expr, GRB.MINIMIZE)

    # Optimize the model
    m.optimize()

    # Retrieve the total cost
    total_cost = int(round(m.objVal))

    return total_cost
