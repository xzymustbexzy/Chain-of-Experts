# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A lab has TotalMedicinalIngredients units of medicinal ingredients available to
produce NumPillTypes different types of pills. Each pill type i requires
RequiredMedicinal[i] units of medicinal ingredients and RequiredFiller[i] units
of filler. The lab must produce at least MinimumPills[i] units of pill type i.
Additionally, at least MinimumProportion[i] of the total number of pills
produced must be of pill type i. The objective is to determine the number of
each pill type to minimize the total filler material used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/133/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
            
# Parameters 
# @Parameter TotalMedicinalIngredients @Def: Total units of medicinal ingredients available to produce pills @Shape: [] 
TotalMedicinalIngredients = data['TotalMedicinalIngredients']
# @Parameter NumPillTypes @Def: Number of different pill types @Shape: [] 
NumPillTypes = data['NumPillTypes']
# @Parameter RequiredMedicinal @Def: Units of medicinal ingredients required to produce one unit of pill type i @Shape: ['NumPillTypes'] 
RequiredMedicinal = data['RequiredMedicinal']
# @Parameter RequiredFiller @Def: Units of filler required to produce one unit of pill type i @Shape: ['NumPillTypes'] 
RequiredFiller = data['RequiredFiller']
# @Parameter MinimumPills @Def: Minimum number of pills that must be produced for pill type i @Shape: ['NumPillTypes'] 
MinimumPills = data['MinimumPills']
# @Parameter MinimumProportion @Def: Minimum proportion of total pills that must be of pill type i @Shape: ['NumPillTypes'] 
MinimumProportion = data['MinimumProportion']

# Variables 
# @Variable PillsProduced @Def: The number of pills produced for each pill type @Shape: ['NumPillTypes'] 
PillsProduced = model.addVars(NumPillTypes, vtype=GRB.INTEGER, name="PillsProduced")

# Constraints 
# @Constraint Constr_1 @Def: The total medicinal ingredients used cannot exceed TotalMedicinalIngredients.
model.addConstr(quicksum(RequiredMedicinal[i] * PillsProduced[i] for i in range(NumPillTypes)) <= TotalMedicinalIngredients)
# @Constraint Constr_2 @Def: For each pill type i, at least MinimumPills[i] units must be produced.
model.addConstrs((PillsProduced[i] >= MinimumPills[i] for i in range(NumPillTypes)), "MinPills")
# @Constraint Constr_3 @Def: For each pill type i, at least MinimumProportion[i] of the total pills produced must be of pill type i.
model.addConstrs((PillsProduced[i] >= MinimumProportion[i] * quicksum(PillsProduced[j] for j in range(NumPillTypes)) for i in range(NumPillTypes)), 'MinimumProportion')

# Objective 
# @Objective Objective @Def: Minimize the total filler material used, which is the sum of RequiredFiller[i] multiplied by the number of pills produced for each pill type i.
model.setObjective(quicksum(RequiredFiller[i] * PillsProduced[i] for i in range(NumPillTypes)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['PillsProduced'] = {i: PillsProduced[i].x for i in range(NumPillTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)