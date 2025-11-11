# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A soda company uses old and new vans to transport soda bottles to stores. Each
old van has a capacity of OldVanCapacity bottles and produces OldVanPollution
units of pollution. Each new van has a capacity of NewVanCapacity bottles and
produces NewVanPollution units of pollution. The company needs to transport at
least MinimumBottles soda bottles and can use at most MaximumNewVans new vans.
The goal is to determine the number of old and new vans to minimize the total
amount of pollution produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/143/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter OldVanCapacity @Def: Capacity of an old van in soda bottles @Shape: [] 
OldVanCapacity = data['OldVanCapacity']
# @Parameter NewVanCapacity @Def: Capacity of a new van in soda bottles @Shape: [] 
NewVanCapacity = data['NewVanCapacity']
# @Parameter OldVanPollution @Def: Pollution produced by an old van in units @Shape: [] 
OldVanPollution = data['OldVanPollution']
# @Parameter NewVanPollution @Def: Pollution produced by a new van in units @Shape: [] 
NewVanPollution = data['NewVanPollution']
# @Parameter MinimumBottles @Def: Minimum number of soda bottles that need to be sent @Shape: [] 
MinimumBottles = data['MinimumBottles']
# @Parameter MaximumNewVans @Def: Maximum number of new vans that can be used @Shape: [] 
MaximumNewVans = data['MaximumNewVans']

# Variables 
# @Variable NumberOfOldVans @Def: The number of old vans used @Shape: [] 
NumberOfOldVans = model.addVar(vtype=GRB.INTEGER, name="NumberOfOldVans")
# @Variable NumberOfNewVans @Def: The number of new vans used @Shape: [] 
NumberOfNewVans = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaximumNewVans, name="NumberOfNewVans")

# Constraints 
# @Constraint Constr_1 @Def: Each old van has a capacity of OldVanCapacity bottles and each new van has a capacity of NewVanCapacity bottles. The total number of bottles transported must be at least MinimumBottles.
model.addConstr(OldVanCapacity * NumberOfOldVans + NewVanCapacity * NumberOfNewVans >= MinimumBottles)
# @Constraint Constr_2 @Def: The number of new vans used must not exceed MaximumNewVans.
model.addConstr(NumberOfNewVans <= MaximumNewVans)

# Objective 
# @Objective Objective @Def: Total pollution is the sum of the pollution produced by all old vans and new vans. The objective is to minimize the total pollution.
model.setObjective(NumberOfOldVans * OldVanPollution + NumberOfNewVans * NewVanPollution, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfOldVans'] = NumberOfOldVans.x
variables['NumberOfNewVans'] = NumberOfNewVans.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
