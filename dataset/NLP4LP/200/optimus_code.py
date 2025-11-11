# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A company produces two types of flooring products: laminate planks and carpets.
Let the production levels of laminate planks and carpets be represented by
variables. The objective is to maximize the total profit, which is calculated by
multiplying the production level of laminate planks by LaminateProfitPerSqFt and
the production level of carpets by CarpetProfitPerSqFt, then summing these two
amounts. The production levels must satisfy the following constraints: the
production of laminate planks must be at least MinLaminateDemand and no more
than MaxLaminateProduction; the production of carpets must be at least
MinCarpetDemand and no more than MaxCarpetProduction; and the combined
production of both products must meet or exceed MinTotalShipping.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/201/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MinLaminateDemand @Def: Minimum weekly demand for laminate planks @Shape: [] 
MinLaminateDemand = data['MinLaminateDemand']
# @Parameter MinCarpetDemand @Def: Minimum weekly demand for carpets @Shape: [] 
MinCarpetDemand = data['MinCarpetDemand']
# @Parameter MinTotalShipping @Def: Minimum total weekly shipping requirement @Shape: [] 
MinTotalShipping = data['MinTotalShipping']
# @Parameter MaxLaminateProduction @Def: Maximum weekly production capacity for laminate planks @Shape: [] 
MaxLaminateProduction = data['MaxLaminateProduction']
# @Parameter MaxCarpetProduction @Def: Maximum weekly production capacity for carpets @Shape: [] 
MaxCarpetProduction = data['MaxCarpetProduction']
# @Parameter LaminateProfitPerSqFt @Def: Profit per square foot for laminate planks @Shape: [] 
LaminateProfitPerSqFt = data['LaminateProfitPerSqFt']
# @Parameter CarpetProfitPerSqFt @Def: Profit per square foot for carpets @Shape: [] 
CarpetProfitPerSqFt = data['CarpetProfitPerSqFt']

# Variables 
# @Variable LaminateProduction @Def: The weekly production level of laminate planks @Shape: [] 
LaminateProduction = model.addVar(lb=0, ub=MaxLaminateProduction, vtype=GRB.CONTINUOUS, name="LaminateProduction")
# @Variable CarpetProduction @Def: The weekly production level of carpets @Shape: [] 
CarpetProduction = model.addVar(vtype=GRB.CONTINUOUS, name="CarpetProduction")

# Constraints 
# @Constraint Constr_1 @Def: The production level of laminate planks must be at least MinLaminateDemand.
model.addConstr(LaminateProduction >= MinLaminateDemand)
# @Constraint Constr_2 @Def: The production level of laminate planks must be no more than MaxLaminateProduction.
model.addConstr(LaminateProduction <= MaxLaminateProduction, "LaminateProductionLimit")
# @Constraint Constr_3 @Def: The production level of carpets must be at least MinCarpetDemand.
model.addConstr(CarpetProduction >= MinCarpetDemand)
# @Constraint Constr_4 @Def: The production level of carpets must be no more than MaxCarpetProduction.
model.addConstr(CarpetProduction <= MaxCarpetProduction)
# @Constraint Constr_5 @Def: The combined production levels of laminate planks and carpets must meet or exceed MinTotalShipping.
model.addConstr(LaminateProduction + CarpetProduction >= MinTotalShipping)

# Objective 
# @Objective Objective @Def: Total profit is calculated by multiplying the production level of laminate planks by LaminateProfitPerSqFt and the production level of carpets by CarpetProfitPerSqFt, then summing these two amounts. The objective is to maximize the total profit.
model.setObjective(LaminateProfitPerSqFt * LaminateProduction + CarpetProfitPerSqFt * CarpetProduction, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['LaminateProduction'] = LaminateProduction.x
variables['CarpetProduction'] = CarpetProduction.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
