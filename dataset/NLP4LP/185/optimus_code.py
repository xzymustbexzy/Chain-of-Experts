# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
An international shipping company uses large ships and small ships to transport
containers. A large ship can carry LargeShipCapacity containers while a small
ship can carry SmallShipCapacity containers. The number of large ships cannot
exceed the number of small ships. The company needs to transport at least
RequiredContainers containers. Find the minimum number of ships that can be
used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/186/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter LargeShipCapacity @Def: Number of containers a large ship can carry @Shape: [] 
LargeShipCapacity = data['LargeShipCapacity']
# @Parameter SmallShipCapacity @Def: Number of containers a small ship can carry @Shape: [] 
SmallShipCapacity = data['SmallShipCapacity']
# @Parameter RequiredContainers @Def: Minimum number of containers to transport @Shape: [] 
RequiredContainers = data['RequiredContainers']

# Variables 
# @Variable NumberLargeShips @Def: The number of large ships @Shape: [] 
NumberLargeShips = model.addVar(vtype=GRB.INTEGER, name="NumberLargeShips")
# @Variable NumberSmallShips @Def: The number of small ships @Shape: [] 
NumberSmallShips = model.addVar(vtype=GRB.INTEGER, name="NumberSmallShips")

# Constraints 
# @Constraint Constr_1 @Def: The number of large ships does not exceed the number of small ships.
model.addConstr(NumberLargeShips <= NumberSmallShips)
# @Constraint Constr_2 @Def: The total number of containers transported by large and small ships is at least RequiredContainers.
model.addConstr(NumberLargeShips * LargeShipCapacity + NumberSmallShips * SmallShipCapacity >= RequiredContainers)

# Objective 
# @Objective Objective @Def: Minimize the total number of ships used, which is the sum of large ships and small ships.
model.setObjective(NumberLargeShips + NumberSmallShips, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberLargeShips'] = NumberLargeShips.x
variables['NumberSmallShips'] = NumberSmallShips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
