# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Minimize CostProteinBars * x + CostNoodles * y subject to CaloriesProteinBars *
x + CaloriesNoodles * y ≥ MinCalories and ProteinProteinBars * x +
ProteinNoodles * y ≥ MinProtein, where x and y are non-negative variables
representing the number of servings of protein bars and noodles respectively.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/195/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CostNoodles @Def: Cost per serving of noodles @Shape: [] 
CostNoodles = data['CostNoodles']
# @Parameter CostProteinBars @Def: Cost per serving of protein bars @Shape: [] 
CostProteinBars = data['CostProteinBars']
# @Parameter CaloriesNoodles @Def: Calories per serving of noodles @Shape: [] 
CaloriesNoodles = data['CaloriesNoodles']
# @Parameter CaloriesProteinBars @Def: Calories per serving of protein bars @Shape: [] 
CaloriesProteinBars = data['CaloriesProteinBars']
# @Parameter ProteinNoodles @Def: Protein per serving of noodles @Shape: [] 
ProteinNoodles = data['ProteinNoodles']
# @Parameter ProteinProteinBars @Def: Protein per serving of protein bars @Shape: [] 
ProteinProteinBars = data['ProteinProteinBars']
# @Parameter MinCalories @Def: Minimum required calories per day @Shape: [] 
MinCalories = data['MinCalories']
# @Parameter MinProtein @Def: Minimum required protein per day @Shape: [] 
MinProtein = data['MinProtein']

# Variables 
# @Variable ServingsNoodles @Def: The number of servings of noodles @Shape: [] 
ServingsNoodles = model.addVar(vtype=GRB.CONTINUOUS, name="ServingsNoodles")
# @Variable ServingsProteinBars @Def: The number of servings of protein bars @Shape: [] 
ServingsProteinBars = model.addVar(vtype=GRB.CONTINUOUS, name="ServingsProteinBars")

# Constraints 
# @Constraint Constr_1 @Def: The total calories from protein bars and noodles must be at least MinCalories.
model.addConstr(CaloriesNoodles * ServingsNoodles + CaloriesProteinBars * ServingsProteinBars >= MinCalories)
# @Constraint Constr_2 @Def: The total protein from protein bars and noodles must be at least MinProtein.
model.addConstr(ProteinNoodles * ServingsNoodles + ProteinProteinBars * ServingsProteinBars >= MinProtein)

# Objective 
# @Objective Objective @Def: The objective is to minimize the total cost of protein bars and noodles while meeting the minimum daily calorie and protein requirements.
model.setObjective(CostNoodles * ServingsNoodles + CostProteinBars * ServingsProteinBars, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ServingsNoodles'] = ServingsNoodles.x
variables['ServingsProteinBars'] = ServingsProteinBars.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
