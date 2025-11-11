# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company distributes masks using small boxes and large boxes. Each small box
holds MasksPerSmallBox masks, and each large box holds MasksPerLargeBox masks.
The number of small boxes must be at least MinRatioSmallToLarge times the number
of large boxes. At least MinLargeBoxes large boxes must be used. The total
number of masks distributed must be at least TotalMasksRequired. The objective
is to minimize the total number of boxes used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/243/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MasksPerSmallBox @Def: Number of masks that fit in a small box @Shape: [] 
MasksPerSmallBox = data['MasksPerSmallBox']
# @Parameter MasksPerLargeBox @Def: Number of masks that fit in a large box @Shape: [] 
MasksPerLargeBox = data['MasksPerLargeBox']
# @Parameter MinRatioSmallToLarge @Def: Minimum ratio of small boxes to large boxes @Shape: [] 
MinRatioSmallToLarge = data['MinRatioSmallToLarge']
# @Parameter MinLargeBoxes @Def: Minimum number of large boxes required @Shape: [] 
MinLargeBoxes = data['MinLargeBoxes']
# @Parameter TotalMasksRequired @Def: Minimum number of masks to distribute @Shape: [] 
TotalMasksRequired = data['TotalMasksRequired']

# Variables 
# @Variable NumberSmallBoxes @Def: The number of small boxes @Shape: [] 
NumberSmallBoxes = model.addVar(vtype=GRB.INTEGER, name="NumberSmallBoxes")
# @Variable NumberLargeBoxes @Def: The number of large boxes @Shape: [] 
NumberLargeBoxes = model.addVar(vtype=GRB.INTEGER, lb=MinLargeBoxes, name="NumberLargeBoxes")

# Constraints 
# @Constraint Constr_1 @Def: The number of small boxes must be at least MinRatioSmallToLarge times the number of large boxes.
model.addConstr(NumberSmallBoxes >= MinRatioSmallToLarge * NumberLargeBoxes)
# @Constraint Constr_2 @Def: At least MinLargeBoxes large boxes must be used.
model.addConstr(NumberLargeBoxes >= MinLargeBoxes)
# @Constraint Constr_3 @Def: The total number of masks distributed must be at least TotalMasksRequired.
model.addConstr(MasksPerSmallBox * NumberSmallBoxes + MasksPerLargeBox * NumberLargeBoxes >= TotalMasksRequired)

# Objective 
# @Objective Objective @Def: The total number of boxes used is the sum of small and large boxes. The objective is to minimize the total number of boxes used.
model.setObjective(NumberSmallBoxes + NumberLargeBoxes, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberSmallBoxes'] = NumberSmallBoxes.x
variables['NumberLargeBoxes'] = NumberLargeBoxes.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
