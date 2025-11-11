# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Mark has TotalLandAvailable acres of land to grow potatoes and cucumbers. He
must grow at least MinAcresPotatoes acres of potatoes and at least
MinAcresCucumbers acres of cucumbers to meet his contract. Mark prefers to grow
more cucumbers than potatoes, but he can grow at most
MaxCucumbersPerPotatoesRatio times as many cucumbers as potatoes. The profit per
acre of potatoes is ProfitPerAcrePotatoes and the profit per acre of cucumbers
is ProfitPerAcreCucumbers. He aims to determine the number of acres to allocate
to each crop to maximize his total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/30/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalLandAvailable @Def: Total land available to grow crops @Shape: [] 
TotalLandAvailable = data['TotalLandAvailable']
# @Parameter MinAcresPotatoes @Def: Minimum acres of potatoes required @Shape: [] 
MinAcresPotatoes = data['MinAcresPotatoes']
# @Parameter MinAcresCucumbers @Def: Minimum acres of cucumbers required @Shape: [] 
MinAcresCucumbers = data['MinAcresCucumbers']
# @Parameter MaxCucumbersPerPotatoesRatio @Def: Maximum ratio of cucumbers to potatoes that can be grown @Shape: [] 
MaxCucumbersPerPotatoesRatio = data['MaxCucumbersPerPotatoesRatio']
# @Parameter ProfitPerAcrePotatoes @Def: Profit per acre of potatoes @Shape: [] 
ProfitPerAcrePotatoes = data['ProfitPerAcrePotatoes']
# @Parameter ProfitPerAcreCucumbers @Def: Profit per acre of cucumbers @Shape: [] 
ProfitPerAcreCucumbers = data['ProfitPerAcreCucumbers']

# Variables 
# @Variable AcresPotatoes @Def: The number of acres allocated to potatoes @Shape: [] 
AcresPotatoes = model.addVar(vtype=GRB.CONTINUOUS, lb=MinAcresPotatoes, name="AcresPotatoes")
# @Variable AcresCucumbers @Def: The number of acres allocated to cucumbers @Shape: [] 
AcresCucumbers = model.addVar(vtype=GRB.CONTINUOUS, name="AcresCucumbers")

# Constraints 
# @Constraint Constr_1 @Def: The number of acres allocated to potatoes must be at least MinAcresPotatoes.
model.addConstr(AcresPotatoes >= MinAcresPotatoes)
# @Constraint Constr_2 @Def: The number of acres allocated to cucumbers must be at least MinAcresCucumbers.
model.addConstr(AcresCucumbers >= MinAcresCucumbers)
# @Constraint Constr_3 @Def: The total acres allocated to potatoes and cucumbers must not exceed TotalLandAvailable.
model.addConstr(AcresPotatoes + AcresCucumbers <= TotalLandAvailable)
# @Constraint Constr_4 @Def: The number of acres allocated to cucumbers must be at most MaxCucumbersPerPotatoesRatio times the number of acres allocated to potatoes.
model.addConstr(AcresCucumbers <= MaxCucumbersPerPotatoesRatio * AcresPotatoes)
# @Constraint Constr_5 @Def: The number of acres allocated to cucumbers must be at least equal to the number of acres allocated to potatoes.
model.addConstr(AcresCucumbers >= AcresPotatoes)

# Objective 
# @Objective Objective @Def: Maximize total profit, where total profit is calculated as (ProfitPerAcrePotatoes × acres of potatoes) plus (ProfitPerAcreCucumbers × acres of cucumbers).
model.setObjective(ProfitPerAcrePotatoes * AcresPotatoes + ProfitPerAcreCucumbers * AcresCucumbers, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['AcresPotatoes'] = AcresPotatoes.x
variables['AcresCucumbers'] = AcresCucumbers.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
