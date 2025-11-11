from pulp import *

def fleet_routing(locations, planes, periods, capacity, cost, available_planes, delta, number_of_passengers):
    prob = LpProblem("Fleet_Routing_Problem", LpMinimize)
    
    NumPlanes = LpVariable.dicts("NumPlanes", (planes, locations, periods, locations, periods), 0, None, LpInteger)
    NumIdlePlanes = LpVariable.dicts("NumIdlePlanes", (planes, locations, periods), 0, None, LpInteger)
    NumIdlePlanesInit = LpVariable.dicts("NumIdlePlanesInit", (planes, locations), 0, None, LpInteger)

    prob += lpSum([cost[v] * NumPlanes[v][i][t][j][h] 
                   for v in planes for i in locations for t in periods 
                   for j in locations for h in periods]), "Total Cost"

    for v in planes:
        for i in locations:
            prob += NumIdlePlanesInit[v][i] == (
                NumIdlePlanes[v][i][1] + 
                lpSum([NumPlanes[v][i][1][j][h] for j in locations for h in periods if delta[i][1][j][h] == 1])
            ), "Initial_Flow_Balance_{}_{}".format(v, i)
    
    for v in planes:
        for i in locations:
            for t in periods:
                if t > 1:
                    prob += NumIdlePlanes[v][i][t] == (
                        NumIdlePlanes[v][i][t-1] + 
                        lpSum([NumPlanes[v][j][p][i][t] for j in locations for p in periods if delta[j][p][i][t] == 1]) -
                        lpSum([NumPlanes[v][i][t][j][h] for j in locations for h in periods if delta[i][t][j][h] == 1])
                    ), "Flow_Balance_{}_{}_{}".format(v, i, t)

    for v in planes:
        prob += lpSum([NumIdlePlanesInit[v][i] for i in locations]) <= available_planes[v], "Available_Planes_{}".format(v)

    for i in locations:
        for t in periods:
            for j in locations:
                for h in periods:
                    if delta[i][t][j][h] == 1:
                        prob += lpSum([capacity[v] * NumPlanes[v][i][t][j][h] for v in planes]) >= number_of_passengers[i][t][j][h], \
                        "Capacity_Flight_{}_{}_{}_{}".format(i, t, j, h)
    
    for v in planes:
        for i in locations:
            for t in periods:
                for j in locations:
                    for h in periods:
                        prob += NumPlanes[v][i][t][j][h] <= available_planes[v] * delta[i][t][j][h], \
                        "Flight_Plan_{}_{}_{}_{}_{}".format(v, i, t, j, h)

    prob.solve()

    total_cost = value(prob.objective)

    return total_cost