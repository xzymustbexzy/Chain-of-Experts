# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A taco stand sells regular tacos and deluxe tacos with extra meat. The stand
makes x1 regular tacos at a profit of ProfitPerRegularTaco each and x2 deluxe
tacos at a profit of ProfitPerDeluxeTaco each (x1 and x2 are unknown variables
both greater than or equal to 0). There is a demand for at most
MaxDemandRegularTacos regular tacos and at most MaxDemandDeluxeTacos deluxe
tacos. The stand only has enough supplies to sell at most MaxTotalSupplyTacos
tacos of either type. How many of each taco should the stand make to maximize
profit?
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/208/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProfitPerRegularTaco @Def: Profit per regular taco @Shape: [] 
ProfitPerRegularTaco = data['ProfitPerRegularTaco']
# @Parameter ProfitPerDeluxeTaco @Def: Profit per deluxe taco @Shape: [] 
ProfitPerDeluxeTaco = data['ProfitPerDeluxeTaco']
# @Parameter MaxDemandRegularTacos @Def: Maximum demand for regular tacos @Shape: [] 
MaxDemandRegularTacos = data['MaxDemandRegularTacos']
# @Parameter MaxDemandDeluxeTacos @Def: Maximum demand for deluxe tacos @Shape: [] 
MaxDemandDeluxeTacos = data['MaxDemandDeluxeTacos']
# @Parameter MaxTotalSupplyTacos @Def: Maximum total supply of tacos @Shape: [] 
MaxTotalSupplyTacos = data['MaxTotalSupplyTacos']

# Variables 
# @Variable RegularTacosProduced @Def: The number of regular tacos produced @Shape: [] 
RegularTacosProduced = model.addVar(vtype=GRB.CONTINUOUS, name="RegularTacosProduced")
# @Variable DeluxeTacosProduced @Def: The number of deluxe tacos produced @Shape: [] 
DeluxeTacosProduced = model.addVar(vtype=GRB.CONTINUOUS, name="DeluxeTacosProduced")

# Constraints 
# @Constraint Constr_1 @Def: The number of regular tacos produced does not exceed the maximum demand for regular tacos.
model.addConstr(RegularTacosProduced <= MaxDemandRegularTacos)
# @Constraint Constr_2 @Def: The number of deluxe tacos produced does not exceed the maximum demand for deluxe tacos.
model.addConstr(DeluxeTacosProduced <= MaxDemandDeluxeTacos)
# @Constraint Constr_3 @Def: The total number of tacos produced does not exceed the maximum total supply of tacos.
model.addConstr(RegularTacosProduced + DeluxeTacosProduced <= MaxTotalSupplyTacos)
# @Constraint Constr_4 @Def: The number of regular tacos produced is non-negative.
model.addConstr(RegularTacosProduced >= 0)
# @Constraint Constr_5 @Def: The number of deluxe tacos produced is non-negative.
model.addConstr(DeluxeTacosProduced >= 0)

# Objective 
# @Objective Objective @Def: The objective is to maximize the total profit, calculated as the sum of the profits from regular and deluxe tacos.
model.setObjective(ProfitPerRegularTaco * RegularTacosProduced + ProfitPerDeluxeTaco * DeluxeTacosProduced, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['RegularTacosProduced'] = RegularTacosProduced.x
variables['DeluxeTacosProduced'] = DeluxeTacosProduced.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
