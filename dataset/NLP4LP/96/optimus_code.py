# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A patient selects a number of FishMeals and ChickenMeals to minimize the total
fat intake, which is calculated as FatPerFishMeal multiplied by FishMeals plus
FatPerChickenMeal multiplied by ChickenMeals. This selection must satisfy the
following constraints: the total protein intake, calculated as
ProteinPerFishMeal multiplied by FishMeals plus ProteinPerChickenMeal multiplied
by ChickenMeals, must be at least MinimumProtein; the total iron intake,
calculated as IronPerFishMeal multiplied by FishMeals plus IronPerChickenMeal
multiplied by ChickenMeals, must be at least MinimumIron; and the number of
ChickenMeals must be at least ChickenToFishRatio multiplied by the number of
FishMeals.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/97/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProteinPerFishMeal @Def: Protein per fish meal @Shape: [] 
ProteinPerFishMeal = data['ProteinPerFishMeal']
# @Parameter ProteinPerChickenMeal @Def: Protein per chicken meal @Shape: [] 
ProteinPerChickenMeal = data['ProteinPerChickenMeal']
# @Parameter IronPerFishMeal @Def: Iron per fish meal @Shape: [] 
IronPerFishMeal = data['IronPerFishMeal']
# @Parameter IronPerChickenMeal @Def: Iron per chicken meal @Shape: [] 
IronPerChickenMeal = data['IronPerChickenMeal']
# @Parameter FatPerFishMeal @Def: Fat per fish meal @Shape: [] 
FatPerFishMeal = data['FatPerFishMeal']
# @Parameter FatPerChickenMeal @Def: Fat per chicken meal @Shape: [] 
FatPerChickenMeal = data['FatPerChickenMeal']
# @Parameter MinimumProtein @Def: Minimum required protein @Shape: [] 
MinimumProtein = data['MinimumProtein']
# @Parameter MinimumIron @Def: Minimum required iron @Shape: [] 
MinimumIron = data['MinimumIron']
# @Parameter ChickenToFishRatio @Def: Minimum ratio of chicken meals to fish meals @Shape: [] 
ChickenToFishRatio = data['ChickenToFishRatio']

# Variables 
# @Variable FishMeals @Def: The number of fish meals @Shape: [] 
FishMeals = model.addVar(vtype=GRB.CONTINUOUS, name="FishMeals")
# @Variable ChickenMeals @Def: The number of chicken meals @Shape: [] 
ChickenMeals = model.addVar(vtype=GRB.INTEGER, name="ChickenMeals")

# Constraints 
# @Constraint Constr_1 @Def: The total protein intake, calculated as ProteinPerFishMeal multiplied by FishMeals plus ProteinPerChickenMeal multiplied by ChickenMeals, must be at least MinimumProtein.
model.addConstr(ProteinPerFishMeal * FishMeals + ProteinPerChickenMeal * ChickenMeals >= MinimumProtein)
# @Constraint Constr_2 @Def: The total iron intake, calculated as IronPerFishMeal multiplied by FishMeals plus IronPerChickenMeal multiplied by ChickenMeals, must be at least MinimumIron.
model.addConstr(IronPerFishMeal * FishMeals + IronPerChickenMeal * ChickenMeals >= MinimumIron)
# @Constraint Constr_3 @Def: The number of ChickenMeals must be at least ChickenToFishRatio multiplied by the number of FishMeals.
model.addConstr(ChickenMeals >= ChickenToFishRatio * FishMeals)

# Objective 
# @Objective Objective @Def: Minimize the total fat intake, calculated as FatPerFishMeal multiplied by FishMeals plus FatPerChickenMeal multiplied by ChickenMeals.
model.setObjective(FatPerFishMeal * FishMeals + FatPerChickenMeal * ChickenMeals, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['FishMeals'] = FishMeals.x
variables['ChickenMeals'] = ChickenMeals.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
