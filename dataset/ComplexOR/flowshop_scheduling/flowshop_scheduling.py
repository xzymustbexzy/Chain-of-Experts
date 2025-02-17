def flowshop_scheduling(jobs, schedules, machines, proces_time):
    """
    Args:
        jobs: list of ints, represents a set of all Jobs
        schedules: list of ints, represents a set of all schedules, range [1, S]
        machines: list of ints, represents a set of all machines, range [1, M]
        proces_time: 2D list of ints, time required to process job `j` on machine `m`, domain size [Jobs x Machines]

    Returns:
        makespan: an integer, the minimized total time to process all jobs on all machines (makespan)
    """
    import gurobipy as gp
    from gurobipy import GRB

    try:
        # Create a new model
        model = gp.Model('flowshop_scheduling')

        # Indices
        J = jobs  # list of all jobs
        M = machines  # list of all machines

        # Parameters
        p = {(j, m): proces_time[j][m] for j in J for m in M}  # processing times

        # Big M value for constraints
        big_M = 1e6

        # Decision variables
        # Start times of jobs on machines
        S = model.addVars(J, M, vtype=GRB.CONTINUOUS, name='S')

        # Completion times of jobs on machines
        C = model.addVars(J, M, vtype=GRB.CONTINUOUS, name='C')

        # Sequencing variables between jobs
        y = model.addVars(J, J, vtype=GRB.BINARY, name='y')

        # Objective: minimize makespan
        makespan = model.addVar(vtype=GRB.CONTINUOUS, name='makespan')
        model.setObjective(makespan, GRB.MINIMIZE)

        # Constraints:

        # Completion time constraints
        for j in J:
            for m in M:
                model.addConstr(C[j, m] == S[j, m] + p[j, m], name=f'completion_time_{j}_{m}')

        # Makespan constraints
        for j in J:
            model.addConstr(makespan >= C[j, M[-1]], name=f'makespan_constr_{j}')

        # Flow constraints: job cannot start on the next machine before it finishes on the current machine
        for j in J:
            for idx, m in enumerate(M):
                if idx > 0:
                    prev_m = M[idx - 1]
                    model.addConstr(S[j, m] >= C[j, prev_m], name=f'flow_constr_{j}_{m}')

        # Disjunctive constraints: jobs cannot overlap on the same machine
        for m in M:
            for i in J:
                for j in J:
                    if i != j:
                        # Sequencing constraints
                        model.addConstr(
                            S[i, m] + p[i, m] <= S[j, m] + big_M * (1 - y[i, j]),
                            name=f'seq_constr1_{i}_{j}_{m}'
                        )
                        model.addConstr(
                            S[j, m] + p[j, m] <= S[i, m] + big_M * y[i, j],
                            name=f'seq_constr2_{i}_{j}_{m}'
                        )

        # Sequencing variable constraints: one job precedes another or vice versa
        for i in J:
            for j in J:
                if i != j:
                    model.addConstr(y[i, j] + y[j, i] == 1, name=f'seq_sum_{i}_{j}')

        # Optimize the model
        model.optimize()

        # Retrieve the minimized makespan
        makespan_value = model.getObjective().getValue()

        return int(makespan_value)

    except gp.GurobiError as e:
        print(f'Gurobi error: {e}')
        return None
    except Exception as e:
        print(f'Error: {e}')
        return None
