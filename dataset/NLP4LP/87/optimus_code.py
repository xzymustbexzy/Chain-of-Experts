# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A vine company sells two types of bottles: vintage and regular. A vintage bottle
holds VintageBottleCapacity milliliters of vine, while a regular bottle holds
RegularBottleCapacity milliliters of vine. The company has TotalAvailableVine
milliliters of vine available. The number of regular bottles must be at least
RegularToVintageMinRatio times the number of vintage bottles. Additionally, at
least MinVintageBottles vintage bottles must be produced. The objective is to
maximize the total number of bottles produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/88/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter VintageBottleCapacity @Def: Capacity of a vintage bottle in milliliters @Shape: [] 
VintageBottleCapacity = data['VintageBottleCapacity']
# @Parameter RegularBottleCapacity @Def: Capacity of a regular bottle in milliliters @Shape: [] 
RegularBottleCapacity = data['RegularBottleCapacity']
# @Parameter TotalAvailableVine @Def: Total available vine in milliliters @Shape: [] 
TotalAvailableVine = data['TotalAvailableVine']
# @Parameter RegularToVintageMinRatio @Def: Minimum ratio of regular bottles to vintage bottles @Shape: [] 
RegularToVintageMinRatio = data['RegularToVintageMinRatio']
# @Parameter MinVintageBottles @Def: Minimum number of vintage bottles to be produced @Shape: [] 
MinVintageBottles = data['MinVintageBottles']

# Variables 
# @Variable NumberVintageBottles @Def: The number of vintage bottles to produce @Shape: [] 
NumberVintageBottles = model.addVar(vtype=GRB.INTEGER, lb=MinVintageBottles, name="NumberVintageBottles")
# @Variable NumberRegularBottles @Def: The number of regular bottles to produce @Shape: [] 
NumberRegularBottles = model.addVar(vtype=GRB.INTEGER, name="NumberRegularBottles")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of vine used by vintage and regular bottles must not exceed TotalAvailableVine milliliters.
model.addConstr(VintageBottleCapacity * NumberVintageBottles + RegularBottleCapacity * NumberRegularBottles <= TotalAvailableVine)
# @Constraint Constr_2 @Def: The number of regular bottles must be at least RegularToVintageMinRatio times the number of vintage bottles.
model.addConstr(NumberRegularBottles >= RegularToVintageMinRatio * NumberVintageBottles)
# @Constraint Constr_3 @Def: At least MinVintageBottles vintage bottles must be produced.
model.addConstr(NumberVintageBottles >= MinVintageBottles)

# Objective 
# @Objective Objective @Def: Maximize the total number of bottles produced.
model.setObjective(NumberVintageBottles + NumberRegularBottles, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberVintageBottles'] = NumberVintageBottles.x
variables['NumberRegularBottles'] = NumberRegularBottles.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
