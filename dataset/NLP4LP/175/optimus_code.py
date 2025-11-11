# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A construction company uses cows and elephants to carry bricks. Each cow can
carry BrickCapacityCow bricks and each elephant can carry BrickCapacityElephant
bricks. The number of elephants cannot exceed MaxElephantsToCowsRatio times the
number of cows, and the number of cows cannot exceed MaxCowsToElephantsRatio
times the number of elephants. The company needs to transport at least
RequiredBricks bricks. Determine the minimum number of animals, cows, and
elephants required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/176/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter BrickCapacityCow @Def: Number of bricks a cow can carry on its back @Shape: [] 
BrickCapacityCow = data['BrickCapacityCow']
# @Parameter BrickCapacityElephant @Def: Number of bricks an elephant can carry on its back @Shape: [] 
BrickCapacityElephant = data['BrickCapacityElephant']
# @Parameter MaxElephantsToCowsRatio @Def: Maximum ratio of elephants to cows @Shape: [] 
MaxElephantsToCowsRatio = data['MaxElephantsToCowsRatio']
# @Parameter MaxCowsToElephantsRatio @Def: Maximum ratio of cows to elephants @Shape: [] 
MaxCowsToElephantsRatio = data['MaxCowsToElephantsRatio']
# @Parameter RequiredBricks @Def: Minimum number of bricks to transport @Shape: [] 
RequiredBricks = data['RequiredBricks']

# Variables 
# @Variable NumberOfCows @Def: The number of cows @Shape: [] 
NumberOfCows = model.addVar(vtype=GRB.INTEGER, name="NumberOfCows")
# @Variable NumberOfElephants @Def: The number of elephants @Shape: [] 
NumberOfElephants = model.addVar(vtype=GRB.INTEGER, name="NumberOfElephants")

# Constraints 
# @Constraint Constr_1 @Def: Each cow can carry BrickCapacityCow bricks and each elephant can carry BrickCapacityElephant bricks. The total number of bricks transported must be at least RequiredBricks.
model.addConstr(BrickCapacityCow * NumberOfCows + BrickCapacityElephant * NumberOfElephants >= RequiredBricks)
# @Constraint Constr_2 @Def: The number of elephants cannot exceed MaxElephantsToCowsRatio times the number of cows.
model.addConstr(NumberOfElephants <= MaxElephantsToCowsRatio * NumberOfCows)
# @Constraint Constr_3 @Def: The number of cows cannot exceed MaxCowsToElephantsRatio times the number of elephants.
model.addConstr(NumberOfCows <= MaxCowsToElephantsRatio * NumberOfElephants)

# Objective 
# @Objective Objective @Def: Minimize the total number of animals (cows and elephants) required to transport at least RequiredBricks bricks while adhering to the specified ratio constraints between cows and elephants.
model.setObjective(NumberOfCows + NumberOfElephants, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfCows'] = NumberOfCows.x
variables['NumberOfElephants'] = NumberOfElephants.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
