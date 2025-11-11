# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
An aquarium uses Otters and Dolphins to perform tricks. Each Otter performs
OtterTricks at a time and requires OtterTreats treats per performance. Each
Dolphin performs DolphinTricks at a time and requires DolphinTreats treats per
performance. The aquarium must use at least MinDolphins Dolphins and ensure that
no more than MaxOtterPercentage of the total performers are Otters. With a total
of TotalTreats treats available, the objective is to maximize the total number
of tricks performed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/145/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter OtterTricks @Def: Number of tricks an otter can perform at a time @Shape: [] 
OtterTricks = data['OtterTricks']
# @Parameter OtterTreats @Def: Number of treats an otter requires to perform at a time @Shape: [] 
OtterTreats = data['OtterTreats']
# @Parameter DolphinTricks @Def: Number of tricks a dolphin can perform at a time @Shape: [] 
DolphinTricks = data['DolphinTricks']
# @Parameter DolphinTreats @Def: Number of treats a dolphin requires to perform at a time @Shape: [] 
DolphinTreats = data['DolphinTreats']
# @Parameter MinDolphins @Def: Minimum number of dolphins required @Shape: [] 
MinDolphins = data['MinDolphins']
# @Parameter MaxOtterPercentage @Def: Maximum percentage of performers that can be otters @Shape: [] 
MaxOtterPercentage = data['MaxOtterPercentage']
# @Parameter TotalTreats @Def: Total number of treats available @Shape: [] 
TotalTreats = data['TotalTreats']

# Variables 
# @Variable NumberOfDolphins @Def: The number of dolphins @Shape: [] 
NumberOfDolphins = model.addVar(vtype=GRB.INTEGER, name="NumberOfDolphins")
# @Variable NumberOfOtters @Def: The number of otters @Shape: [] 
NumberOfOtters = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberOfOtters")

# Constraints 
# @Constraint Constr_1 @Def: The number of Dolphins must be at least MinDolphins.
model.addConstr(NumberOfDolphins >= MinDolphins)
# @Constraint Constr_2 @Def: The number of Otters must not exceed MaxOtterPercentage of the total number of performers.
model.addConstr(NumberOfOtters <= MaxOtterPercentage * (NumberOfOtters + NumberOfDolphins))
# @Constraint Constr_3 @Def: The total number of treats used by Otters and Dolphins must not exceed TotalTreats.
model.addConstr(OtterTreats * NumberOfOtters + DolphinTreats * NumberOfDolphins <= TotalTreats)

# Objective 
# @Objective Objective @Def: Maximize the total number of tricks performed, which is the sum of OtterTricks multiplied by the number of Otters and DolphinTricks multiplied by the number of Dolphins.
model.setObjective(OtterTricks * NumberOfOtters + DolphinTricks * NumberOfDolphins, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfDolphins'] = NumberOfDolphins.x
variables['NumberOfOtters'] = NumberOfOtters.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
