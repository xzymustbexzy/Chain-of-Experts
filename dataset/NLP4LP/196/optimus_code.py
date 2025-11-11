# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Forest Paper produces NumProducts different types of products using NumMachines
different machine types. Each product requires a specific amount of time on each
machine, as defined by TimeRequired. Each machine type has a limited
AvailableTime per day. The company aims to determine the number of each product
to produce in order to maximize total profit, given the ProfitPerProduct for
each product.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/197/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumProducts @Def: Number of different products manufactured @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter NumMachines @Def: Number of different machine types @Shape: [] 
NumMachines = data['NumMachines']
# @Parameter TimeRequired @Def: Time required by each machine to produce each product @Shape: ['NumMachines', 'NumProducts'] 
TimeRequired = data['TimeRequired']
# @Parameter AvailableTime @Def: Available time per machine per day @Shape: ['NumMachines'] 
AvailableTime = data['AvailableTime']
# @Parameter ProfitPerProduct @Def: Profit per product @Shape: ['NumProducts'] 
ProfitPerProduct = data['ProfitPerProduct']

# Variables 
# @Variable ProductionQuantity @Def: The quantity of each product to produce @Shape: ['NumProducts'] 
ProductionQuantity = model.addVars(NumProducts, vtype=GRB.CONTINUOUS, name="ProductionQuantity")

# Constraints 
# @Constraint Constr_1 @Def: For each machine type, the total time required to produce all products cannot exceed the AvailableTime per day.
model.addConstrs((quicksum(TimeRequired[i][j] * ProductionQuantity[j] for j in range(NumProducts)) <= AvailableTime[i] for i in range(NumMachines)), name="MachineTime")

# Objective 
# @Objective Objective @Def: Total profit is the sum of ProfitPerProduct for each product multiplied by the number of each product produced. The objective is to maximize the total profit.
model.setObjective(quicksum(ProfitPerProduct[j] * ProductionQuantity[j] for j in range(NumProducts)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ProductionQuantity'] = {j: ProductionQuantity[j].X for j in range(NumProducts)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)