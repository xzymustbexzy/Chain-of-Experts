def netasgn(supply, demand, cost, limit):
    """
    Args:
        supply: list, hours each person is available, length is number of people
        demand: list, hours each project requires, length is number of projects
        cost: 2D list, cost per hour of work for each person on each project, dimensions are number of people x number of projects
        limit: 2D list, maximum contributions to projects for each person on each project, dimensions are number of people x number of projects

    Returns:
        total_cost: a float, denotes the minimized total cost of assigning people to projects
    """
    # Import gurobipy
    import gurobipy as gp
    from gurobipy import GRB

    # Create indices for people and projects
    num_people = len(supply)
    num_projects = len(demand)
    people = range(num_people)
    projects = range(num_projects)

    # Create the model
    model = gp.Model('net_assignment')

    # Define variables x_{i,j} with bounds [0, Limit_{i,j}] and cost coefficients
    x = {}
    for i in people:
        for j in projects:
            x[i, j] = model.addVar(lb=0, ub=limit[i][j], obj=cost[i][j], vtype=GRB.CONTINUOUS, name=f"x_{i}_{j}")

    # Update the model to integrate the variables
    model.update()

    # Add supply constraints: sum of hours assigned from each person equals their available supply
    for i in people:
        model.addConstr(gp.quicksum(x[i, j] for j in projects) == supply[i], name=f"Supply_{i}")

    # Add demand constraints: sum of hours assigned to each project equals its required demand
    for j in projects:
        model.addConstr(gp.quicksum(x[i, j] for i in people) == demand[j], name=f"Demand_{j}")

    # Optimize the model
    model.optimize()

    # Retrieve the minimized total cost
    if model.status == GRB.OPTIMAL:
        total_cost = model.objVal
    else:
        total_cost = None

    return total_cost
