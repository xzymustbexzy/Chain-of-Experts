# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company can build two types of butcher shops: small shops that produce
HotDogsPerSmallShop hot dogs per day and require WorkersPerSmallShop workers
each, and large shops that produce HotDogsPerLargeShop hot dogs per day and
require WorkersPerLargeShop workers each. The company must produce at least
MinimumHotDogsPerDay hot dogs per day and has AvailableWorkers workers
available. The objective is to minimize the total number of butcher shops built.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/72/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter HotDogsPerSmallShop @Def: Number of hot dogs produced per small shop per day @Shape: [] 
HotDogsPerSmallShop = data['HotDogsPerSmallShop']
# @Parameter WorkersPerSmallShop @Def: Number of workers required for a small shop @Shape: [] 
WorkersPerSmallShop = data['WorkersPerSmallShop']
# @Parameter HotDogsPerLargeShop @Def: Number of hot dogs produced per large shop per day @Shape: [] 
HotDogsPerLargeShop = data['HotDogsPerLargeShop']
# @Parameter WorkersPerLargeShop @Def: Number of workers required for a large shop @Shape: [] 
WorkersPerLargeShop = data['WorkersPerLargeShop']
# @Parameter MinimumHotDogsPerDay @Def: Minimum number of hot dogs to be produced per day @Shape: [] 
MinimumHotDogsPerDay = data['MinimumHotDogsPerDay']
# @Parameter AvailableWorkers @Def: Total number of available workers @Shape: [] 
AvailableWorkers = data['AvailableWorkers']

# Variables 
# @Variable NumberOfSmallShops @Def: Number of small shops @Shape: [] 
NumberOfSmallShops = model.addVar(vtype=GRB.INTEGER, name="NumberOfSmallShops")
# @Variable NumberOfLargeShops @Def: Number of large shops @Shape: [] 
NumberOfLargeShops = model.addVar(vtype=GRB.INTEGER, name="NumberOfLargeShops")

# Constraints 
# @Constraint Constr_1 @Def: HotDogsPerSmallShop * NumberOfSmallShops + HotDogsPerLargeShop * NumberOfLargeShops >= MinimumHotDogsPerDay
model.addConstr(HotDogsPerSmallShop * NumberOfSmallShops + HotDogsPerLargeShop * NumberOfLargeShops >= MinimumHotDogsPerDay)
# @Constraint Constr_2 @Def: WorkersPerSmallShop * NumberOfSmallShops + WorkersPerLargeShop * NumberOfLargeShops <= AvailableWorkers
model.addConstr(WorkersPerSmallShop * NumberOfSmallShops + WorkersPerLargeShop * NumberOfLargeShops <= AvailableWorkers)

# Objective 
# @Objective Objective @Def: Minimize the total number of butcher shops built, calculated as NumberOfSmallShops + NumberOfLargeShops.
model.setObjective(NumberOfSmallShops + NumberOfLargeShops, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfSmallShops'] = NumberOfSmallShops.x
variables['NumberOfLargeShops'] = NumberOfLargeShops.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
