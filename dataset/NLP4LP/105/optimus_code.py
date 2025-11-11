# Code automatically generated from OptiMUS

# Problem type: LP
# Problem description
"""
A pharmacy operates NumFactories factories, each producing NumProducts different
products. Each factory has a ProductionRate for each product in units per hour
and requires BaseGelRequirement units of base gel per hour. The pharmacy has
AvailableBaseGel units of base gel available. The production must satisfy the
MinimumDemand for each product. The objective is to determine the number of
hours each factory should be run to minimize the total time needed.
"""
# Import necessary libraries
import json
from gurobipy import *

# Create a new model
model = Model()

# Load data
with open(
    "/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/106/parameters.json",
    "r",
) as f:
    data = json.load(f)

# @Def: definition of a target
# @Shape: shape of a target

# Parameters
# @Parameter NumFactories @Def: Number of factories @Shape: []
NumFactories = data["NumFactories"]
# @Parameter NumProducts @Def: Number of products @Shape: []
NumProducts = data["NumProducts"]
# @Parameter ProductionRate @Def: Production rate of a product by a factory in units per hour @Shape: ['NumFactories', 'NumProducts']
ProductionRate = data["ProductionRate"]
# @Parameter BaseGelRequirement @Def: Base gel required per hour by a factory @Shape: ['NumFactories']
BaseGelRequirement = data["BaseGelRequirement"]
# @Parameter AvailableBaseGel @Def: Total available units of base gel @Shape: []
AvailableBaseGel = data["AvailableBaseGel"]
# @Parameter MinimumDemand @Def: Minimum required units of each product @Shape: ['NumProducts']
MinimumDemand = data["MinimumDemand"]

# Variables
# @Variable Production @Def: The production quantity of each product by each factory @Shape: ['NumFactories', 'NumProducts']
ProductionMatrix = model.addVars(
    NumFactories, NumProducts, vtype=GRB.CONTINUOUS, name="ProductionMatrix"
)
# @Variable MaxOperatingHours @Def: The maximum operating hours across all factories @Shape: []
MaxOperatingHours = model.addVar(vtype=GRB.CONTINUOUS, name="MaxOperatingHours")

# Constraints
# @Constraint Constr_1 @Def: The production of each product by all factories combined must meet or exceed the MinimumDemand.
model.addConstrs(
    (
        quicksum(ProductionMatrix[f, p] for f in range(NumFactories))
        >= MinimumDemand[p]
        for p in range(NumProducts)
    ),
    name="Demand",
)
# @Constraint Constr_2 @Def: The total base gel required by all factories must not exceed the AvailableBaseGel.
model.addConstr(
    quicksum(
        BaseGelRequirement[i] / ProductionRate[i][p] * ProductionMatrix[i, p]
        for i in range(NumFactories)
        for p in range(NumProducts)
    )
    <= AvailableBaseGel
)

# Objective
# @Objective Objective @Def: The objective is to minimize the maximum operating hours across all factories while meeting production requirements and adhering to base gel resource constraints.
model.setObjective(MaxOperatingHours, GRB.MINIMIZE)

# Solve
model.optimize()

# Extract solution
solution = {}
variables = {}
objective = []
variables["ProductionMatrix"] = {
    f"({k[0]}, {k[1]})": v.x for k, v in ProductionMatrix.items()
}
variables["MaxOperatingHours"] = MaxOperatingHours.x
solution["variables"] = variables
solution["objective"] = model.objVal
with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
