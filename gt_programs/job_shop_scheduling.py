from gurobipy import Model, GRB, quicksum

def job_shop_scheduling(tasks, machines, processing_time, delta, big_m):
    # Create a new model
    model = Model("job_shop_scheduling")

    # Map task labels to indices
    task_indices = {task: idx for idx, task in enumerate(tasks)}

    # Decision variables
    start_time = model.addVars(tasks, machines, vtype=GRB.CONTINUOUS, name="StartTime")
    done_before = model.addVars(tasks, tasks, machines, vtype=GRB.BINARY, name="DoneBefore")
    finish_time_on_machine = model.addVars(machines, vtype=GRB.CONTINUOUS, name="FinishTimeOnMachine")
    max_finish_time = model.addVar(vtype=GRB.CONTINUOUS, name="MaxFinishTime")

    # Objective: Minimize the maximum finish time across all machines
    model.setObjective(max_finish_time, GRB.MINIMIZE)

    # Constraints

    # Constraint 1: The latest finish time over machines
    model.addConstrs((finish_time_on_machine[m] <= max_finish_time for m in machines), "MaxFinishTimeConstraint")

    # Constraint 2: The completion time of the last task on each machine
    model.addConstrs((start_time[task, m] + processing_time[task_indices[task]][m] <= finish_time_on_machine[m]
                      for task in tasks for m in machines), "CompletionTimeConstraint")

    # Constraint 3: Logical constraint on the start times for a task (sequence dependency)
    model.addConstrs((start_time[task, m] + processing_time[task_indices[task]][m] <= -big_m * delta[task_indices[task]][n][m] + big_m + start_time[task, n]
                      for task in tasks for m in machines for n in machines if m != n), "SequenceDependencyConstraint")

    # Constraint 4: Avoid task overlap on each machine
    model.addConstrs((start_time[i, m] + processing_time[task_indices[i]][m] <= -big_m * done_before[i, j, m] + big_m + start_time[j, m]
                      for i in tasks for j in tasks for m in machines if i != j), "NoOverlapConstraint")

    # Optimize the model
    model.optimize()

    # Check if a solution is found
    if model.status == GRB.OPTIMAL:
        min_makespan = model.objVal
        # Optional: Retrieve start times for each task on each machine
        task_start_times = { (task, m): start_time[task, m].X for task in tasks for m in machines }
        print("Optimal Schedule Start Times:", task_start_times)
    else:
        min_makespan = None
        print("No optimal solution found.")

    return min_makespan
