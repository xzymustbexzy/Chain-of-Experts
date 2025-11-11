# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A pharmacy produces NumProducts different products using NumMachines different
machines. Each machine m can produce ProductionRate[m, p] amount of product p
per hour. Additionally, machine m consumes WaterUsage[m] amount of distilled
water per hour. The pharmacy has TotalWaterAvailable amount of distilled water
available. The pharmacy needs to produce at least RequiredProduct[p] amount of
each product p. The objective is to determine the number of hours each machine
should be operated to minimize the total time required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/116/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumMachines @Def: Number of machines @Shape: [] 
NumMachines = data['NumMachines']
# @Parameter NumProducts @Def: Number of products @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter ProductionRate @Def: Amount of product p produced per hour by machine m @Shape: ['NumMachines', 'NumProducts'] 
ProductionRate = data['ProductionRate']
# @Parameter WaterUsage @Def: Amount of distilled water consumed per hour by machine m @Shape: ['NumMachines'] 
WaterUsage = data['WaterUsage']
# @Parameter TotalWaterAvailable @Def: Total amount of distilled water available @Shape: [] 
TotalWaterAvailable = data['TotalWaterAvailable']
# @Parameter RequiredProduct @Def: Minimum required amount of product p @Shape: ['NumProducts'] 
RequiredProduct = data['RequiredProduct']

# Variables 
# @Variable OperatingTime @Def: The operating time for machine m @Shape: ['NumMachines'] 
OperatingTime = model.addVars(NumMachines, vtype=GRB.CONTINUOUS, name="OperatingTime")

# Constraints 
# @Constraint Constr_1 @Def: The total distilled water consumed by all machines cannot exceed TotalWaterAvailable.
model.addConstr(quicksum(WaterUsage[m] * OperatingTime[m] for m in range(NumMachines)) <= TotalWaterAvailable)
# @Constraint Constr_2 @Def: For each product p, the total production must be at least RequiredProduct[p].
for p in range(NumProducts):
    model.addConstr(quicksum(ProductionRate[m][p] * OperatingTime[m] for m in range(NumMachines)) >= RequiredProduct[p], name=f"ProdRequirement_{p}")
    
# Objective 
# @Objective Objective @Def: Minimize the total operating hours of all machines while meeting the minimum production requirements for each product and adhering to the total available distilled water.
model.setObjective(quicksum(OperatingTime[m] for m in range(NumMachines)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['OperatingTime'] = {m: OperatingTime[m].x for m in range(NumMachines)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
