# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A woman consumes servings of NumNutTypes different types of nuts to satisfy at
least CalorieRequirement calories and ProteinRequirement grams of protein per
week. Each nut type has specific CaloriePerServing, ProteinPerServing, and
FatPerServing per serving. She must consume at least ServingRatioMultiplier
times as many servings of one nut type as another. The objective is to minimize
her total fat intake.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/117/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumNutTypes @Def: Number of different nut types @Shape: [] 
NumNutTypes = data['NumNutTypes']
# @Parameter CaloriePerServing @Def: Calories in one serving of each nut type @Shape: ['NumNutTypes'] 
CaloriePerServing = data['CaloriePerServing']
# @Parameter ProteinPerServing @Def: Protein in one serving of each nut type @Shape: ['NumNutTypes'] 
ProteinPerServing = data['ProteinPerServing']
# @Parameter FatPerServing @Def: Fat in one serving of each nut type @Shape: ['NumNutTypes'] 
FatPerServing = data['FatPerServing']
# @Parameter ServingRatioMultiplier @Def: Minimum ratio of servings of almonds to cashews @Shape: [] 
ServingRatioMultiplier = data['ServingRatioMultiplier']
# @Parameter CalorieRequirement @Def: Total calorie intake requirement @Shape: [] 
CalorieRequirement = data['CalorieRequirement']
# @Parameter ProteinRequirement @Def: Total protein intake requirement @Shape: [] 
ProteinRequirement = data['ProteinRequirement']
    
# Variables 
# @Variable NutServings @Def: The number of servings for each nut type @Shape: ['NumNutTypes'] 
NutServings = model.addVars(NumNutTypes, vtype=GRB.CONTINUOUS, name="NutServings")
    
# Constraints 
# @Constraint Constr_1 @Def: The total calorie intake from all nut servings must be at least CalorieRequirement.
model.addConstr(quicksum(CaloriePerServing[i] * NutServings[i] for i in range(NumNutTypes)) >= CalorieRequirement)
# @Constraint Constr_2 @Def: The total protein intake from all nut servings must be at least ProteinRequirement.
model.addConstr(quicksum(ProteinPerServing[i] * NutServings[i] for i in range(NumNutTypes)) >= ProteinRequirement)
# @Constraint Constr_3 @Def: She must consume at least ServingRatioMultiplier times as many servings of almonds as cashews.
model.addConstr(NutServings[0] >= ServingRatioMultiplier * NutServings[1])
    
# Objective 
# @Objective Objective @Def: Total fat intake is the sum of the fat from all consumed nut servings. The objective is to minimize the total fat intake.
model.setObjective(quicksum(NutServings[i] * FatPerServing[i] for i in range(NumNutTypes)), GRB.MINIMIZE)
    
# Solve 
model.optimize()
    
# Extract solution 
solution = {}
variables = {}
objective = []
variables['NutServings'] = {i: NutServings[i].x for i in range(NumNutTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)