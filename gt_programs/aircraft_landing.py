from pulp import *

def aircraft_landing(EarliestLanding, LatestLanding, TargetLanding,
                     PenaltyAfterTarget, PenaltyBeforeTarget, SeparationTime):
    # 数量的飞机
    num_aircrafts = len(EarliestLanding)
    aircrafts = list(range(num_aircrafts))

    # 创建优化问题
    prob = LpProblem("Aircraft_Landing_Problem", LpMinimize)

    # 决策变量
    Landing = LpVariable.dicts("Landing", aircrafts, lowBound=0, cat='Continuous')
    Early = LpVariable.dicts("Early", aircrafts, lowBound=0, cat='Continuous')
    Late = LpVariable.dicts("Late", aircrafts, lowBound=0, cat='Continuous')
    AircraftsOrder = LpVariable.dicts("Aircraft_Order", (aircrafts, aircrafts), 
                                      cat='Binary')

    # 目标函数(最小化总罚金)
    prob += lpSum([PenaltyBeforeTarget[i] * Early[i] + PenaltyAfterTarget[i] * Late[i]
                   for i in aircrafts])

    # 约束条件
    # 1. 飞机着陆顺序约束
    for i in aircrafts:
        for j in aircrafts:
            if i != j:
                prob += AircraftsOrder[i][j] + AircraftsOrder[j][i] == 1

    # 2. 着陆间隔约束
    for i in aircrafts:
        for j in aircrafts:
            if i != j:
                prob += Landing[j] >= Landing[i] + SeparationTime[i][j] * AircraftsOrder[i][j] - (LatestLanding[i] - EarliestLanding[j]) * (1 - AircraftsOrder[i][j])

    # 3. 最早着陆时间约束
    for i in aircrafts:
        prob += Landing[i] >= EarliestLanding[i]

    # 4. 最晚着陆时间约束
    for i in aircrafts:
        prob += Landing[i] <= LatestLanding[i]

    # 5. 提前着陆时间约束
    for i in aircrafts:
        prob += Early[i] >= TargetLanding[i] - Landing[i]

    # 6. 延后着陆时间约束
    for i in aircrafts:
        prob += Late[i] >= Landing[i] - TargetLanding[i]

    # 解决问题
    prob.solve()

    # 输出最终结果
    min_total_penalty = value(prob.objective)

    # 打印每个飞机的着陆时间
    for i in aircrafts:
        print(f"Aircraft {i} landing at {value(Landing[i])}")

    return min_total_penalty

