# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A woodshop can purchase NumSawTypes different types of saws. Each saw type can
cut PlanksCutPerSaw planks of wood per day and produce SawdustPerSaw units of
sawdust per day. The woodshop must cut at least MinPlanks planks of wood per day
and produce at most MaxSawdust units of sawdust per day. The goal is to
determine the number of each type of saw to purchase to minimize the total
number of saws needed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/44/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumSawTypes @Def: Number of types of saws available @Shape: [] 
NumSawTypes = data['NumSawTypes']
# @Parameter PlanksCutPerSaw @Def: Number of planks cut per day by each saw type @Shape: ['NumSawTypes'] 
PlanksCutPerSaw = data['PlanksCutPerSaw']
# @Parameter SawdustPerSaw @Def: Units of sawdust produced per day by each saw type @Shape: ['NumSawTypes'] 
SawdustPerSaw = data['SawdustPerSaw']
# @Parameter MinPlanks @Def: Minimum number of planks to be cut per day @Shape: [] 
MinPlanks = data['MinPlanks']
# @Parameter MaxSawdust @Def: Maximum units of sawdust to be produced per day @Shape: [] 
MaxSawdust = data['MaxSawdust']

# Variables 
# @Variable NumberOfSaws @Def: The number of saws of each type used per day @Shape: ['NumSawTypes'] 
NumberOfSaws = model.addVars(range(NumSawTypes), vtype=GRB.INTEGER, name="NumberOfSaws")

# Constraints 
# @Constraint Constr_1 @Def: The woodshop must cut at least MinPlanks planks of wood per day.
model.addConstr(quicksum(NumberOfSaws[j] * PlanksCutPerSaw[j] for j in range(NumSawTypes)) >= MinPlanks)
# @Constraint Constr_2 @Def: The woodshop must produce at most MaxSawdust units of sawdust per day.
model.addConstr(quicksum(NumberOfSaws[i] * SawdustPerSaw[i] for i in range(NumSawTypes)) <= MaxSawdust)

# Objective 
# @Objective Objective @Def: Minimize the total number of saws purchased.
model.setObjective(quicksum(NumberOfSaws[i] for i in range(NumSawTypes)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfSaws'] = {j: NumberOfSaws[j].X for j in range(NumSawTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)