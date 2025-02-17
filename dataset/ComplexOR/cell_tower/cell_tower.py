def cell_tower(delta, cost, population, budget):
    """
    Args:
        delta: A matrix (list of lists) where delta[i][j] is 1 if site `i` covers region `j`, otherwise 0
        cost: A list where cost[i] is the cost of building the tower at site `i`
        population: A list where population[j] is the population of region `j`
        budget: An integer, the total budget allowed for building the towers

    Returns:
        total_population_covered: An integer indicating the maximum population covered within the given budget
    """
    import gurobipy as gp
    from gurobipy import GRB

    # Number of potential tower sites and regions
    num_sites = len(cost)
    num_regions = len(population)

    # Create a new model
    m = gp.Model("cell_tower_coverage")

    # Decision variables: x[i] is 1 if we build a tower at site i, 0 otherwise
    x = m.addVars(num_sites, vtype=GRB.BINARY, name="x")

    # Decision variables: y[j] is 1 if region j is covered, 0 otherwise
    y = m.addVars(num_regions, vtype=GRB.BINARY, name="y")

    # Budget constraint: sum of cost of selected sites should not exceed the budget
    m.addConstr(gp.quicksum(cost[i] * x[i] for i in range(num_sites)) <= budget, name="Budget")

    # Coverage constraints: a region is covered if at least one of its covering sites is selected
    for j in range(num_regions):
        m.addConstr(
            y[j] <= gp.quicksum(delta[i][j] * x[i] for i in range(num_sites)),
            name=f"Coverage_{j}"
        )

    # Objective: maximize the total population covered
    m.setObjective(gp.quicksum(population[j] * y[j] for j in range(num_regions)), GRB.MAXIMIZE)

    # Optimize the model
    m.optimize()

    # Retrieve the total population covered
    if m.status == GRB.OPTIMAL:
        total_population_covered = int(m.objVal)
    else:
        total_population_covered = 0

    return total_population_covered
