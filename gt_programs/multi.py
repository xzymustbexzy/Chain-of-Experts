import pulp

def multi(supply, demand, limit, cost):

    prob = pulp.LpProblem("Multi-Commodity_Transportation_Problem", pulp.LpMinimize)

    origins = range(len(supply))
    destinations = range(len(demand[0]))
    products = range(len(supply[0]))

    transport = pulp.LpVariable.dicts("Transport", (origins, destinations, products), 0, None, pulp.LpInteger)

    prob += pulp.lpSum([cost[i][j][p] * transport[i][j][p] for i in origins for j in destinations for p in products]), "Total Shipment Costs"

    for i in origins:
        for p in products:
            prob += pulp.lpSum([transport[i][j][p] for j in destinations]) == supply[i][p], f"Supply_Constraint_{i}_{p}"
    
    for j in destinations:
        for p in products:
            prob += pulp.lpSum([transport[i][j][p] for i in origins]) == demand[p][j], f"Demand_Constraint_{j}_{p}"
    
    for i in origins:
        for j in destinations:
            prob += pulp.lpSum([transport[i][j][p] for p in products]) <= limit[i][j], f"Limit_Constraint_{i}_{j}"
    
    prob.solve()
    
    total_cost = pulp.value(prob.objective)

    transport_values = {}
    for i in origins:
        for j in destinations:
            for p in products:
                transport_values[i, j, p] = pulp.value(transport[i][j][p])

    return total_cost, transport_values

