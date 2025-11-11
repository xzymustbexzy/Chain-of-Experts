from pulp import *

def aircraft_assignment(availability, demand, capabilities, costs):
    aircraft = range(len(availability))
    routes = range(len(demand))

    prob = LpProblem("Aircraft_Assignment", LpMinimize)

    # 创建决策变量
    alloc_vars = LpVariable.dicts("Allocation",(aircraft, routes),0,None,LpInteger)

    # 设置目标函数
    prob += lpSum([costs[i][j] * alloc_vars[i][j] for i in aircraft for j in routes])

    # 添加约束：分配的飞机数不超过可用飞机数
    for i in aircraft:
        prob += lpSum([alloc_vars[i][j] for j in routes]) <= availability[i]

    # 添加约束：每个航线分配飞机满足需求
    for j in routes:
        prob += lpSum([alloc_vars[i][j] * capabilities[i][j] for i in aircraft]) >= demand[j]

    # 求解问题
    prob.solve()

    # 返回最小总成本
    min_total_cost = value(prob.objective)
    
    return min_total_cost