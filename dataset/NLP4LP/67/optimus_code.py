# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A banana company sells their bananas in small and large crates. A small crate
can hold CapacitySmallCrate bananas while a large crate can hold
CapacityLargeCrate bananas. The number of large crates must be at least
LargeToSmallRatio times the number of small crates. At least MinSmallCrates
should be used. If the company has available TotalBananas bananas, how many of
each crate should the company use to maximize the total number of crates
produced?
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/68/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CapacitySmallCrate @Def: Number of bananas a small crate can hold @Shape: [] 
CapacitySmallCrate = data['CapacitySmallCrate']
# @Parameter CapacityLargeCrate @Def: Number of bananas a large crate can hold @Shape: [] 
CapacityLargeCrate = data['CapacityLargeCrate']
# @Parameter TotalBananas @Def: Total number of bananas available @Shape: [] 
TotalBananas = data['TotalBananas']
# @Parameter MinSmallCrates @Def: Minimum number of small crates to be used @Shape: [] 
MinSmallCrates = data['MinSmallCrates']
# @Parameter LargeToSmallRatio @Def: Minimum multiple of small crates that large crates must be @Shape: [] 
LargeToSmallRatio = data['LargeToSmallRatio']

# Variables 
# @Variable SmallCrates @Def: The number of small crates @Shape: [] 
SmallCrates = model.addVar(vtype=GRB.INTEGER, lb=MinSmallCrates, name="SmallCrates")
# @Variable LargeCrates @Def: The number of large crates @Shape: [] 
LargeCrates = model.addVar(vtype=GRB.INTEGER, name="LargeCrates")

# Constraints 
# @Constraint Constr_1 @Def: The number of large crates must be at least LargeToSmallRatio times the number of small crates.
model.addConstr(LargeCrates >= LargeToSmallRatio * SmallCrates)
# @Constraint Constr_2 @Def: At least MinSmallCrates should be used.
model.addConstr(SmallCrates >= MinSmallCrates)
# @Constraint Constr_3 @Def: The total number of bananas used by small and large crates cannot exceed TotalBananas.
model.addConstr(CapacitySmallCrate * SmallCrates + CapacityLargeCrate * LargeCrates <= TotalBananas)

# Objective 
# @Objective Objective @Def: The total number of crates produced is the sum of small and large crates. The objective is to maximize the total number of crates produced.
model.setObjective(SmallCrates + LargeCrates, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SmallCrates'] = SmallCrates.x
variables['LargeCrates'] = LargeCrates.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
