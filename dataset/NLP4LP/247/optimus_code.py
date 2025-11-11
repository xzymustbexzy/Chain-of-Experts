# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Determine the number of each process to perform in order to maximize the total
MetalExtraction, subject to the constraints that the total WaterUsage does not
exceed MaxWater and the total PollutionProduction does not exceed MaxPollution.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/248/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter MaxWater @Def: Maximum units of water available @Shape: [] 
MaxWater = data['MaxWater']
# @Parameter MaxPollution @Def: Maximum units of pollution allowed @Shape: [] 
MaxPollution = data['MaxPollution']
# @Parameter MetalExtraction @Def: Amount of metal extracted per unit of process @Shape: ['NumProcesses'] 
MetalExtraction = data['MetalExtraction']
# @Parameter WaterUsage @Def: Amount of water used per unit of process @Shape: ['NumProcesses'] 
WaterUsage = data['WaterUsage']
# @Parameter PollutionProduction @Def: Amount of pollution produced per unit of process @Shape: ['NumProcesses'] 
PollutionProduction = data['PollutionProduction']

# Define the number of processes
NumProcesses = len(MetalExtraction)
    
# Variables 
# @Variable ProcessUnit @Def: The number of units for each process @Shape: ['NumProcesses'] 
ProcessUnit = model.addVars(NumProcesses, vtype=GRB.CONTINUOUS, name="ProcessUnit")
    
# Constraints 
# @Constraint Constr_1 @Def: The total WaterUsage does not exceed MaxWater.
model.addConstr(quicksum(WaterUsage[i] * ProcessUnit[i] for i in range(NumProcesses)) <= MaxWater)
# @Constraint Constr_2 @Def: The total PollutionProduction does not exceed MaxPollution.
model.addConstr(quicksum(PollutionProduction[i] * ProcessUnit[i] for i in range(NumProcesses)) <= MaxPollution)
    
# Objective 
# @Objective Objective @Def: Maximize the total MetalExtraction.
model.setObjective(quicksum(MetalExtraction[i] * ProcessUnit[i] for i in range(NumProcesses)), GRB.MAXIMIZE)
    
# Solve 
model.optimize()
    
# Extract solution 
solution = {}
variables = {}
objective = []
variables['ProcessUnit'] = {i: ProcessUnit[i].X for i in range(NumProcesses)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)