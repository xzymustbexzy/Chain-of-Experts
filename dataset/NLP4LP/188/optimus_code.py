# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A company offers NumFoods different food items, each with an associated Price
and containing specific amounts of NumNutrients nutrients as defined by the
NutrientContent matrix. The company must ensure that the combination of selected
food items provides at least the minimum required amount for each nutrient,
specified by MinNutrient. The objective is to determine the selection of food
items that satisfies all nutrient requirements while minimizing the total Price.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/189/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumFoods @Def: Number of food items @Shape: [] 
NumFoods = data['NumFoods']
# @Parameter NumNutrients @Def: Number of nutrients @Shape: [] 
NumNutrients = data['NumNutrients']
# @Parameter MinNutrient @Def: Minimum required amount for each nutrient @Shape: ['NumNutrients'] 
MinNutrient = data['MinNutrient']
# @Parameter Price @Def: Price of each food item @Shape: ['NumFoods'] 
Price = data['Price']
# @Parameter NutrientContent @Def: Amount of each nutrient in each food item @Shape: ['NumNutrients', 'NumFoods'] 
NutrientContent = data['NutrientContent']

# Variables 
# @Variable Quantity @Def: The quantity of each food item @Shape: ['NumFoods'] 
Quantity = model.addVars(NumFoods, vtype=GRB.CONTINUOUS, name="Quantity")

# Constraints 
# @Constraint Constr_1 @Def: The combination of selected food items provides at least the minimum required amount for each nutrient as specified by MinNutrient.
for n in range(NumNutrients):
    model.addConstr(quicksum(NutrientContent[n][f] * Quantity[f] for f in range(NumFoods)) >= MinNutrient[n])

# Objective 
# @Objective Objective @Def: Minimize the total Price of the selected food items while satisfying all nutrient requirements.
model.setObjective(quicksum(Price[i] * Quantity[i] for i in range(NumFoods)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Quantity'] = model.getAttr("X", Quantity)
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
