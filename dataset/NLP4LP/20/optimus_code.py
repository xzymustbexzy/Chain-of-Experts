# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
The store produces premium desktops and regular desktops. The total number of
desktops produced does not exceed MaxDesktopSales. The total manufacturing cost,
calculated as the number of premium desktops multiplied by
ManufacturingCostPremiumDesktop plus the number of regular desktops multiplied
by ManufacturingCostRegularDesktop, does not exceed MaxManufacturingBudget. The
objective is to maximize profit, which is the number of premium desktops
multiplied by ProfitPremiumDesktop plus the number of regular desktops
multiplied by ProfitRegularDesktop.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/21/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ManufacturingCostPremiumDesktop @Def: Manufacturing cost of a premium desktop @Shape: [] 
ManufacturingCostPremiumDesktop = data['ManufacturingCostPremiumDesktop']
# @Parameter ManufacturingCostRegularDesktop @Def: Manufacturing cost of a regular desktop @Shape: [] 
ManufacturingCostRegularDesktop = data['ManufacturingCostRegularDesktop']
# @Parameter ProfitPremiumDesktop @Def: Profit from a premium desktop @Shape: [] 
ProfitPremiumDesktop = data['ProfitPremiumDesktop']
# @Parameter ProfitRegularDesktop @Def: Profit from a regular desktop @Shape: [] 
ProfitRegularDesktop = data['ProfitRegularDesktop']
# @Parameter MaxDesktopSales @Def: Maximum number of desktops sold per month @Shape: [] 
MaxDesktopSales = data['MaxDesktopSales']
# @Parameter MaxManufacturingBudget @Def: Maximum spending on making the desktops @Shape: [] 
MaxManufacturingBudget = data['MaxManufacturingBudget']

# Variables 
# @Variable NumPremiumDesktops @Def: The number of premium desktops produced @Shape: ['Continuous', 'NonNegative'] 
NumPremiumDesktops = model.addVar(vtype=GRB.CONTINUOUS, lb=0, name="NumPremiumDesktops")
# @Variable NumRegularDesktops @Def: The number of regular desktops produced @Shape: ['Continuous', 'NonNegative'] 
NumRegularDesktops = model.addVar(vtype=GRB.CONTINUOUS, name="NumRegularDesktops")

# Constraints 
# @Constraint Constr_1 @Def: The total number of desktops produced does not exceed MaxDesktopSales.
model.addConstr(NumPremiumDesktops + NumRegularDesktops <= MaxDesktopSales)
# @Constraint Constr_2 @Def: The total manufacturing cost, calculated as the number of premium desktops multiplied by ManufacturingCostPremiumDesktop plus the number of regular desktops multiplied by ManufacturingCostRegularDesktop, does not exceed MaxManufacturingBudget.
model.addConstr(ManufacturingCostPremiumDesktop * NumPremiumDesktops + ManufacturingCostRegularDesktop * NumRegularDesktops <= MaxManufacturingBudget)

# Objective 
# @Objective Objective @Def: The profit is the number of premium desktops multiplied by ProfitPremiumDesktop plus the number of regular desktops multiplied by ProfitRegularDesktop. The objective is to maximize profit.
model.setObjective(ProfitPremiumDesktop * NumPremiumDesktops + ProfitRegularDesktop * NumRegularDesktops, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumPremiumDesktops'] = NumPremiumDesktops.x
variables['NumRegularDesktops'] = NumRegularDesktops.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
