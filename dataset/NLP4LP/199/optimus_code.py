# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A company processes NumOilTypes different types of crude oil. Each type of crude
oil generates a NetRevenue per tank processed. Processing one tank of each type
of crude oil requires specific amounts of each of the NumCompounds compounds, as
defined by the CompoundRequirement matrix. The company has a limited supply of
each compound, specified by TotalCompoundAvailable. The objective is to
determine the number of full or partial tanks of each type of crude oil to
process in order to maximize the total NetRevenue.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/200/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumOilTypes @Def: Number of different types of crude oil @Shape: [] 
NumOilTypes = data['NumOilTypes']
# @Parameter NumCompounds @Def: Number of different compounds required to process oil @Shape: [] 
NumCompounds = data['NumCompounds']
# @Parameter NetRevenue @Def: Net revenue per tank for each type of crude oil @Shape: ['NumOilTypes'] 
NetRevenue = data['NetRevenue']
# @Parameter CompoundRequirement @Def: Amount of each compound required to process one tank of each type of crude oil @Shape: ['NumCompounds', 'NumOilTypes'] 
CompoundRequirement = data['CompoundRequirement']
# @Parameter TotalCompoundAvailable @Def: Total units of each compound available for processing @Shape: ['NumCompounds'] 
TotalCompoundAvailable = data['TotalCompoundAvailable']

# Variables 
# @Variable NumTanksProcessed @Def: The number of tanks processed for each type of crude oil @Shape: ['NumOilTypes'] 
NumTanksProcessed = model.addVars(NumOilTypes, vtype=GRB.CONTINUOUS, name="NumTanksProcessed")

# Constraints 
# @Constraint Constr_1 @Def: Processing one tank of each type of crude oil requires specific amounts of each compound as defined by the CompoundRequirement matrix. The total usage of each compound cannot exceed the TotalCompoundAvailable.
model.addConstrs(
    (quicksum(CompoundRequirement[c][o] * NumTanksProcessed[o] for o in range(NumOilTypes)) <= TotalCompoundAvailable[c] for c in range(NumCompounds)),
    name="CompoundUsage"
)

# Objective 
# @Objective Objective @Def: Total NetRevenue is the sum of the NetRevenue per tank for each type of crude oil processed. The objective is to maximize the total NetRevenue.
model.setObjective(quicksum(NetRevenue[i] * NumTanksProcessed[i] for i in range(NumOilTypes)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumTanksProcessed'] = {o: NumTanksProcessed[o].X for o in range(NumOilTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)