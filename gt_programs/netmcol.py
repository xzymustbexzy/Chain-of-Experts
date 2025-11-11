from pulp import *

def netmcol(Cities, Links, Products, Supply, Demand, ShipmentCost, Capacity, JointCapacity):
    prob = LpProblem("Multi-commodity Transportation Problem", LpMinimize)
    
    Ship = LpVariable.dicts("Ship", (Cities, Cities, Products), 0, cat='Continuous')

    cost = lpSum(ShipmentCost[i][j][p] * Ship[i][j][p] for i,j in Links for p in Products)
    prob += cost 
    
    for k in Cities:
        for p in Products:
            inflow = lpSum(Ship[i][k][p] for i,_ in Links if _==k)
            outflow = lpSum(Ship[k][j][p] for _,j in Links if _==k)
            prob += (Supply[k][p] + inflow == Demand[k][p] + outflow)
    
    for i,j in Links:
        prob += lpSum(Ship[i][j][p] for p in Products) <= JointCapacity[i][j]
                
    for i,j in Links:
        for p in Products:
            prob += Ship[i][j][p] <= Capacity[i][j][p]

    status = prob.solve()

    total_cost = value(prob.objective)
    return total_cost