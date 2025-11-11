def employee_assignment(restaurants, employees, shifts, skills, demand, employee_has_skill, employee_skill_preference, 
                        employee_does_shift, unfulfilled_weighting_factor):
    """
    Args:
        restaurants: list of strings, represents the set of restaurants.
        employees: list of integers, represents the set of employees.
        shifts: list of strings, represents the set of shifts.
        skills: list of strings, represents the set of skills.
        demand: 3D list of integers, demand[r][sh][sk] denotes the needed number of employees with skill 'sk' in shift 'sh' in restaurant 'r'.
        employee_has_skill: 2D list of integers, employee_has_skill[e][sk] indicates if employee 'e' has skill 'sk'.
        employee_skill_preference: 2D list of floats, employee_skill_preference[e][sk] denotes the job preference of the employees (lower number means preferred position).
        employee_does_shift: 2D list of integers, employee_does_shift[e][sh] denotes the availability of employee 'e' for shift 'sh'.
        unfulfilled_weighting_factor: float, the cost factor of an unfulfilled position.

    Returns:
        total_cost: float, the minimized total cost of the schedule.
    """
    # To be implemented
    total_cost = 0.0
    return total_cost