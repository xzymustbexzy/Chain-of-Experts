def car_selection(participants, cars, possible_assignments):
    """
    Args:
        participants: list, the set of all participants.
        cars: list, the set of all cars.
        possible_assignments: 2D list, PossibleAssignments[i][j] indicates whether participant i is interested in car j.

    Returns:
        total_combinations: an integer, denotes the total number of assignments after optimization.
    """
    import gurobipy as gp
    from gurobipy import GRB

    # Initialize model
    model = gp.Model()

    n = len(participants)
    m = len(cars)

    # Create variables
    x = {}
    for i in range(n):
        for j in range(m):
            if possible_assignments[i][j]:
                x[i, j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

    # Set objective: maximize total number of assignments
    model.setObjective(gp.quicksum(x[i, j] for (i, j) in x), GRB.MAXIMIZE)

    # Add constraints
    # Each participant is assigned to at most one car
    for i in range(n):
        model.addConstr(
            gp.quicksum(x[i, j] for j in range(m) if (i, j) in x) <= 1,
            name=f"participant_{i}",
        )

    # Each car is assigned to at most one participant
    for j in range(m):
        model.addConstr(
            gp.quicksum(x[i, j] for i in range(n) if (i, j) in x) <= 1,
            name=f"car_{j}",
        )

    # Optimize the model
    model.optimize()

    # Extract the total number of assignments
    if model.status == GRB.OPTIMAL:
        total_combinations = int(model.objVal)
    else:
        total_combinations = 0

    return total_combinations
