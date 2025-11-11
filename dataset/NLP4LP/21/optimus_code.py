# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
The manufacturer aims to maximize total profit, calculated as ProfitRegular
multiplied by the number of regular models produced (x₁) plus ProfitPremium
multiplied by the number of premium models produced (x₂). This objective is
subject to the following constraints: the number of regular models produced (x₁)
must not exceed DemandRegular, the number of premium models produced (x₂) must
not exceed DemandPremium, the combined production of regular and premium models
(x₁ + x₂) must not exceed MaxCarsTotal, and both x₁ and x₂ must be greater than
or equal to zero.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/22/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProfitRegular @Def: Profit per regular model @Shape: [] 
ProfitRegular = data['ProfitRegular']
# @Parameter ProfitPremium @Def: Profit per premium model @Shape: [] 
ProfitPremium = data['ProfitPremium']
# @Parameter DemandRegular @Def: Daily demand for regular models @Shape: [] 
DemandRegular = data['DemandRegular']
# @Parameter DemandPremium @Def: Daily demand for premium models @Shape: [] 
DemandPremium = data['DemandPremium']
# @Parameter MaxCarsTotal @Def: Maximum number of cars that can be made per day @Shape: [] 
MaxCarsTotal = data['MaxCarsTotal']

# Variables 
# @Variable RegularModelsProduced @Def: The number of regular models produced @Shape: [] 
RegularModelsProduced = model.addVar(vtype=GRB.CONTINUOUS, name="RegularModelsProduced")
# @Variable PremiumModelsProduced @Def: The number of premium models produced @Shape: [] 
PremiumModelsProduced = model.addVar(vtype=GRB.CONTINUOUS, name="PremiumModelsProduced")

# Constraints 
# @Constraint Constr_1 @Def: The number of regular models produced (x₁) must not exceed DemandRegular.
model.addConstr(RegularModelsProduced <= DemandRegular)
# @Constraint Constr_2 @Def: The number of premium models produced (x₂) must not exceed DemandPremium.
model.addConstr(PremiumModelsProduced <= DemandPremium)
# @Constraint Constr_3 @Def: The combined production of regular and premium models (x₁ + x₂) must not exceed MaxCarsTotal.
model.addConstr(RegularModelsProduced + PremiumModelsProduced <= MaxCarsTotal)
# @Constraint Constr_4 @Def: Both x₁ and x₂ must be greater than or equal to zero.
model.addConstr(RegularModelsProduced >= 0)
model.addConstr(PremiumModelsProduced >= 0)

# Objective 
# @Objective Objective @Def: Maximize total profit, calculated as ProfitRegular multiplied by the number of regular models produced (x₁) plus ProfitPremium multiplied by the number of premium models produced (x₂).
model.setObjective(ProfitRegular * RegularModelsProduced + ProfitPremium * PremiumModelsProduced, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['RegularModelsProduced'] = RegularModelsProduced.x
variables['PremiumModelsProduced'] = PremiumModelsProduced.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
