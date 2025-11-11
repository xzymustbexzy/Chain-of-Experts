# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company produces kids size bottles and adult size bottles. Each kids size
bottle has a capacity of KidsBottleCapacity milliliters, and each adult size
bottle has a capacity of AdultBottleCapacity milliliters. The number of adult
size bottles produced must be at least AdultToKidsRatio times the number of kids
size bottles. At least MinKidsBottles kids size bottles must be produced. The
total available cough syrup is AvailableSyrup milliliters. The goal is to
maximize the total number of bottles produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/58/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter KidsBottleCapacity @Def: Capacity of a kids size bottle in milliliters @Shape: [] 
KidsBottleCapacity = data['KidsBottleCapacity']
# @Parameter AdultBottleCapacity @Def: Capacity of an adult size bottle in milliliters @Shape: [] 
AdultBottleCapacity = data['AdultBottleCapacity']
# @Parameter AdultToKidsRatio @Def: Minimum ratio of adult bottles to kids bottles @Shape: [] 
AdultToKidsRatio = data['AdultToKidsRatio']
# @Parameter MinKidsBottles @Def: Minimum number of kids size bottles to be produced @Shape: [] 
MinKidsBottles = data['MinKidsBottles']
# @Parameter AvailableSyrup @Def: Total available milliliters of cough syrup @Shape: [] 
AvailableSyrup = data['AvailableSyrup']

# Variables 
# @Variable NumberOfAdultBottles @Def: The number of adult size bottles to be produced @Shape: [] 
NumberOfAdultBottles = model.addVar(vtype=GRB.INTEGER, name="NumberOfAdultBottles")
# @Variable NumberOfKidsBottles @Def: The number of kids size bottles to be produced @Shape: [] 
NumberOfKidsBottles = model.addVar(vtype=GRB.INTEGER, name="NumberOfKidsBottles")

# Constraints 
# @Constraint Constr_1 @Def: The number of adult size bottles produced must be at least AdultToKidsRatio times the number of kids size bottles.
model.addConstr(NumberOfAdultBottles >= AdultToKidsRatio * NumberOfKidsBottles)
# @Constraint Constr_2 @Def: At least MinKidsBottles kids size bottles must be produced.
model.addConstr(NumberOfKidsBottles >= MinKidsBottles)
# @Constraint Constr_3 @Def: The total volume of cough syrup used by both kids and adult size bottles cannot exceed AvailableSyrup milliliters.
model.addConstr(AdultBottleCapacity * NumberOfAdultBottles + KidsBottleCapacity * NumberOfKidsBottles <= AvailableSyrup)

# Objective 
# @Objective Objective @Def: Maximize the total number of bottles produced.
model.setObjective(NumberOfAdultBottles + NumberOfKidsBottles, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfAdultBottles'] = NumberOfAdultBottles.x
variables['NumberOfKidsBottles'] = NumberOfKidsBottles.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
