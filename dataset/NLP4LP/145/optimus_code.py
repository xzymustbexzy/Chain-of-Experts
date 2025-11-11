# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company supplies at least MinPairsToSupply items using vehicles of two types:
vans and trucks. Each van can transport VanCapacity items and each truck can
transport TruckCapacity items. The number of trucks used cannot exceed the
number of vans used. Determine the minimum number of vans required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/146/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter VanCapacity @Def: Number of pairs of shoes a van can transport @Shape: [] 
VanCapacity = data['VanCapacity']
# @Parameter TruckCapacity @Def: Number of pairs of shoes a truck can transport @Shape: [] 
TruckCapacity = data['TruckCapacity']
# @Parameter MinPairsToSupply @Def: Minimum number of pairs of shoes to supply @Shape: [] 
MinPairsToSupply = data['MinPairsToSupply']

# Variables 
# @Variable NumberOfVans @Def: The number of vans used to transport the shoes @Shape: ['Integer'] 
NumberOfVans = model.addVar(vtype=GRB.INTEGER, name="NumberOfVans")
# @Variable NumberOfTrucks @Def: The number of trucks used to transport the shoes @Shape: ['Integer'] 
NumberOfTrucks = model.addVar(vtype=GRB.INTEGER, name="NumberOfTrucks")

# Constraints 
# @Constraint Constr_1 @Def: The total number of items transported by vans and trucks must be at least MinPairsToSupply.
model.addConstr(VanCapacity * NumberOfVans + TruckCapacity * NumberOfTrucks >= MinPairsToSupply)
# @Constraint Constr_2 @Def: The number of trucks used cannot exceed the number of vans used.
model.addConstr(NumberOfTrucks <= NumberOfVans)

# Objective 
# @Objective Objective @Def: Minimize the number of vans required to supply at least MinPairsToSupply items while ensuring that the number of trucks used does not exceed the number of vans used.
model.setObjective(NumberOfVans, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfVans'] = NumberOfVans.x
variables['NumberOfTrucks'] = NumberOfTrucks.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
