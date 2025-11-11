# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
To maximize the production of carbon dioxide, wood is burned using NumProcesses
different processes. Each process requires WoodRequiredPerProcess units of wood
and OxygenRequiredPerProcess units of oxygen to produce CO2ProducedPerProcess
units of carbon dioxide. The total available wood and oxygen are
TotalWoodAvailable and TotalOxygenAvailable units, respectively. Determine the
number of each process to use to maximize carbon dioxide production.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/64/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumProcesses @Def: Number of available processes @Shape: [] 
NumProcesses = data['NumProcesses']
# @Parameter WoodRequiredPerProcess @Def: Amount of wood required for each process @Shape: ['NumProcesses'] 
WoodRequiredPerProcess = data['WoodRequiredPerProcess']
# @Parameter OxygenRequiredPerProcess @Def: Amount of oxygen required for each process @Shape: ['NumProcesses'] 
OxygenRequiredPerProcess = data['OxygenRequiredPerProcess']
# @Parameter CO2ProducedPerProcess @Def: Amount of carbon dioxide produced by each process @Shape: ['NumProcesses'] 
CO2ProducedPerProcess = data['CO2ProducedPerProcess']
# @Parameter TotalWoodAvailable @Def: Total amount of wood available @Shape: [] 
TotalWoodAvailable = data['TotalWoodAvailable']
# @Parameter TotalOxygenAvailable @Def: Total amount of oxygen available @Shape: [] 
TotalOxygenAvailable = data['TotalOxygenAvailable']

# Variables 
# @Variable ProcessUsage @Def: The amount of each process to be used @Shape: ['NumProcesses'] 
ProcessUsage = model.addVars(NumProcesses, vtype=GRB.CONTINUOUS, name="ProcessUsage")

# Constraints 
# @Constraint Constr_1 @Def: The total wood consumed by all processes cannot exceed TotalWoodAvailable.
model.addConstr(quicksum(WoodRequiredPerProcess[i] * ProcessUsage[i] for i in range(NumProcesses)) <= TotalWoodAvailable)
# @Constraint Constr_2 @Def: The total oxygen consumed by all processes cannot exceed TotalOxygenAvailable.
model.addConstr(quicksum(ProcessUsage[i] * OxygenRequiredPerProcess[i] for i in range(NumProcesses)) <= TotalOxygenAvailable)

# Objective 
# @Objective Objective @Def: Maximize the total carbon dioxide production by summing the carbon dioxide produced by each process.
model.setObjective(quicksum(CO2ProducedPerProcess[i] * ProcessUsage[i] for i in range(NumProcesses)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ProcessUsage'] = {i: ProcessUsage[i].X for i in range(NumProcesses)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)