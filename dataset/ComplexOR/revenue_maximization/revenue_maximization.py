def revenue_maximization(available_seats, demand, revenue, delta):
    """
    Args:
        available_seats: List of integers, available seats for each flight leg
        demand: List of integers, estimated demand for each package
        revenue: List of integers, revenue gained for selling a unit of each package
        delta: 2D list of integers, 1 if package uses a specific flight leg, otherwise 0

    Returns:
        max_revenue: Integer, the maximum revenue that can be achieved
    """
    max_revenue = 0

    # Import Gurobi
    import gurobipy as gp
    from gurobipy import GRB

    # Create model
    m = gp.Model("Revenue_Maximization")
    m.Params.OutputFlag = 0  # Suppress Gurobi output

    # Define indices
    num_packages = len(demand)
    num_legs = len(available_seats)
    packages = range(num_packages)
    legs = range(num_legs)

    # Create variable upper bounds as a dict
    ub_dict = {i: demand[i] for i in packages}

    # Create decision variables
    x = m.addVars(packages, lb=0, ub=ub_dict, vtype=GRB.INTEGER, name="x")

    # Add capacity constraints for each flight leg
    for j in legs:
        m.addConstr(
            gp.quicksum(delta[i][j] * x[i] for i in packages) <= available_seats[j],
            name=f"Capacity_Leg_{j}"
        )

    # Set the objective to maximize revenue
    m.setObjective(
        gp.quicksum(revenue[i] * x[i] for i in packages),
        GRB.MAXIMIZE
    )

    # Optimize the model
    m.optimize()

    # Retrieve the maximum revenue
    if m.status == GRB.OPTIMAL:
        max_revenue = int(m.objVal)
    else:
        max_revenue = None

    return max_revenue
