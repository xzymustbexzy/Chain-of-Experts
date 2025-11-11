# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A car manufacturer produces NumOilTypes different types of car oils using
NumSubstances different substances. Each container of oil type requires specific
amounts of each substance as defined in SubstanceAmountPerContainer. The
manufacturer has AvailableSubstances amounts of each substance available. The
profit obtained from each container of oil type is specified in
ProfitPerContainer. The objective is to determine the number of containers to
produce for each oil type in order to maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/26/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumOilTypes @Def: Number of different types of car oils produced @Shape: [] 
NumOilTypes = data['NumOilTypes']
# @Parameter NumSubstances @Def: Number of different substances used in the car oils @Shape: [] 
NumSubstances = data['NumSubstances']
# @Parameter ProfitPerContainer @Def: Profit per container for each type of car oil @Shape: ['NumOilTypes'] 
ProfitPerContainer = data['ProfitPerContainer']
# @Parameter SubstanceAmountPerContainer @Def: Amount of each substance required per container of each type of car oil @Shape: ['NumSubstances', 'NumOilTypes'] 
SubstanceAmountPerContainer = data['SubstanceAmountPerContainer']
# @Parameter AvailableSubstances @Def: Available amount of each substance @Shape: ['NumSubstances'] 
AvailableSubstances = data['AvailableSubstances']

# Variables 
# @Variable xOilType @Def: The number of containers produced for each type of car oil @Shape: ['NumOilTypes'] 
xOilType = model.addVars(NumOilTypes, vtype=GRB.CONTINUOUS, name="xOilType")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of each substance used across all oil types cannot exceed the available amount of that substance.
model.addConstrs(
    (quicksum(SubstanceAmountPerContainer[s][t] * xOilType[t] for t in range(NumOilTypes)) <= AvailableSubstances[s]
     for s in range(NumSubstances)),
    name="SubstanceLimit"
)
# @Constraint Constr_2 @Def: The number of containers produced for each oil type must be a non-negative value.
model.addConstrs((xOilType[i] >= 0 for i in range(NumOilTypes)), "NonNegative")

# Objective 
# @Objective Objective @Def: Maximize the total profit obtained from producing the car oil containers by determining the optimal number of containers for each oil type.
model.setObjective(quicksum(ProfitPerContainer[o] * xOilType[o] for o in range(NumOilTypes)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['xOilType'] = [xOilType[t].X for t in range(NumOilTypes)]
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)