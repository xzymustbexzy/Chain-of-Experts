# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A family has a TotalInvestment to allocate between apartments and townhouses.
The investment in apartments must not exceed MaxInvestmentApartments and must be
at least MinInvestmentRatio times the investment in townhouses. Apartments yield
a return rate of ReturnRateApartments and townhouses yield a return rate of
ReturnRateTownhouses. The goal is to determine the investment amounts in each to
maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/15/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalInvestment @Def: Total amount available for investment @Shape: [] 
TotalInvestment = data['TotalInvestment']
# @Parameter MaxInvestmentApartments @Def: Maximum amount that can be invested in apartments @Shape: [] 
MaxInvestmentApartments = data['MaxInvestmentApartments']
# @Parameter MinInvestmentRatio @Def: Minimum ratio of investment in apartments to investment in townhouses @Shape: [] 
MinInvestmentRatio = data['MinInvestmentRatio']
# @Parameter ReturnRateApartments @Def: Return on investment rate for apartments @Shape: [] 
ReturnRateApartments = data['ReturnRateApartments']
# @Parameter ReturnRateTownhouses @Def: Return on investment rate for townhouses @Shape: [] 
ReturnRateTownhouses = data['ReturnRateTownhouses']

# Variables 
# @Variable InvestmentApartments @Def: The amount invested in apartments @Shape: [] 
InvestmentApartments = model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=MaxInvestmentApartments, name="InvestmentApartments")
# @Variable InvestmentTownhouses @Def: The amount invested in townhouses @Shape: [] 
InvestmentTownhouses = model.addVar(vtype=GRB.CONTINUOUS, name="InvestmentTownhouses")

# Constraints 
# @Constraint Constr_1 @Def: The total investment allocated to apartments and townhouses must equal TotalInvestment.
model.addConstr(InvestmentApartments + InvestmentTownhouses == TotalInvestment)
# @Constraint Constr_2 @Def: The investment in apartments must not exceed MaxInvestmentApartments.
model.addConstr(InvestmentApartments <= MaxInvestmentApartments)
# @Constraint Constr_3 @Def: The investment in apartments must be at least MinInvestmentRatio times the investment in townhouses.
model.addConstr(InvestmentApartments >= MinInvestmentRatio * InvestmentTownhouses)

# Objective 
# @Objective Objective @Def: Maximize total profit, which is the sum of ReturnRateApartments multiplied by the investment in apartments and ReturnRateTownhouses multiplied by the investment in townhouses.
model.setObjective(ReturnRateApartments * InvestmentApartments + ReturnRateTownhouses * InvestmentTownhouses, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['InvestmentApartments'] = InvestmentApartments.x
variables['InvestmentTownhouses'] = InvestmentTownhouses.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
