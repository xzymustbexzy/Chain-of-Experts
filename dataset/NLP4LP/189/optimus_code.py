# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A meat processing plant utilizes NumMachines different machines to produce
NumProducts products. The time required on each machine to produce one batch of
each product is specified by TimeRequired. Each machine is available for no more
than MaxHours hours per year. The profit obtained per batch for each product is
ProfitPerBatch. The objective is to determine the number of batches of each
product to produce in order to maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/190/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumProducts @Def: Number of products @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter NumMachines @Def: Number of machines @Shape: [] 
NumMachines = data['NumMachines']
# @Parameter ProfitPerBatch @Def: Profit per batch of each product @Shape: ['NumProducts'] 
ProfitPerBatch = data['ProfitPerBatch']
# @Parameter TimeRequired @Def: Time required on each machine to produce one batch of each product @Shape: ['NumMachines', 'NumProducts'] 
TimeRequired = data['TimeRequired']
# @Parameter MaxHours @Def: Maximum available hours per year for each machine @Shape: ['NumMachines'] 
MaxHours = data['MaxHours']
    
# Variables 
# @Variable BatchesProduced @Def: The number of batches of each product to produce @Shape: ['NumProducts'] 
BatchesProduced = model.addVars(NumProducts, vtype=GRB.CONTINUOUS, name="BatchesProduced")
    
# Constraints 
# @Constraint Constr_1 @Def: For each machine, the total time required to produce all batches of each product does not exceed the machine's maximum available hours per year.
for m in range(NumMachines):
    model.addConstr(quicksum(TimeRequired[m][p] * BatchesProduced[p] for p in range(NumProducts)) <= MaxHours[m])
    
# Objective 
# @Objective Objective @Def: Maximize the total profit obtained from producing the batches of each product.
model.setObjective(quicksum(ProfitPerBatch[i] * BatchesProduced[i] for i in range(NumProducts)), GRB.MAXIMIZE)
    
# Solve 
model.optimize()
    
# Extract solution 
solution = {}
variables = {}
objective = []
variables['BatchesProduced'] = {p: BatchesProduced[p].X for p in range(NumProducts)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)