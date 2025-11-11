# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Jordan aims to minimize the total cost of his diet by selecting servings of Rice
and Kebab. Each serving of Rice and Kebab costs CostRice and CostKebab
respectively. The diet must provide at least MinCalories in calories and at
least MinProtein in protein per day. Each serving of Rice and Kebab contributes
CaloriesRice and CaloriesKebab calories, and ProteinRice and ProteinKebab grams
of protein respectively.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/33/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CostRice @Def: Cost per serving of Rice @Shape: [] 
CostRice = data['CostRice']
# @Parameter CostKebab @Def: Cost per serving of Kebab @Shape: [] 
CostKebab = data['CostKebab']
# @Parameter CaloriesRice @Def: Calories per serving of Rice @Shape: [] 
CaloriesRice = data['CaloriesRice']
# @Parameter CaloriesKebab @Def: Calories per serving of Kebab @Shape: [] 
CaloriesKebab = data['CaloriesKebab']
# @Parameter ProteinRice @Def: Protein per serving of Rice @Shape: [] 
ProteinRice = data['ProteinRice']
# @Parameter ProteinKebab @Def: Protein per serving of Kebab @Shape: [] 
ProteinKebab = data['ProteinKebab']
# @Parameter MinCalories @Def: Minimum daily calories required @Shape: [] 
MinCalories = data['MinCalories']
# @Parameter MinProtein @Def: Minimum daily protein required @Shape: [] 
MinProtein = data['MinProtein']

# Variables 
# @Variable ServingsRice @Def: The number of servings of Rice @Shape: [] 
ServingsRice = model.addVar(vtype=GRB.CONTINUOUS, name="ServingsRice")
# @Variable ServingsKebab @Def: The number of servings of Kebab @Shape: [] 
ServingsKebab = model.addVar(vtype=GRB.CONTINUOUS, name="ServingsKebab")

# Constraints 
# @Constraint Constr_1 @Def: The diet must provide at least MinCalories in calories.
model.addConstr(ServingsRice * CaloriesRice + ServingsKebab * CaloriesKebab >= MinCalories)
# @Constraint Constr_2 @Def: The diet must provide at least MinProtein in protein.
model.addConstr(ProteinRice * ServingsRice + ProteinKebab * ServingsKebab >= MinProtein)

# Objective 
# @Objective Objective @Def: Minimize the total cost of the diet, calculated as CostRice multiplied by the number of servings of Rice plus CostKebab multiplied by the number of servings of Kebab.
model.setObjective(CostRice * ServingsRice + CostKebab * ServingsKebab, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ServingsRice'] = ServingsRice.x
variables['ServingsKebab'] = ServingsKebab.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
