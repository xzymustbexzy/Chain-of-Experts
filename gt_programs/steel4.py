from pulp import *

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

    problem = LpProblem("steel4", LpMaximize)
    production_vars = LpVariable.dicts("Production", (range(len(products)), range(len(stages))), lowBound=0)
    
    # Objective function
    problem += pulp.lpSum([profit[i] * production_vars[i][j] / rate[i][j] for i in range(len(products)) for j in range(len(stages))])

    # Constraints
    for i in range(len(products)):
        problem += pulp.lpSum([production_vars[i][j] / rate[i][j] for j in range(len(stages))]) >= commit[i] 
        problem += pulp.lpSum([production_vars[i][j] / rate[i][j] for j in range(len(stages))]) <= market[i] 

    for j in range(len(stages)):
        problem += pulp.lpSum([production_vars[i][j] / rate[i][j] for i in range(len(products))]) <= avail[j]
        
    problem.solve()
    
    total_profit = value(problem.objective)
    return total_profit