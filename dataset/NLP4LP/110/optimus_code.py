# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A salesman chooses quantities of ramen packs and fries packs to minimize the
total sodium intake, which is the sum of SodiumPerRamenPack multiplied by the
number of ramen packs and SodiumPerFriesPack multiplied by the number of fries
packs. He must ensure that the total calories from ramen and fries are at least
MinCalories, the total protein is at least MinProtein, and the number of ramen
packs does not exceed MaxRamenMealRatio proportion of the total meals. All
quantities of ramen and fries packs must be non-negative.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/111/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CaloriesPerRamenPack @Def: Calories per pack of ramen @Shape: [] 
CaloriesPerRamenPack = data['CaloriesPerRamenPack']
# @Parameter ProteinPerRamenPack @Def: Protein per pack of ramen @Shape: [] 
ProteinPerRamenPack = data['ProteinPerRamenPack']
# @Parameter SodiumPerRamenPack @Def: Sodium per pack of ramen @Shape: [] 
SodiumPerRamenPack = data['SodiumPerRamenPack']
# @Parameter CaloriesPerFriesPack @Def: Calories per pack of fries @Shape: [] 
CaloriesPerFriesPack = data['CaloriesPerFriesPack']
# @Parameter ProteinPerFriesPack @Def: Protein per pack of fries @Shape: [] 
ProteinPerFriesPack = data['ProteinPerFriesPack']
# @Parameter SodiumPerFriesPack @Def: Sodium per pack of fries @Shape: [] 
SodiumPerFriesPack = data['SodiumPerFriesPack']
# @Parameter MaxRamenMealRatio @Def: Maximum proportion of meals that can be ramen @Shape: [] 
MaxRamenMealRatio = data['MaxRamenMealRatio']
# @Parameter MinCalories @Def: Minimum calories required @Shape: [] 
MinCalories = data['MinCalories']
# @Parameter MinProtein @Def: Minimum protein required @Shape: [] 
MinProtein = data['MinProtein']

# Variables 
# @Variable NumRamenPacks @Def: The number of ramen packs @Shape: [] 
NumRamenPacks = model.addVar(vtype=GRB.INTEGER, name="NumRamenPacks")
# @Variable NumFriesPacks @Def: The number of fries packs @Shape: [] 
NumFriesPacks = model.addVar(vtype=GRB.INTEGER, name="NumFriesPacks")

# Constraints 
# @Constraint Constr_1 @Def: The total calories from ramen and fries must be at least MinCalories.
model.addConstr(CaloriesPerRamenPack * NumRamenPacks + CaloriesPerFriesPack * NumFriesPacks >= MinCalories)
# @Constraint Constr_2 @Def: The total protein from ramen and fries must be at least MinProtein.
model.addConstr(ProteinPerRamenPack * NumRamenPacks + ProteinPerFriesPack * NumFriesPacks >= MinProtein)
# @Constraint Constr_3 @Def: The number of ramen packs does not exceed MaxRamenMealRatio proportion of the total meals.
model.addConstr(NumRamenPacks <= MaxRamenMealRatio * (NumRamenPacks + NumFriesPacks))
# @Constraint Constr_4 @Def: Quantities of ramen and fries packs must be non-negative.
model.addConstr(NumRamenPacks >= 0)
model.addConstr(NumFriesPacks >= 0)

# Objective 
# @Objective Objective @Def: Minimize the total sodium intake, which is the sum of SodiumPerRamenPack multiplied by the number of ramen packs and SodiumPerFriesPack multiplied by the number of fries packs.
model.setObjective(SodiumPerRamenPack * NumRamenPacks + SodiumPerFriesPack * NumFriesPacks, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumRamenPacks'] = NumRamenPacks.x
variables['NumFriesPacks'] = NumFriesPacks.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
