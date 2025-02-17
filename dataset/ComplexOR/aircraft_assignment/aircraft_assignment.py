def aircraft_assignment(availability, demand, capabilities, costs):
    """
    Args:
        availability: list, availability of each aircraft
        demand: list, demand for each route
        capabilities: 2D list, capabilities of each aircraft for each route
        costs: 2D list, costs of assigning each aircraft to each route

    Returns:
        min_total_cost: float, the minimum total cost of the assignment
    """
    import gurobipy as gp
    from gurobipy import GRB

    num_aircraft = len(availability)
    num_routes = len(demand)

    # Create the model
    model = gp.Model("Aircraft Assignment Problem")

    # Decision variables: number of aircraft of type i assigned to route j
    x = model.addVars(num_aircraft, num_routes, vtype=GRB.INTEGER, name="x")

    # Objective function: minimize total cost
    model.setObjective(
        gp.quicksum(costs[i][j] * x[i, j] for i in range(num_aircraft) for j in range(num_routes)),
        GRB.MINIMIZE
    )

    # Availability constraints: number of aircraft assigned does not exceed availability
    for i in range(num_aircraft):
        model.addConstr(
            gp.quicksum(x[i, j] for j in range(num_routes)) <= availability[i],
            name=f"availability_{i}"
        )

    # Demand constraints: total capacity on each route meets or exceeds demand
    for j in range(num_routes):
        model.addConstr(
            gp.quicksum(capabilities[i][j] * x[i, j] for i in range(num_aircraft)) >= demand[j],
            name=f"demand_{j}"
        )

    # Optimize the model
    model.optimize()

    # Retrieve the optimal objective value
    if model.status == GRB.OPTIMAL:
        min_total_cost = model.objVal
    else:
        min_total_cost = None

    return min_total_cost
