# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Super Shop sells two types of snack mixes. The first mix contains
PercentageCatPawMix1 of cat paw snacks and a corresponding percentage of gold
shark snacks. The second mix contains PercentageCatPawMix2 of cat paw snacks and
a corresponding percentage of gold shark snacks. The store has AvailableCatPawKg
kilograms of cat paw snacks and AvailableGoldSharkKg kilograms of gold shark
snacks available. The profit per kilogram of the first mix is ProfitPerKgMix1
and the profit per kilogram of the second mix is ProfitPerKgMix2. Determine the
number of kilograms of each mix to prepare in order to maximize profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/207/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter PercentageCatPawMix1 @Def: Percentage of cat paw snacks in the first mix @Shape: [] 
PercentageCatPawMix1 = data['PercentageCatPawMix1']
# @Parameter PercentageCatPawMix2 @Def: Percentage of cat paw snacks in the second mix @Shape: [] 
PercentageCatPawMix2 = data['PercentageCatPawMix2']
# @Parameter AvailableCatPawKg @Def: Available kilograms of cat paw snacks @Shape: [] 
AvailableCatPawKg = data['AvailableCatPawKg']
# @Parameter AvailableGoldSharkKg @Def: Available kilograms of gold shark snacks @Shape: [] 
AvailableGoldSharkKg = data['AvailableGoldSharkKg']
# @Parameter ProfitPerKgMix1 @Def: Profit per kilogram of the first mix @Shape: [] 
ProfitPerKgMix1 = data['ProfitPerKgMix1']
# @Parameter ProfitPerKgMix2 @Def: Profit per kilogram of the second mix @Shape: [] 
ProfitPerKgMix2 = data['ProfitPerKgMix2']

# Variables 
# @Variable Mix1 @Def: The quantity of the first mix in kilograms @Shape: [] 
Mix1 = model.addVar(vtype=GRB.CONTINUOUS, name="Mix1")
# @Variable Mix2 @Def: The quantity of the second mix in kilograms @Shape: [] 
Mix2 = model.addVar(vtype=GRB.CONTINUOUS, name="Mix2")

# Constraints 
# @Constraint Constr_1 @Def: The total cat paw snacks used in both mixes must not exceed AvailableCatPawKg kilograms, calculated as (PercentageCatPawMix1 * Mix1) + (PercentageCatPawMix2 * Mix2).
model.addConstr(PercentageCatPawMix1 * Mix1 + PercentageCatPawMix2 * Mix2 <= AvailableCatPawKg)
# @Constraint Constr_2 @Def: The total gold shark snacks used in both mixes must not exceed AvailableGoldSharkKg kilograms, calculated as ((100 - PercentageCatPawMix1) * Mix1) + ((100 - PercentageCatPawMix2) * Mix2).
model.addConstr(((100 - PercentageCatPawMix1) / 100) * Mix1 + ((100 - PercentageCatPawMix2) / 100) * Mix2 <= AvailableGoldSharkKg)

# Objective 
# @Objective Objective @Def: The objective is to maximize the total profit, calculated as (ProfitPerKgMix1 * Mix1) + (ProfitPerKgMix2 * Mix2).
model.setObjective(ProfitPerKgMix1 * Mix1 + ProfitPerKgMix2 * Mix2, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Mix1'] = Mix1.x
variables['Mix2'] = Mix2.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
