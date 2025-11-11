# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
An automotive company is comparing NumCatalysts different catalysts. Each
catalyst requires amounts of resources as specified by ResourceRequirement and
has a conversion rate defined by ConversionRate. Given the TotalResource
available for each resource, determine the number of each catalyst to use to
maximize the total conversion rate without exceeding the available resources.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/247/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumCatalysts @Def: Number of catalyst types @Shape: [] 
NumCatalysts = data['NumCatalysts']
# @Parameter NumResources @Def: Number of resources @Shape: [] 
NumResources = data['NumResources']
# @Parameter ResourceRequirement @Def: Amount of resource r required per unit of catalyst c @Shape: ['NumResources', 'NumCatalysts'] 
ResourceRequirement = data['ResourceRequirement']
# @Parameter ConversionRate @Def: Conversion rate per unit of catalyst c @Shape: ['NumCatalysts'] 
ConversionRate = data['ConversionRate']
# @Parameter TotalResource @Def: Total amount of resource r available @Shape: ['NumResources'] 
TotalResource = data['TotalResource']

# Variables 
# @Variable CatalystUsage @Def: The amount of catalyst c to use @Shape: ['NumCatalysts'] 
CatalystUsage = model.addVars(NumCatalysts, vtype=GRB.CONTINUOUS, name="CatalystUsage")

# Constraints 
# @Constraint Constr_1 @Def: For each resource, the total amount consumed by all catalysts must not exceed the available TotalResource.
model.addConstrs((quicksum(ResourceRequirement[r][c] * CatalystUsage[c] for c in range(NumCatalysts)) <= TotalResource[r] for r in range(NumResources)), name="ResourceConstraint")

# Objective 
# @Objective Objective @Def: Maximize the total conversion rate, calculated as the sum of ConversionRate multiplied by the number of each catalyst used.
model.setObjective(quicksum(ConversionRate[c] * CatalystUsage[c] for c in range(NumCatalysts)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['CatalystUsage'] = {c: CatalystUsage[c].X for c in range(NumCatalysts)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)