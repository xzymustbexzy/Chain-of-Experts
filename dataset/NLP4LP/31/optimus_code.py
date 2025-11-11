# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A berry farmer operates NumFarms farms to harvest and deliver NumBerries types
of berries in order to fulfill a contract requiring RequiredQuantity of each
berry type. Each farm incurs an OperatingCost per day and can harvest and
deliver HarvestDelivery amounts of each berry type per day. The farmer aims to
minimize the total operating cost while ensuring that the harvested and
delivered quantities meet or exceed the RequiredQuantity for each type of berry.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/32/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumFarms @Def: Number of farms @Shape: [] 
NumFarms = data['NumFarms']
# @Parameter NumBerries @Def: Number of berry types @Shape: [] 
NumBerries = data['NumBerries']
# @Parameter OperatingCost @Def: Operating cost per day for each farm @Shape: ['NumFarms'] 
OperatingCost = data['OperatingCost']
# @Parameter HarvestDelivery @Def: Harvest and delivery rate per day for each farm and berry type @Shape: ['NumFarms', 'NumBerries'] 
HarvestDelivery = data['HarvestDelivery']
# @Parameter RequiredQuantity @Def: Required quantity of each berry type to meet contract @Shape: ['NumBerries'] 
RequiredQuantity = data['RequiredQuantity']

# Variables 
# @Variable DaysOperated @Def: The number of days each farm operates @Shape: ['NumFarms'] 
DaysOperated = model.addVars(NumFarms, vtype=GRB.CONTINUOUS, name="DaysOperated")

# Constraints 
# @Constraint Constr_1 @Def: For each berry type, the total harvested and delivered quantity across all farms must meet or exceed the RequiredQuantity.
model.addConstrs((quicksum(HarvestDelivery[f][b] * DaysOperated[f] for f in range(NumFarms)) >= RequiredQuantity[b] for b in range(NumBerries)))

# Objective 
# @Objective Objective @Def: Minimize the total operating cost while ensuring that the harvested and delivered quantities meet or exceed the RequiredQuantity for each type of berry.
model.setObjective(quicksum(OperatingCost[i] * DaysOperated[i] for i in range(NumFarms)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['DaysOperated'] = [DaysOperated[f].x for f in range(NumFarms)]
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)