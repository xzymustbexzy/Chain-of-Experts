# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company produces two types of containers: cans and glass bottles. Each can
holds CapacityCan milliliters and each glass bottle holds CapacityBottle
milliliters. The company must bottle at least MinimumTotalVolume milliliters per
day. The number of cans produced must be at least RatioCansToBottles times the
number of glass bottles produced. Additionally, at least MinimumGlassBottles
glass bottles must be produced each day. The objective is to maximize the total
number of containers produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/240/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CapacityCan @Def: The amount of soda that one can container holds, in milliliters. @Shape: [] 
CapacityCan = data['CapacityCan']
# @Parameter CapacityBottle @Def: The amount of soda that one glass bottle container holds, in milliliters. @Shape: [] 
CapacityBottle = data['CapacityBottle']
# @Parameter MinimumTotalVolume @Def: The minimum total volume of soda that needs to be bottled each day, in milliliters. @Shape: [] 
MinimumTotalVolume = data['MinimumTotalVolume']
# @Parameter RatioCansToBottles @Def: The minimum ratio of number of cans to number of glass bottles. @Shape: [] 
RatioCansToBottles = data['RatioCansToBottles']
# @Parameter MinimumGlassBottles @Def: The minimum number of glass bottles that must be produced. @Shape: [] 
MinimumGlassBottles = data['MinimumGlassBottles']

# Variables 
# @Variable NumberOfBottles @Def: The number of glass bottle containers to produce @Shape: [] 
NumberOfBottles = model.addVar(vtype=GRB.INTEGER, name="NumberOfBottles")
# @Variable NumberOfCans @Def: The number of cans to produce @Shape: [] 
NumberOfCans = model.addVar(vtype=GRB.INTEGER, name="NumberOfCans")

# Constraints 
# @Constraint Constr_1 @Def: The total volume bottled per day must be at least MinimumTotalVolume milliliters.
model.addConstr(CapacityBottle * NumberOfBottles >= MinimumTotalVolume)
# @Constraint Constr_2 @Def: The number of cans produced must be at least RatioCansToBottles times the number of glass bottles produced.
model.addConstr(NumberOfCans >= RatioCansToBottles * NumberOfBottles)
# @Constraint Constr_3 @Def: At least MinimumGlassBottles glass bottles must be produced each day.
model.addConstr(NumberOfBottles >= MinimumGlassBottles)

# Objective 
# @Objective Objective @Def: The total number of containers produced is the sum of the number of cans and the number of glass bottles. The objective is to maximize the total number of containers produced.
model.setObjective(NumberOfCans + NumberOfBottles, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfBottles'] = NumberOfBottles.x
variables['NumberOfCans'] = NumberOfCans.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
