import pulp

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
    # Create problem instance
    prob = pulp.LpProblem('ProjectAssignment', pulp.LpMinimize)

    num_people = len(supply)
    num_projects = len(demand)
    
    # Create decision variables
    assign_vars = [[pulp.LpVariable(f"person_{i}_project_{j}", lowBound=0) for j in range(num_projects)] for i in range(num_people)]
    
    # Objective (to minimize total cost)
    prob += pulp.lpSum([cost[i][j] * assign_vars[i][j] for i in range(num_people) for j in range(num_projects)])

    # Constraint 1: total number of hours assigned from each person equals its supply
    for i in range(num_people):
        prob += pulp.lpSum([assign_vars[i][j] for j in range(num_projects)]) == supply[i]
      
    # Constraint 2: total number of hours assigned to each project equals its demand
    for j in range(num_projects):
        prob += pulp.lpSum([assign_vars[i][j] for i in range(num_people)]) == demand[j]
    
    # Constraint 3: hours to be assigned from each person to each project can't exceed the limit
    for i in range(num_people):
        for j in range(num_projects):
            prob += assign_vars[i][j] <= limit[i][j]

    # Solve the problem
    prob.solve()
    
    total_cost = pulp.value(prob.objective)
    return total_cost