# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A person purchases a number of each of NumSupplements supplement types to meet
the minimum requirements for NumNutrients nutrients. Each supplement type i
provides NutrientContent[i][j] units of nutrient j and has a cost of
CostPerPill[i] per pill. The objective is to minimize the total cost while
ensuring that for each nutrient j, the total obtained is at least
MinRequirement[j].
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/202/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumSupplements @Def: Number of supplement types @Shape: [] 
NumSupplements = data['NumSupplements']
# @Parameter NumNutrients @Def: Number of nutrient types @Shape: [] 
NumNutrients = data['NumNutrients']
# @Parameter NutrientContent @Def: Amount of nutrient j per pill of supplement i @Shape: ['NumSupplements', 'NumNutrients'] 
NutrientContent = data['NutrientContent']
# @Parameter MinRequirement @Def: Minimum required units of nutrient j @Shape: ['NumNutrients'] 
MinRequirement = data['MinRequirement']
# @Parameter CostPerPill @Def: Cost per pill of supplement i @Shape: ['NumSupplements'] 
CostPerPill = data['CostPerPill']

# Variables 
# @Variable NumPillsSupplement @Def: Number of pills of supplement i @Shape: ['NumSupplements'] 
NumPillsSupplement = model.addVars(NumSupplements, vtype=GRB.INTEGER, name="NumPillsSupplement")

# Constraints 
# @Constraint Constr_1 @Def: For each nutrient j, the total amount of nutrient j obtained from the supplements must be at least MinRequirement[j].
model.addConstrs((quicksum(NutrientContent[i][j] * NumPillsSupplement[i] for i in range(NumSupplements)) >= MinRequirement[j] for j in range(NumNutrients)))
# @Constraint Constr_2 @Def: The number of pills purchased for each supplement must be a non-negative integer.
model.addConstrs((NumPillsSupplement[i] >= 0 for i in range(NumSupplements)), 'NumPillsSupplementNonNeg')

# Objective 
# @Objective Objective @Def: Minimize the total cost, which is the sum of CostPerPill[i] multiplied by the number of pills purchased for each supplement i, while ensuring that for each nutrient j, the total obtained is at least MinRequirement[j].
model.setObjective(quicksum(CostPerPill[i] * NumPillsSupplement[i] for i in range(NumSupplements)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumPillsSupplement'] = {i: NumPillsSupplement[i].X for i in range(NumSupplements)}
solution['variables'] = variables
solution['objective'] = model.objVal if model.status == GRB.OPTIMAL else None
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
