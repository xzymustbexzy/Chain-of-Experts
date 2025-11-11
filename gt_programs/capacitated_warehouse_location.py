from pulp import *

def capacitated_warehouse_location(Locations, Customers, Demand, AllocationCost, Capacity, FixedCost):
    prob = LpProblem("Capacitated Warehouse Location Problem", LpMinimize)

    Open = LpVariable.dicts("Open", Locations, cat='Binary')
    DemandFractionSupplied = LpVariable.dicts("DemandFractionSupplie", [(i,j) for i in Locations for j in Customers], lowBound=0)

    prob += lpSum([AllocationCost[i][j] * DemandFractionSupplied[(i,j)] for i in Locations for j in Customers]) + \
            lpSum([FixedCost[i] * Open[i] for i in Locations])

    for j in Customers:
        prob += lpSum([DemandFractionSupplied[(i,j)] for i in Locations]) >= Demand[j]

    for i in Locations:
        prob += lpSum([Demand[j] * DemandFractionSupplied[(i,j)] for j in Customers]) <= Capacity[i] * Open[i]

    prob.solve()

    return value(prob.objective)