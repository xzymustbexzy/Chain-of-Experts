from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus

def netthru(cities, links, supply, demand, cost, city_capacity, link_capacity):
    prob = LpProblem("Minimum_Cost_Network_Flow", LpMinimize)

    shipping = LpVariable.dicts("Shipping", ((i, j) for i, j in links), lowBound=0, cat='Continuous')

    # Objective Function
    prob += lpSum([cost[i][j] * shipping[(i, j)] for i, j in links])

    # Constraints
    for k in cities:
        prob += (lpSum(shipping[(i, k)] for i, _ in links if k == _) + supply[k] ==
                 lpSum(shipping[(k, j)] for _, j in links if k == _) + demand[k])

        prob += lpSum(shipping[(i, k)] for i, _ in links if k == _) + supply[k] <= city_capacity[k]

    for i, j in links:
        prob += shipping[(i, j)] <= link_capacity[i][j]
    
    # Solve the problem
    prob.solve()

    if LpStatus[prob.status] == 'Optimal':
        total_cost = 0
        for i, j in links:
            total_cost += shipping[(i, j)].varValue * cost[i][j]
        return total_cost
    else:
        return None