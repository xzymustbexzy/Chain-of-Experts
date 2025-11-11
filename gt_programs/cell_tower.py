from scipy.optimize import linprog

def cell_tower(delta, cost, population, budget):
    num_towers = len(cost)
    num_regions = len(population)

    # Create objective function coefficients: negative population values 
    # because linprog method minimizes the objective function
    c = [-population[j] for j in range(num_regions)] + [0 for i in range(num_towers)]
    
    # Construct inequality constraints matrix and upper bounds
    A = []
    b = []
    
    # Add constraints for region coverage
    for j in range(num_regions):
        A_row = [0 for _ in range(num_regions)]
        A_row[j] = -1
        A_row += delta[j]
        A.append(A_row)
        b.append(0)

    # Add constraint for budget
    A_row = [0 for _ in range(num_regions)] + cost
    A.append(A_row)
    b.append(budget)

    # Add additional constraint that build decision vars should be less than or equal to covered decision vars
    for i in range(num_towers):
        A_row = [0 for _ in range(num_regions + num_towers)]
        for j in range(num_regions):
           A_row[j] = delta[i][j]
        A_row[num_regions + i] = -1
        A.append(A_row)
        b.append(0)
    
    # Variables bounds: all variables are greater than or equal to zero and less than or equal to one
    x0_bounds = (0, 1)
    bounds = [x0_bounds for _ in range(num_regions + num_towers)]
    
    # Solve the linear programming problem
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    # Calculate total population covered
    total_population_covered = sum(res.x[i] * population[i] for i in range(num_regions))
    
    return total_population_covered