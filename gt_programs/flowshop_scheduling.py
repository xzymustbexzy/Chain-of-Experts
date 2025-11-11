from pulp import LpProblem, LpMinimize, LpVariable, lpSum, PULP_CBC_CMD

def flowshop_scheduling(jobs, schedules, machines, proces_time):
    M = len(machines)  # number of machines
    S = len(schedules) # number of jobs
    
    prob = LpProblem("FlowShop_Scheduling", LpMinimize)
    
    # decision variables
    JobSchedule = LpVariable.dicts("Job_Schedule", ((j, s) for j in jobs for s in schedules), cat='Binary')
    StartTime = LpVariable.dicts("Start_Time", ((s, m) for s in schedules for m in machines), lowBound=0)
    
    # objective function
    prob += StartTime[S, M] + lpSum(proces_time[j-1][M-1] * JobSchedule[j,S] for j in jobs)
    
    # constraints
    for s in schedules:
        prob += lpSum(JobSchedule[j,s] for j in jobs) == 1

    for j in jobs:
        prob += lpSum(JobSchedule[j,s] for s in schedules) == 1

    for m in range(1, M):
        for s in schedules:
            prob += StartTime[s, m+1] >= StartTime[s, m] + lpSum(proces_time[j-1][m-1] * JobSchedule[j,s] for j in jobs)
            
    for s in range(1, S):
        for m in machines:
            prob += StartTime[s+1, m] >= StartTime[s, m] + lpSum(proces_time[j-1][m-1] * JobSchedule[j,s] for j in jobs)

    # solve the problem
    prob.solve(PULP_CBC_CMD(msg=0))

    makespan = int(prob.objective.value())  # total time to process all jobs
    
    return makespan