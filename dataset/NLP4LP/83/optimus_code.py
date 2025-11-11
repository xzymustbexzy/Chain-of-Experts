# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
There are NumReactions different chemical reactions. Each reaction requires
ResourceRequirement units of each of the NumResources types of resources and
produces ProductionPerReaction units of a rare compound. There are
ResourceAvailable units of each resource available in the lab. Determine the
number of reactions of each type to maximize the total amount of the rare
compound produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/84/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumReactions @Def: Number of reaction types @Shape: [] 
NumReactions = data['NumReactions']
# @Parameter NumResources @Def: Number of resource types @Shape: [] 
NumResources = data['NumResources']
# @Parameter ResourceRequirement @Def: Units of resource j required for reaction i @Shape: ['NumReactions', 'NumResources'] 
ResourceRequirement = data['ResourceRequirement']
# @Parameter ProductionPerReaction @Def: Units of rare compound produced by reaction i @Shape: ['NumReactions'] 
ProductionPerReaction = data['ProductionPerReaction']
# @Parameter ResourceAvailable @Def: Total units of resource j available @Shape: ['NumResources'] 
ResourceAvailable = data['ResourceAvailable']
    
# Variables 
# @Variable NumberReactions @Def: The number of reactions of type i @Shape: ['NumReactions'] 
NumberReactions = model.addVars(NumReactions, vtype=GRB.CONTINUOUS, name="NumberReactions")
    
# Constraints 
# @Constraint Constr_1 @Def: For each resource type, the total units used by all reactions cannot exceed the available ResourceAvailable units. Specifically, for each resource j, the sum of (ResourceRequirement[i][j] * number of reactions of type i) across all reactions i must be less than or equal to ResourceAvailable[j].
model.addConstrs((quicksum(ResourceRequirement[i][j] * NumberReactions[i] for i in range(NumReactions)) <= ResourceAvailable[j] for j in range(NumResources)), name='ResourceUsage')
# @Constraint Constr_2 @Def: The number of reactions of each type must be non-negative.
model.addConstrs((NumberReactions[i] >= 0 for i in range(NumReactions)))
    
# Objective 
# @Objective Objective @Def: The total amount of the rare compound produced is the sum of (ProductionPerReaction[i] * number of reactions of type i) across all reactions i. The objective is to maximize the total amount of the rare compound produced.
model.setObjective(quicksum(ProductionPerReaction[i] * NumberReactions[i] for i in range(NumReactions)), GRB.MAXIMIZE)
    
# Solve 
model.optimize()
    
# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberReactions'] = {i: NumberReactions[i].X for i in range(NumReactions)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
