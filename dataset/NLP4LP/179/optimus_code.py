# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A grape farmer uses small and large crates to transport grapes. Each small crate
holds SmallCrateCapacity grapes, and each large crate holds LargeCrateCapacity
grapes. The number of small crates used must be at least
MinimumSmallToLargeRatio times the number of large crates. The farmer can use up
to MaxSmallCrates small crates and up to MaxLargeCrates large crates.
Additionally, the truck can carry up to MaxTotalCrates crates in total, and at
least MinLargeCrates large crates must be used. The objective is to determine
the number of small and large crates to maximize the total number of grapes
transported.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/180/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SmallCrateCapacity @Def: Number of grapes a small crate can hold @Shape: [] 
SmallCrateCapacity = data['SmallCrateCapacity']
# @Parameter LargeCrateCapacity @Def: Number of grapes a large crate can hold @Shape: [] 
LargeCrateCapacity = data['LargeCrateCapacity']
# @Parameter MinimumSmallToLargeRatio @Def: Minimum ratio of small crates to large crates @Shape: [] 
MinimumSmallToLargeRatio = data['MinimumSmallToLargeRatio']
# @Parameter MaxSmallCrates @Def: Maximum number of small crates available @Shape: [] 
MaxSmallCrates = data['MaxSmallCrates']
# @Parameter MaxLargeCrates @Def: Maximum number of large crates available @Shape: [] 
MaxLargeCrates = data['MaxLargeCrates']
# @Parameter MaxTotalCrates @Def: Maximum number of crates the truck can carry @Shape: [] 
MaxTotalCrates = data['MaxTotalCrates']
# @Parameter MinLargeCrates @Def: Minimum number of large crates to be used @Shape: [] 
MinLargeCrates = data['MinLargeCrates']

# Variables 
# @Variable NumSmallCrates @Def: The number of small crates used @Shape: [] 
NumSmallCrates = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxSmallCrates, name="NumSmallCrates")
# @Variable NumLargeCrates @Def: The number of large crates used @Shape: [] 
NumLargeCrates = model.addVar(vtype=GRB.INTEGER, lb=MinLargeCrates, ub=MaxLargeCrates, name="NumLargeCrates")

# Constraints 
# @Constraint Constr_1 @Def: The number of small crates used must be at least MinimumSmallToLargeRatio times the number of large crates.
model.addConstr(NumSmallCrates >= MinimumSmallToLargeRatio * NumLargeCrates)
# @Constraint Constr_2 @Def: The number of small crates used cannot exceed MaxSmallCrates.
model.addConstr(NumSmallCrates <= MaxSmallCrates)
# @Constraint Constr_3 @Def: The number of large crates used cannot exceed MaxLargeCrates.
model.addConstr(NumLargeCrates <= MaxLargeCrates)
# @Constraint Constr_4 @Def: The total number of crates used cannot exceed MaxTotalCrates.
model.addConstr(NumSmallCrates + NumLargeCrates <= MaxTotalCrates)
# @Constraint Constr_5 @Def: At least MinLargeCrates large crates must be used.
model.addConstr(NumLargeCrates >= MinLargeCrates)

# Objective 
# @Objective Objective @Def: The total number of grapes transported is the sum of the grapes in small crates and large crates. The objective is to maximize the total number of grapes transported.
model.setObjective(NumSmallCrates * SmallCrateCapacity + NumLargeCrates * LargeCrateCapacity, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumSmallCrates'] = NumSmallCrates.x
variables['NumLargeCrates'] = NumLargeCrates.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
