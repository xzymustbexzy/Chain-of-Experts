# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A fast food place produces wraps and platters. Each wrap requires MeatPerWrap
units of meat and RicePerWrap units of rice, and takes TimePerWrap time to make.
Each platter requires MeatPerPlatter units of meat and RicePerPlatter units of
rice, and takes TimePerPlatter time to make. The production must use at least
MinMeat units of meat and MinRice units of rice. Additionally, the number of
wraps produced must be at least WrapPlatterRatio times the number of platters
produced. The objective is to minimize the total production time.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/46/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MeatPerWrap @Def: Amount of meat required to produce one wrap @Shape: [] 
MeatPerWrap = data['MeatPerWrap']
# @Parameter RicePerWrap @Def: Amount of rice required to produce one wrap @Shape: [] 
RicePerWrap = data['RicePerWrap']
# @Parameter MeatPerPlatter @Def: Amount of meat required to produce one platter @Shape: [] 
MeatPerPlatter = data['MeatPerPlatter']
# @Parameter RicePerPlatter @Def: Amount of rice required to produce one platter @Shape: [] 
RicePerPlatter = data['RicePerPlatter']
# @Parameter TimePerWrap @Def: Production time required to produce one wrap @Shape: [] 
TimePerWrap = data['TimePerWrap']
# @Parameter TimePerPlatter @Def: Production time required to produce one platter @Shape: [] 
TimePerPlatter = data['TimePerPlatter']
# @Parameter MinMeat @Def: Minimum required amount of meat @Shape: [] 
MinMeat = data['MinMeat']
# @Parameter MinRice @Def: Minimum required amount of rice @Shape: [] 
MinRice = data['MinRice']
# @Parameter WrapPlatterRatio @Def: Minimum ratio of wraps to platters @Shape: [] 
WrapPlatterRatio = data['WrapPlatterRatio']

# Variables 
# @Variable NumberOfWraps @Def: The number of wraps produced @Shape: [] 
NumberOfWraps = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfWraps")
# @Variable NumberOfPlatters @Def: The number of platters produced @Shape: [] 
NumberOfPlatters = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfPlatters")

# Constraints 
# @Constraint Constr_1 @Def: The total meat used, calculated as MeatPerWrap multiplied by the number of wraps plus MeatPerPlatter multiplied by the number of platters, must be at least MinMeat.
model.addConstr(MeatPerWrap * NumberOfWraps + MeatPerPlatter * NumberOfPlatters >= MinMeat)
# @Constraint Constr_2 @Def: The total rice used, calculated as RicePerWrap multiplied by the number of wraps plus RicePerPlatter multiplied by the number of platters, must be at least MinRice.
model.addConstr(RicePerWrap * NumberOfWraps + RicePerPlatter * NumberOfPlatters >= MinRice)
# @Constraint Constr_3 @Def: The number of wraps produced must be at least WrapPlatterRatio times the number of platters produced.
model.addConstr(NumberOfWraps >= WrapPlatterRatio * NumberOfPlatters)

# Objective 
# @Objective Objective @Def: Total production time is TimePerWrap multiplied by the number of wraps plus TimePerPlatter multiplied by the number of platters. The objective is to minimize the total production time while meeting requirements for meat, rice, and product ratio.
model.setObjective(TimePerWrap * NumberOfWraps + TimePerPlatter * NumberOfPlatters, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfWraps'] = NumberOfWraps.x
variables['NumberOfPlatters'] = NumberOfPlatters.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
