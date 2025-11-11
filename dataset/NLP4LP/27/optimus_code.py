# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A nutritionist is creating a mix using NumDrinks different drinks. The mix must
contain at least the minimum required units specified by MinRequirements for
certain vitamins and at most the maximum allowed units specified by
MaxRequirements for other vitamins. Each cup of each drink provides amounts of
each vitamin as defined in VitaminContent. The goal is to determine the number
of cups of each drink to minimize the total units of a specific vitamin.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/28/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumVitamins @Def: Number of different vitamins @Shape: [] 
NumVitamins = data['NumVitamins']
# @Parameter NumDrinks @Def: Number of different drinks @Shape: [] 
NumDrinks = data['NumDrinks']
# @Parameter MinRequirements @Def: Minimum required units for each vitamin @Shape: ['NumVitamins'] 
MinRequirements = data['MinRequirements']
# @Parameter MaxRequirements @Def: Maximum allowed units for each vitamin @Shape: ['NumVitamins'] 
MaxRequirements = data['MaxRequirements']
# @Parameter VitaminContent @Def: Amount of each vitamin per cup of each drink @Shape: ['NumVitamins', 'NumDrinks'] 
VitaminContent = data['VitaminContent']

# Variables 
# @Variable DrinkCups @Def: The number of cups selected for each drink @Shape: ['NumDrinks'] 
DrinkCups = model.addVars(range(NumDrinks), vtype=GRB.CONTINUOUS, name="DrinkCups")

# Constraints 
# @Constraint Constr_1 @Def: The mix must contain at least the minimum required units specified by MinRequirements for certain vitamins.
model.addConstrs((quicksum(VitaminContent[i][j] * DrinkCups[j] for j in range(NumDrinks)) >= MinRequirements[i] for i in range(NumVitamins)), name="MinVitamin")
# @Constraint Constr_2 @Def: The mix must contain at most the maximum allowed units specified by MaxRequirements for other vitamins.
model.addConstrs(
    (quicksum(VitaminContent[v][d] * DrinkCups[d] for d in range(NumDrinks)) <= MaxRequirements[v] for v in range(NumVitamins)),
    name="MaxVitaminRequirements"
)

# Objective 
# @Objective Objective @Def: Minimize the total units of Vitamin K in the mix.
model.setObjective(quicksum(VitaminContent[K, j] * DrinkCups[j] for j in range(NumDrinks)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['DrinkCups'] = DrinkCups.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
