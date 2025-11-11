# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A fire department employs NumFireFighterTypes different fire fighter types. Each
fire fighter type works HoursPerShift hours per shift and incurs CostPerShift
cost per shift. The fire department needs at least TotalHoursRequired fire
fighter hours and has a budget of Budget. The objective is to minimize the total
number of fire fighters.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/70/parameters.json", "r") as f:
    data = json.load(f)
        
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumFireFighterTypes @Def: Number of fire fighter types @Shape: [] 
NumFireFighterTypes = data['NumFireFighterTypes']
# @Parameter HoursPerShift @Def: Amount of hours each fire fighter type works per shift @Shape: ['NumFireFighterTypes'] 
HoursPerShift = data['HoursPerShift']
# @Parameter CostPerShift @Def: Cost of each fire fighter type per shift @Shape: ['NumFireFighterTypes'] 
CostPerShift = data['CostPerShift']
# @Parameter TotalHoursRequired @Def: Total required fire fighter hours @Shape: [] 
TotalHoursRequired = data['TotalHoursRequired']
# @Parameter Budget @Def: Total available budget @Shape: [] 
Budget = data['Budget']

# Variables 
# @Variable ShiftsPerType @Def: The number of shifts for each fire fighter type @Shape: ['NumFireFighterTypes'] 
ShiftsPerType = model.addVars(NumFireFighterTypes, vtype=GRB.INTEGER, name="ShiftsPerType")

# Constraints 
# @Constraint Constr_1 @Def: The fire department needs at least TotalHoursRequired fire fighter hours.
model.addConstr(quicksum(HoursPerShift[i] * ShiftsPerType[i] for i in range(NumFireFighterTypes)) >= TotalHoursRequired)
# @Constraint Constr_2 @Def: The fire department has a budget of Budget.
model.addConstr(quicksum(ShiftsPerType[t] * CostPerShift[t] for t in range(NumFireFighterTypes)) <= Budget)

# Objective 
# @Objective Objective @Def: Minimize the total number of fire fighters.
model.setObjective(quicksum(ShiftsPerType[t] for t in range(NumFireFighterTypes)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ShiftsPerType'] = {i: ShiftsPerType[i].x for i in range(NumFireFighterTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
