# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A flooring company produces two types of products: hardwood and vinyl planks.
The weekly production of hardwood must be at least MinimumDemandHardwood and no
more than MaxProductionHardwood. Similarly, the weekly production of vinyl
planks must be at least MinimumDemandVinyl and no more than MaxProductionVinyl.
Additionally, the combined weekly production of both hardwood and vinyl planks
must be at least MinimumTotalShipping. The objective is to maximize the total
profit, which is calculated as ProfitHardwood multiplied by the quantity of
hardwood produced plus ProfitVinyl multiplied by the quantity of vinyl planks
produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/31/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MinimumDemandHardwood @Def: Minimum expected weekly demand for hardwood @Shape: [] 
MinimumDemandHardwood = data['MinimumDemandHardwood']
# @Parameter MinimumDemandVinyl @Def: Minimum expected weekly demand for vinyl planks @Shape: [] 
MinimumDemandVinyl = data['MinimumDemandVinyl']
# @Parameter MinimumTotalShipping @Def: Minimum total square feet of flooring to be shipped weekly @Shape: [] 
MinimumTotalShipping = data['MinimumTotalShipping']
# @Parameter MaxProductionHardwood @Def: Maximum weekly production capacity for hardwood @Shape: [] 
MaxProductionHardwood = data['MaxProductionHardwood']
# @Parameter MaxProductionVinyl @Def: Maximum weekly production capacity for vinyl planks @Shape: [] 
MaxProductionVinyl = data['MaxProductionVinyl']
# @Parameter ProfitHardwood @Def: Profit per square foot of hardwood @Shape: [] 
ProfitHardwood = data['ProfitHardwood']
# @Parameter ProfitVinyl @Def: Profit per square foot of vinyl planks @Shape: [] 
ProfitVinyl = data['ProfitVinyl']

# Variables 
# @Variable ProductionHardwood @Def: Weekly production of hardwood @Shape: [] 
ProductionHardwood = model.addVar(lb=MinimumDemandHardwood, ub=MaxProductionHardwood, vtype=GRB.CONTINUOUS, name="ProductionHardwood")
# @Variable ProductionVinyl @Def: Weekly production of vinyl planks @Shape: [] 
ProductionVinyl = model.addVar(vtype=GRB.CONTINUOUS, name="ProductionVinyl")

# Constraints 
# @Constraint Constr_1 @Def: Weekly production of hardwood must be at least MinimumDemandHardwood.
model.addConstr(ProductionHardwood >= MinimumDemandHardwood)
# @Constraint Constr_2 @Def: Weekly production of hardwood must be no more than MaxProductionHardwood.
model.addConstr(ProductionHardwood <= MaxProductionHardwood)
# @Constraint Constr_3 @Def: Weekly production of vinyl planks must be at least MinimumDemandVinyl.
model.addConstr(ProductionVinyl >= MinimumDemandVinyl)
# @Constraint Constr_4 @Def: Weekly production of vinyl planks must be no more than MaxProductionVinyl.
model.addConstr(ProductionVinyl <= MaxProductionVinyl)
# @Constraint Constr_5 @Def: The combined weekly production of both hardwood and vinyl planks must be at least MinimumTotalShipping.
model.addConstr(ProductionHardwood + ProductionVinyl >= MinimumTotalShipping)

# Objective 
# @Objective Objective @Def: Total profit is calculated as ProfitHardwood multiplied by the quantity of hardwood produced plus ProfitVinyl multiplied by the quantity of vinyl planks produced. The objective is to maximize the total profit.
model.setObjective(ProfitHardwood * ProductionHardwood + ProfitVinyl * ProductionVinyl, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ProductionHardwood'] = ProductionHardwood.x
variables['ProductionVinyl'] = ProductionVinyl.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
