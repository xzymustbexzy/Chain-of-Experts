# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A patient selects non-negative quantities of each of the NumPillTypes pill
types. Each pill type provides specific amounts of each of the NumMedicineTypes
medicine types as defined by AmountPerPill. The total amount of each medicine
must meet or exceed the RequiredAmount. The objective is to minimize the total
cost, calculated using PillCost.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/25/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumPillTypes @Def: Number of different pill types @Shape: [] 
NumPillTypes = data['NumPillTypes']
# @Parameter NumMedicineTypes @Def: Number of different medicine types @Shape: [] 
NumMedicineTypes = data['NumMedicineTypes']
# @Parameter AmountPerPill @Def: Amount of a medicine type per pill type @Shape: ['NumMedicineTypes', 'NumPillTypes'] 
AmountPerPill = data['AmountPerPill']
# @Parameter PillCost @Def: Cost per pill type @Shape: ['NumPillTypes'] 
PillCost = data['PillCost']
# @Parameter RequiredAmount @Def: Required amount of a medicine type @Shape: ['NumMedicineTypes'] 
RequiredAmount = data['RequiredAmount']

# Variables 
# @Variable PillsSelected @Def: The number of pills selected for each pill type @Shape: ['NumPillTypes'] 
PillsSelected = model.addVars(NumPillTypes, vtype=GRB.CONTINUOUS, name="PillsSelected")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of each medicine type provided by the selected pills must meet or exceed the RequiredAmount.
model.addConstrs((quicksum(AmountPerPill[i][j] * PillsSelected[j] for j in range(NumPillTypes)) >= RequiredAmount[i] for i in range(NumMedicineTypes)), "MedicineRequirements")
# @Constraint Constr_2 @Def: The quantity of each pill type selected must be non-negative.
model.addConstrs((PillsSelected[k] >= 0 for k in range(NumPillTypes)), name='NonNegativity')

# Objective 
# @Objective Objective @Def: Minimize the total cost, calculated using PillCost.
model.setObjective(quicksum(PillCost[i] * PillsSelected[i] for i in range(NumPillTypes)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['PillsSelected'] = {k: v.x for k, v in PillsSelected.items()}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)