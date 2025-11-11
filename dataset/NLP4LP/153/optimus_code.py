# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A sand company delivers sand using small containers and large containers. Each
small container requires UnloadPersonsSmall persons to unload and can hold
CapacitySmall units of sand. Each large container requires UnloadPersonsLarge
persons to unload and can hold CapacityLarge units of sand. The number of small
containers used must be RatioSmallToLargeContainers times the number of large
containers used. At least MinSmallContainers small containers and
MinLargeContainers large containers must be used. The company has
TotalPersonsAvailable persons available. The objective is to maximize the total
units of sand delivered.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/154/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter UnloadPersonsSmall @Def: Number of persons required to unload a small container @Shape: [] 
UnloadPersonsSmall = data['UnloadPersonsSmall']
# @Parameter CapacitySmall @Def: Units of sand a small container can hold @Shape: [] 
CapacitySmall = data['CapacitySmall']
# @Parameter UnloadPersonsLarge @Def: Number of persons required to unload a large container @Shape: [] 
UnloadPersonsLarge = data['UnloadPersonsLarge']
# @Parameter CapacityLarge @Def: Units of sand a large container can hold @Shape: [] 
CapacityLarge = data['CapacityLarge']
# @Parameter RatioSmallToLargeContainers @Def: Required ratio of small containers to large containers @Shape: [] 
RatioSmallToLargeContainers = data['RatioSmallToLargeContainers']
# @Parameter MinSmallContainers @Def: Minimum number of small containers to be used @Shape: [] 
MinSmallContainers = data['MinSmallContainers']
# @Parameter MinLargeContainers @Def: Minimum number of large containers to be used @Shape: [] 
MinLargeContainers = data['MinLargeContainers']
# @Parameter TotalPersonsAvailable @Def: Total number of persons available @Shape: [] 
TotalPersonsAvailable = data['TotalPersonsAvailable']

# Variables 
# @Variable SmallContainers @Def: The number of small containers used @Shape: ['Integer'] 
SmallContainers = model.addVar(vtype=GRB.INTEGER, name="SmallContainers")
# @Variable LargeContainers @Def: The number of large containers used @Shape: ['Integer'] 
LargeContainers = model.addVar(vtype=GRB.INTEGER, name='LargeContainers')

# Constraints 
# @Constraint Constr_1 @Def: The number of small containers used must be RatioSmallToLargeContainers times the number of large containers used.
model.addConstr(SmallContainers == RatioSmallToLargeContainers * LargeContainers)
# @Constraint Constr_2 @Def: At least MinSmallContainers small containers must be used.
model.addConstr(SmallContainers >= MinSmallContainers)
# @Constraint Constr_3 @Def: At least MinLargeContainers large containers must be used.
model.addConstr(LargeContainers >= MinLargeContainers)
# @Constraint Constr_4 @Def: The total number of persons required to unload all containers cannot exceed TotalPersonsAvailable.
model.addConstr(UnloadPersonsSmall * SmallContainers + UnloadPersonsLarge * LargeContainers <= TotalPersonsAvailable)

# Objective 
# @Objective Objective @Def: Total units of sand delivered is the sum of the sand held by small and large containers. The objective is to maximize the total units of sand delivered.
model.setObjective(SmallContainers * CapacitySmall + LargeContainers * CapacityLarge, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SmallContainers'] = SmallContainers.x
variables['LargeContainers'] = LargeContainers.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
