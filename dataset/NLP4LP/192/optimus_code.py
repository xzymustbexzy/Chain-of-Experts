# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A milk tea shop owner aims to produce NumMilkTeaTypes different types of milk
tea. Each type requires specific amounts of NumResources different resources as
defined by ResourceUsage. The profit earned from each bottle of milk tea type j
is ProfitPerBottle[j]. The total usage of each resource i must not exceed
AvailableResource[i]. The objective is to determine the number of bottles of
each milk tea type to produce in order to maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/193/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumMilkTeaTypes @Def: Number of different milk tea types to be produced @Shape: [] 
NumMilkTeaTypes = data['NumMilkTeaTypes']
# @Parameter NumResources @Def: Number of different resources used in production @Shape: [] 
NumResources = data['NumResources']
# @Parameter ResourceUsage @Def: Amount of resource i required to produce one bottle of milk tea type j @Shape: ['NumResources', 'NumMilkTeaTypes'] 
ResourceUsage = data['ResourceUsage']
# @Parameter ProfitPerBottle @Def: Profit earned from selling one bottle of milk tea type j @Shape: ['NumMilkTeaTypes'] 
ProfitPerBottle = data['ProfitPerBottle']
# @Parameter AvailableResource @Def: Total available amount of resource i @Shape: ['NumResources'] 
AvailableResource = data['AvailableResource']

# Variables 
# @Variable Produce @Def: The number of bottles produced for each milk tea type @Shape: ['NumMilkTeaTypes'] 
Produce = model.addVars(NumMilkTeaTypes, vtype=GRB.CONTINUOUS, name="Produce")

# Constraints 
# @Constraint Constr_1 @Def: The total usage of each resource must not exceed the available amount of that resource.
model.addConstrs((quicksum(ResourceUsage[i][j] * Produce[j] for j in range(NumMilkTeaTypes)) <= AvailableResource[i] for i in range(NumResources)), name='ResourceLimits')
# @Constraint Constr_2 @Def: The number of bottles of each milk tea type to produce must be non-negative.
model.addConstrs((Produce[j] >= 0 for j in range(NumMilkTeaTypes)), "ProduceNonNegative")

# Objective 
# @Objective Objective @Def: Total profit is the sum of the profits from each milk tea type. The objective is to maximize the total profit.
model.setObjective(quicksum(ProfitPerBottle[j] * Produce[j] for j in range(NumMilkTeaTypes)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Produce'] = model.getAttr("X", Produce)
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
