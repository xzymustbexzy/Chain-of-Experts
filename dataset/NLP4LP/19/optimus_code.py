# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A factory has TotalSpace square feet of available space. It produces
NumberOfProducts different products. Each product requires LaborRequiredPerSqFt
labor hours per square foot and costs CostPerSqFt dollars per square foot to
produce. Each product generates RevenuePerSqFt dollars of net revenue per square
foot. The factory aims to spend at most Budget dollars and has at most
LaborHoursAvailable labor hours. The objective is to determine the allocation of
space to each product to maximize revenue.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/20/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter TotalSpace @Def: Total available space in square feet @Shape: [] 
TotalSpace = data['TotalSpace']
# @Parameter Budget @Def: Maximum allowed budget in dollars @Shape: [] 
Budget = data['Budget']
# @Parameter LaborHoursAvailable @Def: Maximum available labor hours @Shape: [] 
LaborHoursAvailable = data['LaborHoursAvailable']
# @Parameter NumberOfProducts @Def: Number of products produced @Shape: [] 
NumberOfProducts = data['NumberOfProducts']
# @Parameter LaborRequiredPerSqFt @Def: Labor hours required per square foot for each product @Shape: ['NumberOfProducts'] 
LaborRequiredPerSqFt = data['LaborRequiredPerSqFt']
# @Parameter CostPerSqFt @Def: Cost per square foot for each product @Shape: ['NumberOfProducts'] 
CostPerSqFt = data['CostPerSqFt']
# @Parameter RevenuePerSqFt @Def: Net revenue per square foot for each product @Shape: ['NumberOfProducts'] 
RevenuePerSqFt = data['RevenuePerSqFt']

# Variables 
# @Variable AllocatedSpace @Def: The allocated space for each product @Shape: ['NumberOfProducts'] 
AllocatedSpace = model.addVars(NumberOfProducts, vtype=GRB.CONTINUOUS, name="AllocatedSpace")

# Constraints 
# @Constraint Constr_1 @Def: The total allocated space for all products cannot exceed TotalSpace square feet.
model.addConstr(quicksum(AllocatedSpace[i] for i in range(NumberOfProducts)) <= TotalSpace)
# @Constraint Constr_2 @Def: The total production cost, calculated as the sum of CostPerSqFt multiplied by the allocated space for each product, cannot exceed Budget dollars.
model.addConstr(quicksum(CostPerSqFt[i] * AllocatedSpace[i] for i in range(NumberOfProducts)) <= Budget)
# @Constraint Constr_3 @Def: The total labor hours required, calculated as the sum of LaborRequiredPerSqFt multiplied by the allocated space for each product, cannot exceed LaborHoursAvailable labor hours.
model.addConstr(quicksum(LaborRequiredPerSqFt[i] * AllocatedSpace[i] for i in range(NumberOfProducts)) <= LaborHoursAvailable)

# Objective 
# @Objective Objective @Def: Total revenue is the sum of the net revenue per square foot for each product multiplied by the allocated space for each product. The objective is to maximize total revenue.
model.setObjective(quicksum(RevenuePerSqFt[i] * AllocatedSpace[i] for i in range(NumberOfProducts)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['AllocatedSpace'] = {i: AllocatedSpace[i].x for i in range(NumberOfProducts)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)