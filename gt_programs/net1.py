import pulp

def net1(Cities, Links, Supply, Demand, ShippingCost, Capacity):
    prob = pulp.LpProblem("Network_Flow_Problem", pulp.LpMinimize)

    Ship = pulp.LpVariable.dicts("ship", (Cities, Cities), lowBound=0, cat='Integer')

    prob += pulp.lpSum([ShippingCost[i][j] * Ship[i][j] for i in Cities for j in Cities])

    for k in Cities:
        prob += pulp.lpSum([Ship[i][k] for (i, j) in Links if j == k]) + \
                Supply[k] == Demand[k] + pulp.lpSum([Ship[k][j] for (i, j) in Links if i == k])
    for (i, j) in Links:
        prob += Ship[i][j] <= Capacity[i][j]
    
    prob.solve()

    total_cost = pulp.value(prob.objective)
    return total_cost