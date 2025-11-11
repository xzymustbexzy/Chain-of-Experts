# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
There are NumContainers types of specialized containers used to produce paste.
Each container type requires WaterRequiredPerContainer units of water and
PowderedPillRequiredPerContainer units of powdered pill to produce
PasteProducedPerContainer units of paste. The pharmacy has WaterAvailability
units of water and PowderedPillAvailability units of powdered pill available.
Determine the number of each container type to maximize the total amount of
paste produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/54/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumContainers @Def: Number of container types @Shape: [] 
NumContainers = data['NumContainers']
# @Parameter WaterAvailability @Def: Available units of water @Shape: [] 
WaterAvailability = data['WaterAvailability']
# @Parameter PowderedPillAvailability @Def: Available units of powdered pill @Shape: [] 
PowderedPillAvailability = data['PowderedPillAvailability']
# @Parameter WaterRequiredPerContainer @Def: Water required per container type @Shape: ['NumContainers'] 
WaterRequiredPerContainer = data['WaterRequiredPerContainer']
# @Parameter PowderedPillRequiredPerContainer @Def: Powdered pill required per container type @Shape: ['NumContainers'] 
PowderedPillRequiredPerContainer = data['PowderedPillRequiredPerContainer']
# @Parameter PasteProducedPerContainer @Def: Paste produced per container type @Shape: ['NumContainers'] 
PasteProducedPerContainer = data['PasteProducedPerContainer']

# Variables 
# @Variable NumUsedContainers @Def: The number of containers used for each container type @Shape: ['NumContainers'] 
NumUsedContainers = model.addVars(NumContainers, vtype=GRB.INTEGER, name="NumUsedContainers")

# Constraints 
# @Constraint Constr_1 @Def: The total water required by all container types does not exceed the available units of water.
model.addConstr(quicksum(WaterRequiredPerContainer[j] * NumUsedContainers[j] for j in range(NumContainers)) <= WaterAvailability)
# @Constraint Constr_2 @Def: The total powdered pill required by all container types does not exceed the available units of powdered pill.
model.addConstr(quicksum(NumUsedContainers[c] * PowderedPillRequiredPerContainer[c] for c in range(NumContainers)) <= PowderedPillAvailability)

# Objective 
# @Objective Objective @Def: The total paste produced is the sum of the paste produced by each container type. The objective is to maximize the total amount of paste produced.
model.setObjective(quicksum(PasteProducedPerContainer[i] * NumUsedContainers[i] for i in range(NumContainers)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumUsedContainers'] = [NumUsedContainers[j].X for j in range(NumContainers)]
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)