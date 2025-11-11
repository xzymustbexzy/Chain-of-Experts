# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A candy store prepares NumMixes different candy mixes using NumCandyTypes
different types of candy. Each kilogram of each mix requires specific amounts of
each candy type as defined by CompositionRequired. The profit per kilogram of
each mix is given by ProfitPerMix. The store has AvailableCandy kilograms of
each candy type available. Determine the quantities of each mix to produce to
maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/19/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumMixes @Def: Number of different candy mixes prepared @Shape: [] 
NumMixes = data['NumMixes']
# @Parameter NumCandyTypes @Def: Number of different candy types used @Shape: [] 
NumCandyTypes = data['NumCandyTypes']
# @Parameter CompositionRequired @Def: Amount of each candy type required per kilogram of each mix @Shape: ['NumCandyTypes', 'NumMixes'] 
CompositionRequired = data['CompositionRequired']
# @Parameter ProfitPerMix @Def: Profit per kilogram of each mix @Shape: ['NumMixes'] 
ProfitPerMix = data['ProfitPerMix']
# @Parameter AvailableCandy @Def: Amount of each candy type available @Shape: ['NumCandyTypes'] 
AvailableCandy = data['AvailableCandy']

# Variables 
# @Variable ProductionMix @Def: The quantity of each mix produced (in kilograms) @Shape: ['NumMixes'] 
ProductionMix = model.addVars(NumMixes, vtype=GRB.CONTINUOUS, name="ProductionMix")

# Constraints 
# @Constraint Constr_1 @Def: Each kilogram of each mix requires specific amounts of each candy type as defined by CompositionRequired.
model.addConstrs((quicksum(CompositionRequired[j][i] * ProductionMix[i] for i in range(NumMixes)) <= AvailableCandy[j] for j in range(NumCandyTypes)), name="CandySupply")
# @Constraint Constr_2 @Def: The total usage of each candy type across all mixes cannot exceed the available amount AvailableCandy.
model.addConstrs((quicksum(CompositionRequired[c][m] * ProductionMix[m] for m in range(NumMixes)) <= AvailableCandy[c] for c in range(NumCandyTypes)), name="CandyUsage")

# Objective 
# @Objective Objective @Def: Total profit is the sum of the profit per kilogram of each mix multiplied by the quantities produced. The objective is to maximize the total profit.
model.setObjective(quicksum(ProductionMix[i] * ProfitPerMix[i] for i in range(NumMixes)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ProductionMix'] = {i: ProductionMix[i].X for i in range(NumMixes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)