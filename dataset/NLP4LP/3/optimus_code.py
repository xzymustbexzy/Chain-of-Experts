# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
There is TotalGold available to produce long and short cables. Each long cable
requires GoldPerLong amount of gold, while each short cable requires
GoldPerShort amount of gold. At least MinShortToLongRatio times the number of
long cables must be produced as short cables. Additionally, a minimum of
MinLongCables long cables must be made. Each long cable sold generates a
ProfitPerLong profit, and each short cable sold generates a ProfitPerShort
profit. Determine the number of each type of cable to maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/4/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalGold @Def: Total amount of gold available @Shape: [] 
TotalGold = data['TotalGold']
# @Parameter GoldPerLong @Def: Amount of gold required to produce one long cable @Shape: [] 
GoldPerLong = data['GoldPerLong']
# @Parameter GoldPerShort @Def: Amount of gold required to produce one short cable @Shape: [] 
GoldPerShort = data['GoldPerShort']
# @Parameter MinShortToLongRatio @Def: Minimum ratio of the number of short cables to long cables @Shape: [] 
MinShortToLongRatio = data['MinShortToLongRatio']
# @Parameter MinLongCables @Def: Minimum number of long cables to be made @Shape: [] 
MinLongCables = data['MinLongCables']
# @Parameter ProfitPerLong @Def: Profit earned per long cable sold @Shape: [] 
ProfitPerLong = data['ProfitPerLong']
# @Parameter ProfitPerShort @Def: Profit earned per short cable sold @Shape: [] 
ProfitPerShort = data['ProfitPerShort']

# Variables 
# @Variable NumberLongCables @Def: The number of long cables to produce @Shape: [] 
NumberLongCables = model.addVar(vtype=GRB.INTEGER, name="NumberLongCables")
# @Variable NumberShortCables @Def: The number of short cables to produce @Shape: [] 
NumberShortCables = model.addVar(vtype=GRB.INTEGER, name="NumberShortCables")

# Constraints 
# @Constraint Constr_1 @Def: Each long cable requires GoldPerLong amount of gold, and each short cable requires GoldPerShort amount of gold. The total amount of gold used cannot exceed TotalGold.
model.addConstr(NumberLongCables * GoldPerLong + NumberShortCables * GoldPerShort <= TotalGold)
# @Constraint Constr_2 @Def: At least MinShortToLongRatio times the number of long cables must be produced as short cables. Additionally, a minimum of MinLongCables long cables must be made.
model.addConstr(NumberShortCables >= MinShortToLongRatio * NumberLongCables)
model.addConstr(NumberLongCables >= MinLongCables)

# Objective 
# @Objective Objective @Def: Total profit is the sum of the profits from long and short cables. The objective is to maximize total profit.
model.setObjective(ProfitPerLong * NumberLongCables + ProfitPerShort * NumberShortCables, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberLongCables'] = NumberLongCables.x
variables['NumberShortCables'] = NumberShortCables.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
