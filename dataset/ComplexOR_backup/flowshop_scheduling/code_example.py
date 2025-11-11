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
    makespan = 0
    return makespan