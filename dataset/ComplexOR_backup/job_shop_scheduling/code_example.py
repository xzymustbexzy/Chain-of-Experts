def job_shop_scheduling(tasks, machines, processing_time, delta, big_m):
    """
    Args:
        tasks: List of tasks
        machines: List of machines
        processing_time: 2D list, processing_time[j][m] represents the processing time of task j on machine m
        delta: 3D list, delta[i][n][m] is a binary parameter indicating if task i should move from machine m to machine n
        big_m: A large constant used for the linearization of logical constraints

    Returns:
        min_makespan: Float, the minimum makespan which is the optimized maximum finish time of all tasks
    """
    # To be implemented
    min_makespan = 0.0
    return min_makespan