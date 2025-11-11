# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Maximize the total fat intake, which is FatApple multiplied by the number of
apple servings plus FatCarrot multiplied by the number of carrot servings.
Subject to the constraint that the total folate intake, calculated as
FolateApple multiplied by the number of apple servings plus FolateCarrot
multiplied by the number of carrot servings, does not exceed MaxFolate.
Additionally, the number of apple servings must be equal to AppleToCarrotRatio
multiplied by the number of carrot servings, and the number of carrot servings
must be at least MinCarrotServings.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/104/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter FatApple @Def: Fat units per serving of apple flavored baby food @Shape: [] 
FatApple = data['FatApple']
# @Parameter FolateApple @Def: Folate units per serving of apple flavored baby food @Shape: [] 
FolateApple = data['FolateApple']
# @Parameter FatCarrot @Def: Fat units per serving of carrot flavored baby food @Shape: [] 
FatCarrot = data['FatCarrot']
# @Parameter FolateCarrot @Def: Folate units per serving of carrot flavored baby food @Shape: [] 
FolateCarrot = data['FolateCarrot']
# @Parameter AppleToCarrotRatio @Def: Multiplier for the number of apple servings relative to carrot servings @Shape: [] 
AppleToCarrotRatio = data['AppleToCarrotRatio']
# @Parameter MinCarrotServings @Def: Minimum servings of carrot flavored baby food @Shape: [] 
MinCarrotServings = data['MinCarrotServings']
# @Parameter MaxFolate @Def: Maximum total folate units allowed @Shape: [] 
MaxFolate = data['MaxFolate']

# Variables 
# @Variable AppleServings @Def: The number of apple servings @Shape: [] 
AppleServings = model.addVar(vtype=GRB.CONTINUOUS, name="AppleServings")
# @Variable CarrotServings @Def: The number of carrot servings @Shape: [] 
CarrotServings = model.addVar(vtype=GRB.CONTINUOUS, lb=MinCarrotServings, name="CarrotServings")

# Constraints 
# @Constraint Constr_1 @Def: The total folate intake (FolateApple * number of apple servings + FolateCarrot * number of carrot servings) does not exceed MaxFolate.
model.addConstr(FolateApple * AppleServings + FolateCarrot * CarrotServings <= MaxFolate)
# @Constraint Constr_2 @Def: The number of apple servings is equal to AppleToCarrotRatio multiplied by the number of carrot servings.
model.addConstr(AppleServings == AppleToCarrotRatio * CarrotServings)
# @Constraint Constr_3 @Def: The number of carrot servings is at least MinCarrotServings.
model.addConstr(CarrotServings >= MinCarrotServings)

# Objective 
# @Objective Objective @Def: The total fat intake is FatApple * number of apple servings + FatCarrot * number of carrot servings. The objective is to maximize the total fat intake.
model.setObjective(FatApple * AppleServings + FatCarrot * CarrotServings, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['AppleServings'] = AppleServings.x
variables['CarrotServings'] = CarrotServings.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
