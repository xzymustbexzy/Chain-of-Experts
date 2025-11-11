# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A pharmaceutical company operates NumLabs laboratories to produce NumPillTypes
types of medication pills. Each laboratory has a ProductionRate of pills per
hour for each pill type. Each session at a laboratory requires WorkerLaborPerLab
worker hours. The company has TotalWorkerHours worker hours available and must
produce at least MinRequiredPills pills for each pill type. The objective is to
determine the number of hours each laboratory should operate to minimize the
total time needed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/126/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumLabs @Def: Number of labs @Shape: [] 
NumLabs = data['NumLabs']
# @Parameter NumPillTypes @Def: Number of pill types @Shape: [] 
NumPillTypes = data['NumPillTypes']
# @Parameter ProductionRate @Def: Production rate (pills per hour) for each lab and pill type @Shape: ['NumLabs', 'NumPillTypes'] 
ProductionRate = data['ProductionRate']
# @Parameter WorkerLaborPerLab @Def: Worker labor hours required per session for each lab @Shape: ['NumLabs'] 
WorkerLaborPerLab = data['WorkerLaborPerLab']
# @Parameter TotalWorkerHours @Def: Total worker hours available @Shape: [] 
TotalWorkerHours = data['TotalWorkerHours']
# @Parameter MinRequiredPills @Def: Minimum required pills for each pill type @Shape: ['NumPillTypes'] 
MinRequiredPills = data['MinRequiredPills']

# Variables 
# @Variable Sessions @Def: The number of sessions for each lab @Shape: ['NumLabs'] 
Sessions = model.addVars(NumLabs, vtype=GRB.CONTINUOUS, name="Sessions")

# Constraints 
# @Constraint Constr_1 @Def: The total worker labor hours used across all laboratories must not exceed TotalWorkerHours.
model.addConstr(quicksum(WorkerLaborPerLab[l] * Sessions[l] for l in range(NumLabs)) <= TotalWorkerHours)
# @Constraint Constr_2 @Def: For each pill type, the total number of pills produced across all laboratories must be at least MinRequiredPills.
model.addConstrs((quicksum(Sessions[l] * ProductionRate[l, p] for l in range(NumLabs)) >= MinRequiredPills[p] for p in range(NumPillTypes)), name="MinRequiredPills")

# Objective 
# @Objective Objective @Def: Minimize the total operating hours across all laboratories to determine the number of hours each laboratory should operate.
model.setObjective(quicksum(Sessions[i] * WorkerLaborPerLab[i] for i in range(NumLabs)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Sessions'] = Sessions.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
