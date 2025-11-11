from scipy.optimize import linprog

def car_selection(participants, cars, possible_assignments):
    assignments = [[0 for _ in cars] for _ in participants]

    c = [-1 for _ in range(len(participants)*len(cars))]
    A = []
    b = []

    for idx, p in enumerate(participants):
        A.append([1 if j // len(cars) == idx else 0 for j in range(len(participants)*len(cars))])
        b.append(1)

    for idx, c in enumerate(cars):
        A.append([1 if j % len(cars) == idx else 0 for j in range(len(participants)*len(cars))])
        b.append(1)

    for idx_p, p in enumerate(participants):
        for idx_c, c in enumerate(cars):
            if possible_assignments[idx_p][idx_c] == 0:
                A.append([1 if j // len(cars) == idx_p and j % len(cars) == idx_c else 0 for j in range(len(participants)*len(cars))])
                b.append(0)

    result = linprog(c, A_ub=A, b_ub=b, bounds=(0, 1), method='highs')

    total_combinations = -result.fun

    return int(total_combinations)